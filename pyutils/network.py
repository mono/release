"""
simple routines to copy files and execute commands

"""

import utils
import os.path
import os
import string
import config
import re


class ssh:

	def __init__(self, username, hostname, env="", logger=""):
		# Ignore host checks, and blowfish might be faster and less cpu intensive
		self.options = '-o "BatchMode yes" -o "StrictHostKeyChecking no" -o "Cipher blowfish" '

		self.username = username
		self.hostname = hostname
		self.logger = logger

		# Get tar paths (required from copy to/from)
		if env and env.has_key('tar_path'):
			self.remote_tar_path = env['tar_path']
		else:   self.remote_tar_path = 'tar'

		self.local_tar_path = config.tar_path


        def login(self, command):
		command = "ssh -t %s %s@%s %s" % (self.options, self.username, self.hostname, command)
		# Can't use utils.launch_process here because we need an interactive terminal
                return os.system(command)

        def execute_command(self, command, logger=""):

		# Escape these so they get interpolated by the remote machine
		command = command.replace('$', '\$')

		# Put single quotes around the command so the whole command gets passed over ssh
		# (must use single quotes here since command may have double quotes (shell allows double quotes inside of single, without escaping)
		command = "ssh %s %s@%s '%s'" % (self.options, self.username, self.hostname, command)
                return utils.launch_process(command, logger=logger)

	def copy_to(self, src, dest, compress=True, logger=""):
		"""Args: src (list of strings), dest, Returns: (exit_code, output).
		Optional args: compress=True of False"""

		src = " ".join(src)

		if compress:
			compress_option = "z"
			# This was causing problems with copy to the windows machine... hmm... ? (ssh problem?  Would explain the s390 problems)
			#compress_option = "j"
		else:
			compress_option = ""

		# Note: the -f - option to the remote tar is required for solaris tar, otherwise it tries to read from a tape
		command = "%s -%spc %s | ssh %s %s@%s 'cd %s ; %s -%spvxf - ' " % (self.local_tar_path, compress_option, src, self.options, self.username, self.hostname, dest, self.remote_tar_path, compress_option )
		return utils.launch_process(command, logger=logger)

	def copy_from(self, src, dest, compress=True, logger=""):
                """Args: (src (list), dest) Returns: (exit_code, output).

                Optional args: compress=0 or 1
                # tar mode handles symbolic links and preserving time stamps, unlike scp.
                #  I guess I could also use zip/unzip... oh well (What does this mean?)
                # Note: tar mode appends src path of file to dest (just the way tar works)"""

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

                return utils.launch_process(command, logger=logger)


class scp:

	def __init__(self, username, hostname, env="", logger=""):
		# Ignore host checks, and blowfish might be faster and less cpu intensive
		self.options = '-o "StrictHostKeyChecking no" -o "Cipher blowfish" '

		self.username = username
		self.hostname = hostname
		self.logger = logger

	def copy_to(self, src, dest, compress=True, logger=""):
		"""Args: src (list of strings), dest, Returns: (exit_code, output).

		Optional args: compress=0 or 1 (but doesn't actually do anything in ssh protocol 2... oh well
		Note, in scp mode, recursive is on by default"""

		src = " ".join(src)

		if compress:
			# CompressionLevel only works for protocol 1... (bummer)
			compress_option = ' -o "Compression yes" -o "CompressionLevel 9" '
		else:
			compress_option = ""

		command = "scp -r %s %s %s@%s:%s" % (self.options + compress_option, src, self.username, self.hostname, dest)

		return utils.launch_process(command, logger=logger)

	def copy_from(self, src, dest, compress=True, logger=""):
		"""Args: (src (list), dest) Returns: (exit_code, output).

		Optional args: compress=0 or 1, mode=tar or scp.
		#  I guess I could also use zip/unzip... oh well (??)"""

		if compress:
			# CompressionLevel only works for protocol 1... (bummer)
			compress_option = ' -o "Compression yes" -o "CompressionLevel 9" '
		else:
			compress_option = ""

		files = ""

		for file in src:
			files += " %s@%s:%s " % (self.username, self.hostname, file)
		command = "scp -r %s %s %s" % (self.options + compress_option, files, dest)

		return utils.launch_process(command, logger=logger)

# TODO: implement code for this
# Needs to be tested
class smbclient:
	
	def __init__(self, username, hostname, env="", logger=""):

		self.username = username
		self.hostname = hostname
		self.logger = logger


	# Copy to jail
	def copy_to(self, src, dest, compress=True, logger=""):
		"""Args: src (list), dest, Returns: (exit_code, output)."""

		# this is the original 'scp' mode
		# fixed: You can't mput files outside the current local dir (going to have to chdir to each dir and issue separate smbclient commands)
		# Kinda ugly, but it works!
		dest = dest.replace(self.SMB_ROOT, '')
		current_dir = os.getcwd()
		command = ""
		for file in src:
			dir = os.path.dirname(file)
			filename = os.path.basename(file)

			if dir: dir_cmd = "cd %s;" % dir
			else: dir_cmd = ""

			command += "%s smbclient //%s/%s -A %s -U %s -D %s -c 'prompt; recurse; mput %s' ; cd %s ;" % (dir_cmd, self.host, self.SMB_SHARE, config.smb_passfile, self.user, dest, filename, current_dir)

		# This is for 'tar' mode:
		# (But doesn't have compression, only useful if not using tar over ssh)
		#command = "%s -spc %s | smbclient //%s/%s -A %s -U %s -D %s -Trqx -" % (self.local_tar_path, src, self.host, self.SMB_SHARE, config.smb_passfile, self.user, dest)


		return utils.launch_process(command, print_output=self.print_output)
		
	def copy_from(self, src, dest, compress=True, logger=""):
		"""Args: (src (list), dest) Returns: (exit_code, output)."""


		# fixed: You can't mput files outside the current local dir (going to have to chdir to each dir and issue separate smbclient commands)
		# Kinda ugly, but it works!
		current_dir = os.getcwd()
		command = ""
		for file in src:
			dir = os.path.dirname(file)
			dir = dir.replace(self.SMB_ROOT, '')
			filename = os.path.basename(file)

			command += "cd %s; smbclient //%s/%s -A %s -U %s -D %s -c 'prompt; recurse; mget %s' ; cd %s ;" % (dest, self.host, self.SMB_SHARE, config.smb_passfile, self.user, dir, filename, current_dir)


		return utils.launch_process(command, print_output=self.print_output)


