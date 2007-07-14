"""
Routines to execute commands locally, inside of jails, remotely in jails
as well as log into them, and copy files back and forth

Also very handy for installer scripts

"""

import os
import config
import network
import utils
import socket
import distutils.dir_util
import shutil
import glob
import tempfile
import getpass

import logger

import pdb

class buildenv:

        def __init__(self, username="", hostname="", root_dir="", lock_filename="", target_command_prefix="", env=config.env_vars, logger="", login_mode='ssh', copy_mode='scp', exec_mode='ssh'):

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

		if lock_filename:
			self.lock_filename = lock_filename
		else:
			self.lock_filename = self.uid

                # Optional...
                self.root_dir = root_dir
                self.env = env

                self.target_command_prefix = target_command_prefix

		# Add some things into the 'env' map
                self.env['local_tar_path'] = config.tar_path

		# initialize objects for later
		self.modes = {}
		self.modes['ssh'] = network.ssh(username=username, hostname=hostname, env=self.env, logger=logger)
		self.modes['scp'] = network.scp(username=username, hostname=hostname, env=self.env, logger=logger)
		self.modes['smbclient'] = network.smbclient(username=username, hostname=hostname, env=self.env, logger=logger)
		self.modes['local'] = local(username=username, hostname=hostname, env=self.env, logger=logger)

		self.logger = logger

		# chroot options
		if root_dir:
			self.root_dir_options = "sudo -H %s %s sudo -H -u %s" % (env['chroot_path'], self.root_dir, self.username)
		else:   self.root_dir_options = ""

		# Set flag so we don't copy over and over for execute_command
		self.exec_util_files_copied = False


	def login(self, mode=""):

		if not mode:
			mode = self.login_mode

		# TODO: the old code didn't call a shell when root_dir wasn't set (does that matter?)
		command = "%s %s %s" % (self.root_dir_options, self.env['shell_path'], "-l")

		mode = self.modes[mode].login(command)

	def execute_command(self, command, working_dir="", mode="", exec_as_root=False, output_timeout=0, max_output_size=0, terminate_reg="", env={}, logger=""):

		if not working_dir:
			working_dir = self.build_location

		if not logger:
			logger = self.logger

		if not mode:
			mode = self.exec_mode

		if exec_as_root:
			sudo_opts = "sudo"
		else:   sudo_opts = ""

		if not env:
			env = self.env

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
		command = '%s %s %s "%s %s %s"' % (self.root_dir_options, self.env['shell_path'], "-c",  self.target_command_prefix, sudo_opts, command)

		return self.modes[mode].execute_command(command, logger=logger)

	def execute_code(self, code, working_dir="", interpreter="", exec_as_root=False, output_timeout=0, max_output_size=0, terminate_reg="", env={}, logger=""):
		""" interpreter can be anything that works... mcs *.cs; mono, perl, python, etc... """

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
		args['logger'] = logger
		args['working_dir'] = working_dir

		command = "%s %s" % (interpreter, self.build_location + os.sep + file_basename)
		code, output = self.execute_command(command, **args)

		# Clean up locally (and remote?)
		os.remove(code_filename)

		return code, output

	def make_path(self, dir, mode=""):

		if not mode:
			mode = self.exec_mode

		return self.modes[mode].make_path(self.root_dir + os.sep + dir)

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

		# Make sure it exists
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

	def interrupt_command(self):
		pass
	

	# TODO: use os level locking here
	def lock_env(self):
		fd = open(self.lock_filename, 'w')
		fd.write("")
		fd.close()
		return True

	def unlock_env(self):
		if os.path.exists(self.lock_filename):
			os.unlink(self.lock_filename)
			return True
		else:
			print "Build environment already unlocked"
			return False

	def is_locked(self):
		return os.path.exists(self.lock_filename)

	def offline(self):
		old_logger = self.logger
		self.logger = logger.Logger(config.devnull, print_screen=0)

		# Run some arbitrary command that will always return true
		(code, output) = self.execute_command("ls")

		self.logger = old_logger

		if code: return 1
		else:    return 0


class local:
	"""Class implementing the same interface as a network object, but the jail is or machine is on the host machine"""

	def __init__(self, username, hostname, env="", logger=""):
                self.username = username
                self.hostname = hostname
                self.logger = logger

	def login(self, command):

		os.system(command)

	def execute_command(self, command, logger=""):
		# TODO: execute this under a new pgid so only it gets killed, not us all
		# check http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
		# Or, put that code in the utils.launch_process routine, which would make it more robust
		return utils.launch_process(command, logger=logger)

	# For local copyings, you can use the same commands (scp, tar), just not over ssh (scp?)
	# TODO: But how to know what to use... scp or tar, because they behave differently
	# (could add a parameter to the copy to/from definition to distinguish between the two, if this
	#  becomes necessary)
	# difference: # Note: tar mode appends src path of file to dest (just the way tar works)"""
	# tar mode handles symbolic links and preserving time stamps, unlike scp.

        def copy_to(self, src, dest, compress=True, logger=""):
		results = []
		# Glob each of the src filesnames to allow wildcards
		new_src = []
		for i in src:
			new_src += glob.glob(i)
		src = new_src

		# seems os.path.normpath should do this, but it doesn't
		dest = dest.replace('//', '/')

		for i in src:

			i = i.replace('//', '/')

			# Don't copy if src and dest are the same (really for execute_code)
			if os.path.abspath(os.path.normpath(i)) == os.path.abspath(os.path.normpath(dest + os.sep + os.path.basename(i))):
				pass
			elif os.path.isdir(i):
				results += distutils.dir_util.copy_tree(i, dest, preserve_symlinks=True)
			else:
				shutil.copy2(i, dest)
				results += [dest + os.sep + i]

		return 0, "\n".join(results)

        def copy_from(self, src, dest, compress=True, logger=""):
		""" No need to duplicate this, since we're on a local machine, use the same method"""
		return self.copy_to(src, dest, compress=compress, logger=logger)

        def make_path(self, dir):
		"""Create a path"""

		error = 0
		try:
			distutils.dir_util.mkpath(dir)
		except:
			error = 1
		return error


