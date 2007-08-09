"""
simple routines to copy files and execute commands using several different methods
"""

import os.path
import os
import re
import glob
import shutil

import config
import utils

debug = False
ssh_options = '-o "BatchMode yes" -o "StrictHostKeyChecking no" -o "Cipher blowfish" -o "ConnectTimeout 10" '

class ssh:

	def __init__(self, username, hostname, env="", my_logger=""):
		# Ignore host checks, and blowfish might be faster and less cpu intensive
		# Add connecttimeout so we don't wait forever for a host that is down
		self.options = ssh_options

		self.username = username
		self.hostname = hostname
		self.logger = my_logger

		# Get tar paths (required from copy to/from)
		if env and env.has_key('tar_path'):
			self.remote_tar_path = env['tar_path']
		else:   self.remote_tar_path = 'tar'

		self.local_tar_path = config.tar_path


        def login(self, command):
		command = "ssh -t %s %s@%s %s" % (self.options, self.username, self.hostname, command)
		# Can't use utils.launch_process here because we need an interactive terminal
		if debug: print "* Executing: " + command
                return os.system(command)

        def execute_command(self, command, my_logger=""):

		if not my_logger:
			my_logger = self.logger

		# Escape these so they get interpolated by the remote machine
		command = command.replace('$', '\$')

		# Put single quotes around the command so the whole command gets passed over ssh
		# (must use single quotes here since command may have double quotes (shell allows double quotes inside of single, without escaping)
		command = "ssh %s %s@%s '%s'" % (self.options, self.username, self.hostname, command)
		if debug: print "* Executing: " + command
                return utils.launch_process(command, my_logger=my_logger)

	def copy_to(self, src, dest, compress=True, my_logger=""):
		"""Args: src (list of strings), dest, Returns: (exit_code, output).
		Optional args: compress=True of False"""

		if not my_logger:
			my_logger = self.logger

		src = " ".join(src)

		if compress:
			compress_option = "z"
			# This was causing problems with copy to the windows machine... hmm... ? (ssh problem?  Would explain the s390 problems)
			#compress_option = "j"
		else:
			compress_option = ""

		# Note: the -f - option to the remote tar is required for solaris tar, otherwise it tries to read from a tape
		command = "%s -%spc %s | ssh %s %s@%s 'cd %s ; %s -%spvxf - ' " % (self.local_tar_path, compress_option, src, self.options, self.username, self.hostname, dest, self.remote_tar_path, compress_option )
		if debug: print "* Executing: " + command
		return utils.launch_process(command, my_logger=my_logger)

	def copy_from(self, src, dest, compress=True, my_logger=""):
                """Args: (src (list), dest) Returns: (exit_code, output).

                Optional args: compress=0 or 1
                # tar mode handles symbolic links and preserving time stamps, unlike scp.
                #  I guess I could also use zip/unzip... oh well (What does this mean?)
                # Note: tar mode appends src path of file to dest (just the way tar works)"""

		if not my_logger:
			my_logger = self.logger

                if compress:
                        # CompressionLevel only works for protocol 1... (bummer)
                        compress_option = "z"
                else:   
                        compress_option = ""

                files = ""

		# TODO: this method doesn't work (but it's not used)
		tar_dir_options = ""
		#tar_dir_options = "-C %s" % os.path.dirname(self.root_dir)

		# Note: the -f - option to the remote tar is required for solaris tar, otherwise it tries to read from a tape
		command = "cd %s; ssh %s %s@%s ' %s %s -%spcf - %s ' | %s -%spvxf - " % (dest, self.options, self.username, self.hostname, self.remote_tar_path, tar_dir_options, compress_option, files, self.local_tar_path, compress_tar_option )
		if debug: print "* Executing: " + command

                return utils.launch_process(command, my_logger=my_logger)

	def make_path(self, dir):
		"""Args: (dir) Returns: (mkdir exit code and output)."""

		return self.execute_command("mkdir -p -m777 " + dir)


class scp:

	def __init__(self, username, hostname, env="", my_logger=""):
		# Ignore host checks, and blowfish might be faster and less cpu intensive
		self.options = ssh_options

		self.username = username
		self.hostname = hostname
		self.logger = my_logger

	def copy_to(self, src, dest, compress=True, my_logger=""):
		"""Args: src (list of strings), dest, Returns: (exit_code, output).

		Optional args: compress=0 or 1 (but doesn't actually do anything in ssh protocol 2... oh well
		Note, in scp mode, recursive is on by default"""

		if not my_logger:
			my_logger = self.logger

		src = " ".join(src)

		if compress:
			# CompressionLevel only works for protocol 1... (bummer)
			compress_option = ' -o "Compression yes" -o "CompressionLevel 9" '
		else:
			compress_option = ""

		command = "scp -r %s %s %s@%s:%s" % (self.options + compress_option, src, self.username, self.hostname, dest)
		if debug: print "* Executing: " + command

		return utils.launch_process(command, my_logger=my_logger)

	def copy_from(self, src, dest, compress=True, my_logger=""):
		"""Args: (src (list), dest) Returns: (exit_code, output).

		Optional args: compress=0 or 1, mode=tar or scp.
		#  I guess I could also use zip/unzip... oh well (??)"""

		if not my_logger:
			my_logger = self.logger

		if compress:
			# CompressionLevel only works for protocol 1... (bummer)
			compress_option = ' -o "Compression yes" -o "CompressionLevel 9" '
		else:
			compress_option = ""

		files = ""

		for file in src:
			files += " %s@%s:%s " % (self.username, self.hostname, file)
		command = "scp -r %s %s %s" % (self.options + compress_option, files, dest)
		if debug: print "* Executing: " + command

		return utils.launch_process(command, my_logger=my_logger)

# TODO: implement code for this
# Needs to be tested
class smbclient:
	
	def __init__(self, username, hostname, env="", my_logger=""):

		self.username = username
		self.hostname = hostname
		self.logger = my_logger

		# TODO:
		#self.SMB_SHARE = env['SMB_SHARE']

	# Copy to jail
	def copy_to(self, src, dest, compress=True, my_logger=""):
		"""Args: src (list), dest, Returns: (exit_code, output)."""

		if not my_logger:
			my_logger = self.logger

		# this is the original 'scp' mode
		# fixed: You can't mput files outside the current local dir (going to have to chdir to each dir and issue separate smbclient commands)
		# Kinda ugly, but it works!
		current_dir = os.getcwd()
		command = ""
		for file in src:
			dir = os.path.dirname(file)
			filename = os.path.basename(file)

			if dir: dir_cmd = "cd %s;" % dir
			else: dir_cmd = ""

			command += "%s smbclient //%s/%s -A %s -U %s -D %s -c 'prompt; recurse; mput %s' ; cd %s ;" % (dir_cmd, self.hostname, self.SMB_SHARE, config.smb_passfile, self.username, dest, filename, current_dir)

		# This is for 'tar' mode:
		# (But doesn't have compression, only useful if not using tar over ssh)
		#command = "%s -spc %s | smbclient //%s/%s -A %s -U %s -D %s -Trqx -" % (self.local_tar_path, src, self.host, self.SMB_SHARE, config.smb_passfile, self.user, dest)


		return utils.launch_process(command, my_logger=my_logger)
		
	def copy_from(self, src, dest, compress=True, my_logger=""):
		"""Args: (src (list), dest) Returns: (exit_code, output)."""

		if not my_logger:
			my_logger = self.logger

		# fixed: You can't mput files outside the current local dir (going to have to chdir to each dir and issue separate smbclient commands)
		# Kinda ugly, but it works!
		current_dir = os.getcwd()
		command = ""
		for file in src:
			dir = os.path.dirname(file)
			if not dir: dir = "."
			filename = os.path.basename(file)

			command += "cd %s; smbclient //%s/%s -A %s -U %s -D %s -c 'prompt; recurse; mget %s' ; cd %s ;" % (dest, self.hostname, self.SMB_SHARE, config.smb_passfile, self.username, dir, filename, current_dir)


		return utils.launch_process(command, my_logger=my_logger)


class local:
	"""Class implementing the same interface as a copyexec object, but the jail or machine is on the host machine"""

	def __init__(self, username, hostname, env="", my_logger=""):
                self.username = username
                self.hostname = hostname
                self.logger = my_logger

	def login(self, command):

		os.system(command)

	def execute_command(self, command, my_logger=""):

		if not my_logger:
			my_logger = self.logger

		# TODO: execute this under a new pgid so only it gets killed, not us all
		# check http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
		# Or, put that code in the utils.launch_process routine, which would make it more robust
		return utils.launch_process(command, my_logger=my_logger)

	# For local copyings, you can use the same commands (scp, tar), just not over ssh (scp?)
	# TODO: But how to know what to use... scp or tar, because they behave differently
	# (could add a parameter to the copy to/from definition to distinguish between the two, if this
	#  becomes necessary)
	# difference: # Note: tar mode appends src path of file to dest (just the way tar works)"""
	# tar mode handles symbolic links and preserving time stamps, unlike scp.

        def copy_to(self, src, dest, compress=True, my_logger=""):
		results = []
		# Glob each of the src filesnames to allow wildcards
		new_src = []
		for i in src:
			new_src += glob.glob(i)
		src = new_src

		for i in src:

			# Don't copy if src and dest are the same (really for execute_code)
			if os.path.abspath(os.path.normpath(i)) == os.path.abspath(os.path.normpath(dest + os.sep + os.path.basename(i))):
				pass
			elif os.path.isdir(i):
				# add basename of the src to dest
				#  This is to match behavior of scp
				temp_dest = dest + os.sep + os.path.basename(i)
				results += distutils.dir_util.copy_tree(i, temp_dest, preserve_symlinks=True)
			else:
				shutil.copy2(i, dest)
				results += [dest + os.sep + i]

		return 0, "\n".join(results)

        def copy_from(self, src, dest, compress=True, my_logger=""):
		""" No need to duplicate this, since we're on a local machine, use the same method"""
		return self.copy_to(src, dest, compress=compress, my_logger=my_logger)

	def make_path(self, dir):
		"""Create a path"""

		error = 0
		try:
			distutils.dir_util.mkpath(dir)
			os.chmod(dir, 0777)
		except:
			error = 1
		return error
