"""
Routines to execute commands locally, inside of jails, remotely in jails
as well as log into them, and copy files back and forth

Also very handy for installer scripts

"""

import os
import socket
import distutils.dir_util
import tempfile
import getpass

import config
import remote_shell
import utils
import logger

import pdb

debug = False

class buildenv:

        def __init__(self, username="", hostname="", root_dir="", lock_filename="", target_command_prefix="", arch_change_path="", env=config.env_vars, my_logger="", login_mode='ssh', copy_mode='scp', exec_mode='ssh'):

		self.login_mode=login_mode
		self.copy_mode=copy_mode
		self.exec_mode=exec_mode

		# Only used by execute for now (for location of launch_process.py)
		self.build_location = env['build_location']

		# buildenv is on a remote host instead of a local one
		if hostname: 
			self.hostname = hostname

		else:
			self.login_mode = 'local'
			self.copy_mode = 'local'
			self.exec_mode = 'local'

			self.hostname = socket.gethostname()

		if username:
			self.username = username
		else:
			# portable way to do this? (doesn't work from install-deps?  What's going on)?
			#self.username = os.getlogin()
			# testing
			#self.username = "wberrier"
			self.username = "builder"
			#self.username = getpass.getuser()


		# Custom identifier to use at various places
		self.uid = "%s@%s:%s" % (self.username, self.hostname, root_dir)

		# Host lock filename
		if lock_filename:
			self.host_lock_filename = lock_filename
		else:
			self.host_lock_filename = self.uid

		# Client lock filename
		self.client_lock_filename = self.build_location + os.sep + "locked"

                # Optional...
                self.root_dir = root_dir
                self.env = env

                self.target_command_prefix = target_command_prefix

		# Optional command to run to prepend executing the shell.  suse x86_64 has 'linux32', and sles s390x has 's390'
		#  allows 32bit jails on 64bit hosts
		self.arch_change_path = arch_change_path

		# Add some things into the 'env' map
                self.env['local_tar_path'] = config.tar_path

		# initialize objects for later
		self.modes = {}
		self.modes['ssh'] = remote_shell.ssh(username=username, hostname=hostname, env=self.env, my_logger=my_logger)
		self.modes['scp'] = remote_shell.scp(username=username, hostname=hostname, env=self.env, my_logger=my_logger)
		self.modes['smbclient'] = remote_shell.smbclient(username=username, hostname=hostname, env=self.env, my_logger=my_logger)
		self.modes['local'] = remote_shell.local(username=username, hostname=hostname, env=self.env, my_logger=my_logger)

		self.logger = my_logger

		# chroot options
		if root_dir:
			self.root_dir_options = "sudo -H %s %s sudo -H -u %s" % (env['chroot_path'], self.root_dir, self.username)
		else:   self.root_dir_options = ""

		# Set flag so we don't copy over and over for execute_command
		self.exec_util_files_copied = False

		# Keep track of dirs we create so it doesn't get done over and over
		self.created_dest_dirs = {}

		# empty logger to use at various places
		self.empty_logger = logger.Logger(config.devnull, print_screen=0)

		# Filenames for process jobs
		self.interrupted_file = self.build_location + os.sep + 'interrupted'
		self.pgkill_file = self.build_location + os.sep + 'pgid_kill'

	def login(self, mode=""):

		if not mode:
			mode = self.login_mode

		# TODO: the old code didn't call a shell when root_dir wasn't set (does that matter?)
		command = "%s %s %s %s" % (self.arch_change_path, self.root_dir_options, self.env['shell_path'], "-l")

		mode = self.modes[mode].login(command)

	def execute_command(self, command, working_dir="", mode="", exec_as_root=False, output_timeout=0, max_output_size=0, terminate_reg="", env={}, my_logger="", interruptable=True):
		"""setting interruptable to False is for internal and really important commands (ie: killing rpm installs/removes could cause havoc)  Using that flag doesn't write a pgid file"""

		if not working_dir:
			working_dir = self.build_location

		if not my_logger:
			my_logger = self.logger

		if not mode:
			mode = self.exec_mode

		if exec_as_root:
			sudo_opts = "sudo"
		else:   sudo_opts = ""

		if not env:
			env = self.env

		# If true, but no filename passed in, use this default filename
		if interruptable == True:
			interruptable = self.pgkill_file

		# launch process options. pass everything through launch process, and have it save the pgid to enable process interruptions
		# TODO: this doesn't play nicely with local commands, because this code is in the process group.  
		#  We need the local execute to be in a different process group for this to work
		launch_options = ""
		if output_timeout:
			launch_options += " --output_timeout=%s" % output_timeout
		if max_output_size:
			launch_options += " --max_output_size=%s" % max_output_size
		if terminate_reg:
			launch_options += " --terminate_reg=%s" % terminate_reg
		if working_dir:
			launch_options += " --working_dir=%s" % working_dir
		if interruptable:
			launch_options += " --interruptable=%s" % interruptable

		# Build environment string to pass to launch_process
		if env:
			items = []
			for k,v in env.iteritems():
				items.append("%s=%s" % (k,v))
			launch_options += " --env=\\\"%s\\\"" % ",".join(items)

		# Surround command with escaped double quotes in order to run multiline commands
		# TODO: Would it be better to execute this as 'remote code' instead?  (ie: remote is win32)
		command = "%s/launch_process.py --kill_process_group %s \\\"%s\\\" " % (self.build_location, launch_options, command)

		# Copy the necessary files for launch_process
		# cache this so it's not done every time
		if not self.exec_util_files_copied:
			self.copy_to([ config.packaging_dir + "/../pyutils/utils.py", config.packaging_dir + "/../pyutils/launch_process.py" ], self.build_location)
			self.exec_util_files_copied = True

		# Double quotes are very meticulous
		command = '%s %s %s %s "%s %s %s"' % (self.arch_change_path, self.root_dir_options, self.env['shell_path'], "-c",  self.target_command_prefix, sudo_opts, command)

		return self.modes[mode].execute_command(command, my_logger=my_logger)

	def execute_code(self, code, working_dir="", interpreter="", exec_as_root=False, output_timeout=0, max_output_size=0, terminate_reg="", env={}, my_logger="", interruptable=True):
		""" interpreter can be anything that works... mcs *.cs; mono, perl, python, etc... """

                if not my_logger:
			my_logger = self.logger

		# Default to shell code, but can be overwritten
		if not interpreter:
			interpreter = self.env['shell_path']

		# get code as a string if a file was passed in
		if os.path.isfile(code):
			fd = open(code)
			code = fd.read()
			fd.close()

		# Prepare a temp file to copy over
		fd, code_filename = tempfile.mkstemp(prefix='monobuild')
		file_basename = os.path.basename(code_filename)
		# Hrm... documentation says fd is a file object, but it's an integer.  Open manually
		fd = open(code_filename, 'w')
		fd.write(code)
		fd.close()

		# Make sure file is world readable, because our uid's change over ssh and inside chroot envs
		os.chmod(code_filename, config.data_perms)

		self.copy_to(code_filename, self.build_location)

		# Pass these args on
		args = {}
		args['exec_as_root'] = exec_as_root
		args['output_timeout'] = output_timeout
		args['max_output_size'] = max_output_size
		args['terminate_reg'] = terminate_reg
		args['env'] = env
		args['my_logger'] = my_logger
		args['working_dir'] = working_dir
		args['interruptable'] = interruptable

		if debug: print "* Executing code: " + code

		command = "%s %s" % (interpreter, self.build_location + os.sep + file_basename)
		code, output = self.execute_command(command, **args)

		# Clean up locally (and remote?)
		os.remove(code_filename)

		return code, output

	def make_path(self, dir, mode=""):
		"""Create a path
			This must be implemented in the lower layers since execute_* depend on it"""
		if not mode:
			mode = self.exec_mode

		# Add to the list if it's not there
		if not self.created_dest_dirs.has_key(dir):
			self.created_dest_dirs[dir] = self.modes[mode].make_path(self.root_dir + dir)

		return self.created_dest_dirs[dir]

        def remove_path(self, dir):
		"""Remove a path.  Since no internal functions depend on this, it can be a higher layer function"""

		remove_path_code = """
import os
import shutil

path = '%s'

if os.path.exists(path):
	# Newer versions of python's rmtree will remove files, but not all versions
	if os.path.isdir(path):
		shutil.rmtree(path)
	else:
		os.unlink(path)
""" % dir

		# Remove from listing so if we try to create again, it doesn't get skipped
		if self.created_dest_dirs.has_key(dir):
			self.created_dest_dirs.pop(dir)

		return self.execute_code(remove_path_code, interpreter=self.env['python_path'], interruptable=False)

        def copy_to(self, src, dest, compress=True, mode=""):

                if not mode:
                        mode = self.copy_mode

		# Convert to array if it's a string
		if src.__class__ == str:
			src = [ src ]

		# bail out if there are no files to copy
		if not len(src):
			print "No files to copy..."
			return 0, ""

		## Make sure it exists (turns into circular recursion at this point)
		self.make_path(dest)

		return self.modes[mode].copy_to(src, self.root_dir + dest, compress=compress)


        def copy_from(self, src, dest, compress=True, mode=""):

                if not mode:
                        mode = self.copy_mode

		# Convert to array if it's a string
		if src.__class__ == str:
			src = [ src ]

		# append root_dir to entries in src
		new_src = []
		for i in src:
			new_src.append(self.root_dir + i)
		src = new_src

		# bail out if there are no files to copy
		if not len(src):
			print "No files to copy..."
			return 0, ""

                return self.modes[mode].copy_from(src, dest, compress=compress)

	def interrupt(self):
		"""Write interrupted file flag, read pgid_kill file, and blow process group away!"""

		flag_code = """
import os

path = '%s'

fd = open(path, 'w')
fd.write("")
fd.close()""" % self.interrupted_file

		(code, output) = self.execute_code(flag_code, interpreter=self.env['python_path'], interruptable=False)

		if code:
			return (code, output)

		kill_code = """
import os
import signal
import sys

path = '%s'
client_lock = '%s'

if not os.path.exists(path):
	if os.path.exists(client_lock):
		print "Client is busy and uninterruptable, try again in a few minutes"
		sys.exit(1)
	print "Client is not running an interruptable command, exiting..."
	print "  (it could be running an non-interruptable command, but the client isn't locked)"
	sys.exit(0)


fd = open(path)
pgid = int(fd.read())
fd.close()
os.unlink(path)

# Kill the process group
print "Killing process group: %%d" %% pgid
try:
	os.kill(-pgid, signal.SIGKILL)
except OSError:
	print "Error killing process group %%d (already gone?)" %% pgid
	sys.exit(1)
""" % (self.pgkill_file, self.client_lock_filename)

		return self.execute_code(kill_code, interpreter=self.env['python_path'], interruptable=False)
	

	# TODO: use os level locking here
	def lock_env(self):
		fd = open(self.host_lock_filename, 'w')
		fd.write("")
		fd.close()

		# also put file in jail to signify that it's locked (method not perfect, but should be good enough)
		#self.execute_command("touch %s" % self.client_lock_filename)

		lock_code = """
path = '%s'

fd = open(path, 'w')
fd.write("")
fd.close()

""" % self.client_lock_filename

		self.execute_code(lock_code, interpreter=self.env['python_path'], interruptable=False)

		return True

	def unlock_env(self, clear_interrupt=False):
		if os.path.exists(self.host_lock_filename):
			os.unlink(self.host_lock_filename)
			host_ret = True
		else:
			print "unlock_env: host lockfile already removed"
			host_ret = False

		# also remove interrupt file if it is there
		if clear_interrupt:
			(ret, output) = self.remove_path(self.interrupted_file)
		(client_ret, output) = self.remove_path(self.client_lock_filename)

		# Return False on failure
		if host_ret or not client_ret:
			return True
		else:
			return False

	def is_locked(self):

		# Check host lockfile
		if os.path.exists(self.host_lock_filename):
			host_ret = True
		else:
			host_ret = False

		path_exists_code = """
import os
import sys

path = '%s'

if not os.path.exists(path):
	sys.exit(1)
""" % self.client_lock_filename

		(client_ret, output) = self.execute_code(path_exists_code, interpreter=self.env['python_path'], interruptable=False)

		# if host lock or client lock exists, we're locked
		if host_ret or not client_ret:
			return True
		else:
			return False

	def offline(self):

		# Run some arbitrary command that will always return true
		(code, output) = self.execute_code("print 'online'", interpreter=self.env['python_path'], my_logger=self.empty_logger, interruptable=False)

		if code: return 1
		else:    return 0


