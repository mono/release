
"""
Various routines to assist in connection over ssh with python
Also handles chroots into jails, aleviating running ssh inside the jail

Routines to execute commands inside of jails,
as well as log into them, and copy files back and forth

Also very handy for installer scripts

TODO
-permaconnection
"""

import utils
import os.path
import os
import string

import pdb

class init:
	
	def __init__(self, target_host, print_output=1, jaildir="", chroot_path="/usr/sbin/chroot", remote_tar_path="tar", local_tar_path="tar", target_command_prefix="", execute_command=1, print_command=0, logger=""):

		self.target_host = target_host

		# Optional...
		self.print_output = print_output
		self.jaildir = jaildir
		self.chroot_path = chroot_path
		self.remote_tar_path = remote_tar_path
		self.local_tar_path = local_tar_path
		self.target_command_prefix = target_command_prefix
		self.logger = logger

		# Options for debugging
		self.execute_command=execute_command
		self.print_command=print_command

		#  quiet
		# Ignore host checks, and blowfish might be faster and less cpu intensive
		# Batchmode: don't prompt for password, quickly detect unavailable hosts
		#self.options = '-q -o "StrictHostKeyChecking no" -o "Cipher blowfish" '
		# Let's be a little more verbose (especially with scp)... hmm... didn't work
		self.options = '-o "StrictHostKeyChecking no" -o "Cipher blowfish" '

		# Check to see if we're using a jail
		if self.jaildir:
			self.chroot_options = " sudo -H %s %s $SHELL" % (self.chroot_path, self.jaildir)
		else:
			self.chroot_options = ""


		# Possilbly TODO later...
		self.conn_in = ""
		self.conn_out = ""

	# Args: command to execute, and option to print_output
	#  Will always return output
	# NOTE: In order to use backticks, you must escape them in the string you pass in
	def execute(self, command, capture_stderr=1, terminate_reg=""):
		"""Args, command string to execute.  Option args: capture_stderr, and terminate_reg.

		capture_stderr is 1 or 0 (Currently unimplemented)
		See doc for utils.launch_process for description of terminate_reg. """

		if self.target_command_prefix:
			command = self.target_command_prefix + command

		# Quoting very importand here: double quotes
		command = '"' + command + '"'

		if self.jaildir:
			# Not sure what the most portable flag -c is (executing a command in the shell)
			#  The quoting here is very meticulous, single around outer sudo command
			execute_options = "'" + self.chroot_options + ' -c ' + command + "'"
		else:
			execute_options = command
	
		command_string = "ssh -o \"BatchMode yes\" %s %s %s " % (self.options, self.target_host, execute_options)

		code = 0
		output = ""

		if self.print_command: self.log("Executing %s" % command_string)

		if self.execute_command:
			(code, output) = utils.launch_process(command_string, print_output=self.print_output, terminate_reg=terminate_reg, logger=self.logger)

		return code, output

	def interactive_login(self):
		execute_options = " "
		if self.jaildir:
			# Not sure what the most portable flag for this is...
			execute_options = "'" + self.chroot_options + ' -i' + "'"
		command_string =  "ssh -t %s %s %s" % (self.options, self.target_host, execute_options)
		os.system(command_string)


	# Copy to jail
	def copy_to(self, src, dest, compress=1, mode='scp'):
		"""Args: src (string or list), dest, Returns: (exit_code, output).

		Optional args: compress=0 or 1, mode=tar or scp.
		Note, in scp mode, recursive is on by default
		src can be a string or a list of strings"""

		if compress: compress_option = ' -o "Compression yes" '
		else:	     compress_option = ""

		# Concatenate for src if it's a list
		if src.__class__ == list:
			src = string.join(src, " ")

		if mode == 'scp':
			command = "scp -r %s %s %s:%s%s" % (self.options + compress_option, src, self.target_host, self.jaildir, dest)

		elif mode == 'tar':
			# Note: the -f - option to the remote tar is required for solaris tar, otherwise it tries to read from a tape
			if self.jaildir:
				dest = self.jaildir + os.sep + dest
		        command = "%s -pc %s | ssh %s %s 'cd %s ; %s -pvxf - ' " % (self.local_tar_path, src, self.options + compress_option, self.target_host, dest, self.remote_tar_path )
		else:
			self.log("Invalid copy_to mode: %s" % mode)
			sys.exit(1)

		if self.print_output: self.log(command)
		return utils.launch_process(command, print_output=self.print_output)
		

	def copy_from(self, src, dest, compress=1, mode='scp'):
		"""Args: (src (string or list), dest) Returns: (exit_code, output).

		Optional args: compress=0 or 1, mode=tar or scp.
		# tar mode is default because it handles symbolic links and preserving time stamps, unlike scp.
		#  I guess I could also use zip/unzip... oh well
		# Note: tar mode appends src path of file to dest (just the way tar works)"""

		# Convert to array if it's a string
		if src.__class__ == str:
			src = [ src ]

		if compress: compress_option = ' -o "Compression yes" '
		else:	     compress_option = ""

		files = ""

		if mode == 'scp':
			for file in src:
				files += " %s:%s%s " % (self.target_host, self.jaildir, file)
			command = "scp -r %s %s %s" % (self.options + compress_option, files, dest)

		elif mode == 'tar':
			for file in src:
				files += " %s%s " % (self.jaildir, file)
			tar_dir_options = ""
			if self.jaildir:
				tar_dir_options = "-C %s" % os.path.dirname(self.jaildir)
				
			# Note: the -f - option to the remote tar is required for solaris tar, otherwise it tries to read from a tape
		        command = "cd %s; ssh %s %s ' %s %s -pcf - %s ' | %s -pvxf - " % (dest, self.options + compress_option, self.target_host, self.remote_tar_path, tar_dir_options, files, self.local_tar_path )

		else:
			self.log("Invalid copy_from mode: %s" % mode)
			sys.exit(1)

		if self.print_output: self.log(command)
		return utils.launch_process(command, print_output=self.print_output)

	def log(self, message):
		if self.logger: self.logger.log(message)
		else: print message


	# Extra future bonus features...
	#  Not sure this stuff would ever be useful...
	# Only gets called once, exatblish handle to an ssh connection
	#  Implementing this would probably only work on unix... python on windows doesn't do return codes when opening pipes for input and output to a process.  Could always do some funky shell stuff to get the output... hmmm...
	# Actually, I can't think of a good reason for permaconnection... especially with restoring a clean environment
	def connect(self):
		"""Not working..."""
		# Set up connection to the host and set the correct stuff in the object
		command_string = "ssh -o \"BatchMode yes\" -T %s %s 2>&1 " % (self.options, self.target_host)

		(self.conn_in, self.conn_out) = os.popen2(command_string)
		

	# Check to see if there's a connection, if not, run the command, returning the output, leave connection open
	def run_command(self, command, print_output=1):
		"""Not working..."""

		# Connect if we haven't already
		if not (self.conn_in and self.conn_out):
			self.connect()

		# TODO: Execute inside jail options

		self.conn_in.write(command + ' && echo "\n@@SSH_UTIL_EXIT_CODE@@:$?\n')

		collected = []
		code = -1

		exit_reg = re.compile('@@SSH_UTIL_EXIT_CODE@@:(?P<exit>\d+)')

		while(1):
			line = self.conn_out.readline()
			if not line: break
			if print_output:
				print line,
				sys.stdout.flush()
				# This doesn't work on macosx... ?
				#process.flush()
			collected += line

			# Check for a line containing an exit code
			if exit_reg.search(line):
				code = exit_reg.groupindex['exit']
				break

		return code, "".join(collected).rstrip()


