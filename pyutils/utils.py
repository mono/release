#!/usr/bin/env python

"""

utils.py

Various routines used in installer and packaging scripts

To include:

import utils
# If utils.py is not in the same dir
sys.path += [ '../pyutils' ] #or whatever path contains utils.py

"""

import sys
import os
import os.path
import shutil
import re
import tempfile
import string
import glob
import time
import calendar
import popen2
import signal
import fcntl

# Catch this error, and then die later on if the namespace isn't found
#  (Allows us to use launch_process without having python-devel rpm installed on SuSE type machines)
try:
	import distutils.dir_util
except ImportError:
	print "Missing distutils.dir_util..."


import pdb

# Full path to the rpmvercmp binary, maybe this could be done in python
#  So it's not arch specific
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
rpmvercmp_path = os.path.abspath(module_dir + "../rpmvercmp/rpmvercmp")

debug=0
KILLED_EXIT_CODE=-42

# Get vars out of shell scripts (def files)
def get_env_var(var_name, source):

	if not os.path.exists(source):
		print "get_env_var: File not found: %s" % source
		sys.exit(1)

        tmp_script = tempfile.mktemp()

        my_script = open(tmp_script, 'w')
        my_script.write(". %s\n" % source)
        my_script.write("echo ${%s[@]}\n" % var_name)
        my_script.close()

        (code, output) = launch_process("sh %s" % tmp_script, print_output=debug)

        os.unlink(tmp_script)

        return output
# Extract either tarball, rpm, or zip
def extract_file(filename, preserve_symlinks=0):
        print "Extracting: %s" % filename
        (root, ext) = os.path.splitext(filename)

        if ext ==  ".zip" or ext == ".exe":
                #print "Found zip!"
                (status, output) = launch_process("unzip -o %s" % filename, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:
                        print "Error unzipping file! %s" % filename
                        print "File is probably corrupt, removing"
                        os.remove(filename)
                        sys.exit(1)

        elif ext == ".rpm":
                #print "Found rpm!"
                tempdir = "___EXTRACT___"

                if os.path.exists(tempdir):
                        shutil.rmtree(tempdir)
                os.mkdir(tempdir)
                os.chdir(tempdir)

                command = "rpm2cpio %s | cpio -idv" % filename
                (status, output) = launch_process(command, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:

			# Weirdness for macosx...
			#  This is a huge hack, because rpm2cpio doesn't come with macosx...
			if re.compile('Unable to set file uid\/gid').search(output):
				# The files were extracted, it should be ok, try again
				(status, output) = launch_process(command, print_output=debug)
				if status:
					print "Error extracting rpm file: %s" % filename
					print output
					sys.exit(1)

			else:

				print "Error extracting rpm file: %s" % filename
				print output
				sys.exit(1)

                os.chdir("usr")
		distutils.dir_util.copy_tree(".", "../..", preserve_symlinks=preserve_symlinks)

                if status:
                        print "Error massaging files from rpm: %s" % filename
                        sys.exit(1)

                os.chdir("../..")
                shutil.rmtree(tempdir)

	# If it's a .tar.gz or tar.bz2
        elif (ext == ".gz" and re.compile('\.tar\.gz$').search(filename) ) or (ext == ".bz2" and re.compile('\.tar\.bz2$').search(filename) ):
                if ext == ".gz": flag = "z"
                if ext == ".bz2": flag = "j"

                #print "Found tarball!"
                (status, output) = launch_process("tar -%sxvpf %s" % (flag, filename), print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:
                        print "Error untarring file: %s" % filename
                        sys.exit(1)

	# If it's a gzipped solaris package
        elif ext == ".gz":
                tempdir = "___EXTRACT___"

                if os.path.exists(tempdir):
                        shutil.rmtree(tempdir)
                os.mkdir(tempdir)
                os.chdir(tempdir)

                (status, output) = launch_process("gunzip -c %s | pkgtrans /dev/stdin . all" % filename, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:
                        print "Error extracting solaris package file: %s" % filename
                        sys.exit(1)
		packagedir = glob.glob('*').pop()
                os.chdir(packagedir + os.sep + 'reloc')

		pkgmap = open('../pkgmap', 'r')

		# Fix up the symbolic links
		for line in pkgmap:
			# Matching example:
			#1 s none lib/libglib-2.0.so=libglib-2.0.so.0.200.3
			try: 
				(link, target) = re.compile('. . .*? (.*)=(.*)').search(line).groups()
				os.symlink(target, link)
			except AttributeError:
				pass

		distutils.dir_util.copy_tree(".", "../../..", preserve_symlinks=preserve_symlinks)

                os.chdir("../../..")
                shutil.rmtree(tempdir)

	else:
		print "Warning!!! Unable to extract file of type %s" % ext
		return

        return os.path.basename(filename)

# Download url into cache (Don't redownload if file exists)
def get_url(url,destination):

	filename = os.path.basename(url)

        # Download if not in cache
        if not os.path.exists(destination + os.sep + filename):
                print "Downloading: %s ..." % url
                command = "wget -c %s -O %s" % (url, destination + os.sep + filename)
                #print command
                (status, output) = launch_process(command, print_output=debug)


def substitute_parameters_in_file(file, qualifier, parameter_map):

        fd = open(file, 'r')
        text = fd.read()
        fd.close()

        if qualifier.match(text):
                print "Substituting: " + file
                text = substitute_parameters(text, parameter_map)

        fd = open(file, 'w')
        fd.write(text)
        fd.close()


# First arg: text
# Second arg, hash of key value pairs to swap in the text
# Note: keys can be regexs
def substitute_parameters(text, parameter_map):

        for regex in parameter_map.keys():
                # In the text, substitute the key with the value from the hash
                text = re.sub(regex, parameter_map[regex], text)

        return text
def add_dll_map(file, new_dll_line):

        fd = open(file, 'r')
        closing_config_match = re.compile('</configuration>')
        text = ""

        for line in fd.readlines():
                if closing_config_match.search(line):
                        text = text + '\t' + new_dll_line + '\n'

                text = text + line
        fd.close()

        # Save changes back out
        fd = open(file, 'w')
        fd.write(text)
        fd.close()


# Might need this later
# Actually removes lines containing text
#  Used to be: remove_dll_map
def remove_line_matching(file, text_to_remove):

        fd = open(file, 'r')
        new_text = ""

        for line in fd.readlines():
                if not line.count(text_to_remove):
                        new_text = new_text + line
        fd.close()

        # Save changes back out
        fd = open(file, 'w')
        fd.write(new_text)
        fd.close()


def launch_process(command, capture_stderr=1, print_output=1, print_command=0, terminate_reg="", logger="", output_timeout=0, kill_process_group=0):
	"""Execute a command, return output (stdout and optionally stderr), and optionally print output the process is being run.

	Returns a tuple: exit code, output

	terminate_reg is a regular expression object where if it is matched during the output,
		execution terminates, and None is returned for exit code, and output thus far is returned

	If a logger object (pyutils/logger) is passed in, output will be logged to there as well.

	output_timeout: kill process if it produces no output for x number of seconds.

	kill_process_group: This determines how the process is killed when output_timeout is specified.
		If this is true, the process group of the current python interpreter is killed, killing all subprocesses.
		If not, only the child process id is killed.
		The exit status of killed processes seems to vary (see packaging/build for possibilities)."""

	terminate_flag = 0
	if terminate_reg: terminate_flag = 1

	# This is set by utils.debug
	if debug:
		print_output=1
		print_command=1

	# turn off output if a logger is used
	if logger: print_output=0

	if print_command: print command

	if capture_stderr:
		process = popen2.Popen4(command)
	else:
		process = popen2.Popen3(command)

	# Close unnecessary handles
	process.tochild.close()

	if output_timeout:
		flags = fcntl.fcntl(process.fromchild.fileno(), fcntl.F_GETFL)
		flags = flags | os.O_NONBLOCK
		fcntl.fcntl(process.fromchild.fileno(), fcntl.F_SETFL, flags)
		# Set process group
		# each process created has a process group of the same number as the process id already
		#  But usually, this is the bash process, and we need to find out how to get that in 

	output_received_timestamp = time.time()
	killed = 0

	collected = []

	# there's a bug with output_timeout... ex:
	# adding: lib/mono/1.0/mono-service.exe.mdb (deflated 51%)
	# (deflated 52%)
	#  adding: lib/mono/1.0/mono-shlib-cop.exe.mdb (deflated 54%)
	# Looks like a bug in python's readline...

	# TODO: If we're going to accurately use terminate_reg, we'll need some reworking so that we try the reg, line at a time

	# Use this looping method insead of 'for line in process' so it doesn't use the readahead buffer
	#  This smooths output greatly, instead of getting big chunks of output with lots of lag
	while(1):
		try:
			#line = process.fromchild.readline()
			#  in non blocking mode, readline somehow misses data... use read() instead
			line = process.fromchild.read(128)
			output_received_timestamp = time.time()
		except IOError:
			#print "No data..."
			if time.time() - output_received_timestamp > output_timeout:
				print "** Terminating process because no output for %d second(s)**" % output_timeout
				sys.stdout.flush()
				# Close I/O handles?
				process.fromchild.close()

				#  Kill the process
				try:
					# Kill the process group of the current process...
					if kill_process_group:
						print "** Killing process group (committing suicide) ... **"
						pid = -os.getpgrp()
					else:
						print "** Killing process subprocess pid... **"
						pid = process.pid

					sys.stdout.flush()
					os.kill(pid, signal.SIGKILL)
				
				except OSError:
					print "** Error killing process(es) (%d), exiting... **" % pid
					sys.stdout.flush()
					sys.exit(1)

				# This will only get set if kill_process_group is false
				killed = 1
				break
			# Don't work the processor too much...
			time.sleep(.3)
			continue

		if not line: break
		if print_output:
			#print line,
			# Use this instead so we don't get spaces (the print function always adds a space
			#  between arguments)
			sys.stdout.write(line)
			sys.stdout.flush()
			# This doesn't work on macosx... ?
			#process.fromchild.flush()
		if logger:
			logger.log(line)

		collected += [ line ]

		if terminate_flag and terminate_reg.search(line):
			print "** Terminating process because termination string was found **"
			os.kill(process.pid, signal.SIGKILL)
			break


	exit_code = process.wait()
	
	if exit_code:
		exit_code /= 256

	if killed:
		exit_code = KILLED_EXIT_CODE

	#  Concat array elements into a string 
	#  strip the whitespace off the end (makes it behave more like commands.getxxx)
	return exit_code, "".join(collected).rstrip()


def get_latest_ver(dir, version=""):
	"""args: dir, and optional version.
	If version is specified, the latest release of that version will be selected."""

	if os.path.exists(dir):
		files = os.listdir(dir)
	else:
		print "utils.get_latest_ver: Path does not exist: %s" % dir
		sys.exit(1)

	if not files:
		print "utils.get_latest_ver: No dir entries in %s, exiting..." % dir
		sys.exit(1)

	# If a version is specified, find latest release of that version
	if version:
		candidates = []
		if os.path.exists(dir + os.sep + version):
			candidates.append(version)

		for file in files:
			# If a version is found in 'version-x' format, add it to candidates
			if file.find(version + "-") != -1:
				candidates.append(file)
		files = candidates

		if len(files) == 0:
			print "utils.Could not find dir entry for '%s/%s', exiting" % (dir, version)
			sys.exit(1)

	latest_version = version_sort(files).pop()

        return latest_version



# TODO: Might implement this in python later... ?
def version_sort(my_list):
	"""returns list that was passed in in a sorted order."""


	# Test to see if rpmvercmp is working
        (code, output) = launch_process(rpmvercmp_path + " " + string.join(my_list), print_output=debug)
	if code:
		print "Warning, rpmvercmp is not working!"
		cwd = os.getcwd()
		os.chdir(os.path.dirname(rpmvercmp_path))
		print "Attempting to fix..."
		(code, output) = launch_process("make clean; make", print_output=debug)
		(code, output) = launch_process(rpmvercmp_path + " " + string.join(my_list), print_output=debug)
		os.chdir(cwd)

		if code:
			print "Unable to fix..."
			sys.exit(1)

	return output.split()


def remove_list_duplicates(my_list):
	copy = my_list
	files = []
	for file in copy:
		if not file in files:
			files += [ file ]
	return files

def get_time():
	#Fri Apr 29 14:20:47
	#return time.strftime("%a %b %d %H:%M:%S")
	return time.asctime()

def time_duration_asc(start, finish):
	"""Returns number of minutes between times (and times are in time.asctime format)."""

	# Construct time time tuple
	try:
		start_time = calendar.timegm( time.strptime(start) )
		finish_time = calendar.timegm( time.strptime(finish) )
	except:
		return "?"

	# Return minutes of duration
	return (finish_time - start_time) / 60


