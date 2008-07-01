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
import re
import tempfile
import string
import glob
import time
import calendar
import popen2
import signal
import fcntl
import smtplib
import urllib2

# Catch this error, and then die later on if the namespace isn't found
#  (Allows us to use launch_process without having python-devel rpm installed on SuSE type machines)
try:
	import distutils.dir_util
except ImportError:
	print "Safely ignored warning: Missing distutils.dir_util..."


import pdb

# Full path to the rpmvercmp binary, maybe this could be done in python
#  So it's not arch specific
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
rpmvercmp_path = os.path.abspath(module_dir + "../rpmvercmp/rpmvercmp")
rpm2cpio_py_path = os.path.abspath(module_dir + "rpm2cpio.py")
rpmvercmp_module_path = os.path.abspath(module_dir + "../rpmvercmp")

debug=0
# These exit codes can't be negative... probably 8 bit unsigned
KILLED_EXIT_CODE=42
INTERRUPTED_EXIT_CODE=10 # Should be arbitrary... ?

match_all = re.compile('')

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

def extract_file(filename, preserve_symlinks=0, truncate_path='usr'):
	"""Extract various file types.

	preserve_symlinks: this option will be passed to copy_tree
	truncate_path: only files under this dir will be extracted, and the truncate_path will not 
		be included in extracted files"""


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
			print output
                        sys.exit(1)

        elif ext == ".rpm":
                #print "Found rpm!"
                tempdir = "___EXTRACT___"

                if os.path.exists(tempdir):
                        distutils.dir_util.remove_tree(tempdir)
                os.mkdir(tempdir)
                os.chdir(tempdir)

		# Use python version of rpm2cpio by default
                command = rpm2cpio_py_path + " %s | cpio -idv" % filename

		try:
			import bz2
		except ImportError:
			print "bz2 module not found... falling back to native rpm2cpio"
			command = "rpm2cpio %s | cpio -idv" % filename

                (status, output) = launch_process(command, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:

			# Weirdness for macosx...
			#  cpio on mac fails because it can't set the owner... just ignore this message
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

		# .mdb handling for broken -debug packages
		for root, dirs, files in os.walk('.'):
			for file in files:
				full_path = root + os.sep + file
				m1 = re.search("usr\/lib\/debug\/(.*\.mdb)", full_path)
				if m1:

					#print "Current: " + os.getcwd()

					dest_dir = os.path.dirname(m1.group(1))
					#print "Creating: " + dest_dir
					distutils.dir_util.mkpath(dest_dir)

					#print "Moving: " + full_path
					#print "to:                     " + m1.group(1)
					os.rename(full_path, m1.group(1))

		if truncate_path:
			current = os.getcwd()
			try:
				os.chdir(truncate_path)
			except OSError:
				print "truncate_path does not exist: %s (note: defaults to usr if nothing specified)" % truncate_path	
				sys.exit(1)
			distutils.dir_util.copy_tree(".", current + "/..", preserve_symlinks=preserve_symlinks)
			os.chdir(current)
		else:
			distutils.dir_util.copy_tree(".", "..", preserve_symlinks=preserve_symlinks)


                os.chdir("..")
                distutils.dir_util.remove_tree(tempdir)

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
			print output
                        sys.exit(1)

	# If it's a gzipped solaris package
        elif ext == ".gz":
                tempdir = "___EXTRACT___"

		final_dest_dir = os.getcwd()

                if os.path.exists(tempdir):
                        distutils.dir_util.remove_tree(tempdir)
                os.mkdir(tempdir)
                os.chdir(tempdir)

                (status, output) = launch_process("gunzip -c %s | pkgtrans /dev/stdin . all" % filename, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:
                        print "Error extracting solaris package file: %s" % filename
			print output
                        sys.exit(1)
		packagedir = glob.glob('*').pop()
		pkgmap = open(packagedir + os.sep + 'pkgmap', 'r')

		try:
			# sunfreeware packages use this convention
			os.chdir(packagedir + os.sep + 'reloc')
		except:
			# blastwave uses these
			os.chdir(os.path.join(packagedir, 'root', 'opt', 'csw'))

		# Fix up the symbolic links
		for line in pkgmap:
			# Matching example:
			#1 s none lib/libglib-2.0.so=libglib-2.0.so.0.200.3
			try: 
				(link, target) = re.compile('. . .*? (.*)=(.*)').search(line).groups()
				link = link.replace("/opt/csw/", "") # This is for blastwave packages, since they don't use relative paths
				os.symlink(target, link)
			except AttributeError:
				pass

		distutils.dir_util.copy_tree(".", final_dest_dir, preserve_symlinks=preserve_symlinks)

                os.chdir(final_dest_dir)
                distutils.dir_util.remove_tree(tempdir)

		# need to do some cleanup here (/var/tmp/<something>) (created by pkgtrans)
		for dir in glob.glob("/var/tmp/aaa*"):
			try:
				distutils.dir_util.remove_tree(dir)
			except:
				#print "Unable to remove: " + dir
				pass

	else:
		print "Warning!!! Unable to extract file of type %s" % ext
		return

        return os.path.basename(filename)

# Download url into cache (Don't redownload if file exists)
def get_url(url, destination):

	download_filename = destination + os.sep + os.path.basename(url)

	# Get size to make sure it's > 0
	if os.path.exists(download_filename):
		size = os.stat(download_filename).st_size
	else:
		size = 0

        # Download if we don't have it already
        if not size:
                print "Downloading: %s ..." % url
		if not os.path.exists(destination):
			distutils.dir_util.mkpath(destination)

		fd_out = open(download_filename, 'wb')

		try:
			fd_url = urllib2.urlopen(url)
		except:
			os.unlink(download_filename)
			raise "ErrorDownloadingFile"

		for data in fd_url.read():
			fd_out.write(data)

		fd_url.close()
		fd_out.close()

		# we didn't get any data...
		if not os.stat(download_filename).st_size:
			os.unlink(download_filename)
			raise "ErrorDownloadingFile"


def substitute_parameters_in_file(file, parameter_map, qualifier=match_all):

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

def append_text_to_files(file_text_map):

        for file in file_text_map.keys():
                print "Adding text to: " + file

		fd = open(file)
		text = fd.read()
		fd.close()

                text += file_text_map[file]

		fd = open(file, 'w')
		fd.write(text)
		fd.close()


def launch_process(command, capture_stderr=1, print_output=1, print_command=0, terminate_reg="", my_logger="", output_timeout=0, kill_process_group=0, max_output_size=0, interruptable=False):
	"""Execute a command, return output (stdout and optionally stderr), and optionally print output the process is being run.

	Returns a tuple: exit code, output

	terminate_reg is a regular expression string where if it is matched during the output,
		execution terminates, and None is returned for exit code, and output thus far is returned

	If a logger object (pyutils/logger) is passed in, output will be logged to there as well.

	output_timeout: kill process if it produces no output for x number of seconds.

	max_output_size: kill process if it outputs more than x chars.  0 (default) to disable.

	kill_process_group: This determines how the process is killed when output_timeout is specified.
		If this is true, the process group of the current python interpreter is killed, killing all subprocesses.
		If not, only the child process id is killed.
		The exit status of killed processes seems to vary (see packaging/build for possibilities)."""

	terminate_flag = 0
	if terminate_reg:
		terminate_flag = 1
		terminate_reg_obj = re.compile(terminate_reg)

	# This is set by utils.debug
	if debug:
		print_output=1
		print_command=1

	# turn off output if a logger is used
	if my_logger: print_output=0

	if print_command: print command

	if interruptable:
		interrupted_file = os.path.dirname(interruptable) + os.sep + "interrupted"
		if os.path.exists(interrupted_file):
			print "** Failing to execute command '%s' because 'interrupted' file is present: %s" % (command, interrupted_file )
			sys.exit(INTERRUPTED_EXIT_CODE)

	if capture_stderr:
		process = popen2.Popen4(command)
	else:
		process = popen2.Popen3(command)

	# Close unnecessary handles
	process.tochild.close()


	if interruptable:
		fd = open(interruptable, 'w')
		fd.write(str(os.getpgrp()))
		fd.close()

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

	# Track number of output bytes so we can die if it goes above log max
	output_size = 0
	output_overflow = False
	output_timeout_flag = False
	terminate_reg_flag = False

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
			output_size += len(line)
			output_received_timestamp = time.time()

			if max_output_size and output_size > max_output_size:
				print "** Terminating process because output size max of %d exceeded: %d chars(s)**" % (max_output_size, output_size)
				output_overflow = True
				raise IOError

			if terminate_flag and terminate_reg_obj.search(line):
				print "** Terminating process because termination regular expression (%s) was found: '%s'" % (terminate_reg, line)
				terminate_reg_flag = True
				raise IOError
				
		except IOError:
			#print "No data..."
			if output_timeout and time.time() - output_received_timestamp > output_timeout:
				output_timeout_flag = True
				print "** Terminating process because no output for %d second(s)**" % output_timeout
			if output_overflow or output_timeout_flag or terminate_reg_flag:
				sys.stdout.flush()
				# Close I/O handles?
				process.fromchild.close()

				#  Kill the process
				try:
					# clean up interruptable file if it's there
					if interruptable and os.path.exists(interruptable):
						os.unlink(interruptable)

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
		if my_logger:
			my_logger.log(line)

		collected += [ line ]



	exit_code = process.wait()
	
	if exit_code:
		exit_code /= 256

	if killed:
		exit_code = KILLED_EXIT_CODE

	# Clean up interruptable file? naw... shouldn't need to
	#  actually we do, one to remove file if process isn't running,
	#  also if we're root (install rpms), we need to remove this while we have rights
	if interruptable and os.path.exists(interruptable):
		os.unlink(interruptable)

	#  Concat array elements into a string 
	#  strip the whitespace off the end (makes it behave more like commands.getxxx)
	return exit_code, "".join(collected).rstrip()



def get_versions(dir, version="", fail_on_missing=True, version_reg=""):
	"""args: dir, and optional version.
	If version is specified, the latest release of that version will be selected.

	version_reg: select version only based on files matching regular expression,
		but verion has high precedence than version_reg.

	returns all versions (sorted)
	"""

	files = []
	if os.path.exists(dir):
		files = os.listdir(dir)
	elif fail_on_missing:
		print "utils.get_versions: Path does not exist: %s" % dir
		sys.exit(1)
	else:
		print "utils.py: get_versions: fail_on_missing=False, Warning: path does not exist: " + dir

	# If a version is specified, find latest release of that version
	#  and also take precedence over a version_reg
	if version:
		candidates = []
		if os.path.exists(dir + os.sep + version):
			candidates.append(version)

		for file in files:
			# If a version is found in 'version-x' format, add it to candidates
			if file.count(version + "-"):
				candidates.append(file)
		files = candidates

	# Or if a version reg is specified, only select versions matching it
	elif version_reg:
		candidates = []
		for file in files:
			if re.compile(version_reg).search(file):
				candidates.append(file)
		files = candidates

	return version_sort(files)

def get_latest_ver(dir, version="", fail_on_missing=True, version_reg=""):
	"""args: dir, and optional version.
	If version is specified, the latest release of that version will be selected.

	version_reg: select version only based on files matching regular expression,
		but verion has high precedence than version_reg.

	returns the latest version
	"""

	files = get_versions(dir, version, fail_on_missing, version_reg)

	if len(files) == 0:
		latest_version = ""
		if fail_on_missing:
			print "utils.get_latest_ver: No candidates for dir entry for '%s/%s', exiting" % (dir, version)
			sys.exit(1)

	else:
		latest_version = files.pop()

        return latest_version


# TODO: Might implement this in python later... ?
def version_sort_old(my_list):
	"""returns list that was passed in in a sorted order."""


	# Test to see if rpmvercmp is working
        (code, output) = launch_process(rpmvercmp_path + " " + string.join(my_list), print_output=debug)
	if code:
		print "Warning, rpmvercmp is not working!"
		cwd = os.getcwd()
		os.chdir(os.path.dirname(rpmvercmp_path))
		print "Attempting to fix..."
		(code, make_output) = launch_process("make clean; make", print_output=debug)
		(code, output) = launch_process(rpmvercmp_path + " " + string.join(my_list), print_output=debug)
		os.chdir(cwd)

		if code:
			print "Unable to fix... errors:"
			print make_output
			sys.exit(1)

	return output.split()

def version_sort(my_list):
	"""returns list that was passed in in a sorted order.

	Uses the rpmvercmp python extension to speed things up a bit.
	"""
	sys.path.append(rpmvercmp_module_path)
	try:
		import rpmvercmp
	except:
		print "Warning, rpmvercmp extension not compiled"
		cwd = os.getcwd()
		os.chdir(os.path.dirname(rpmvercmp_path))
		print "Attempting to fix..."
		(code, make_output) = launch_process("make clean; make", print_output=debug)
		os.chdir(cwd)
		import rpmvercmp

	my_list.sort(rpmvercmp.version_compare)

	return my_list

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
	# Return GMT instead of the current timezone (so we can store GMT time in info.xml)
	return time.asctime(time.gmtime())

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

def time_duration_clock(start, finish):
	"""Returns duration in [x days] hh:mm:ss format (times in time.asctime format)

	x days shows up only on long (usually frozen) times
	"""

	# Construct time time tuple
	try:
		start_time = calendar.timegm( time.strptime(start) )
		finish_time = calendar.timegm( time.strptime(finish) )
	except:
		return "?"

	# seconds of duration
	duration = finish_time - start_time

	days = duration / 86400
	duration %= 86400

	hours = duration / 3600
	duration %= 3600

	mins = duration / 60
	duration %= 60

	secs = duration

	ret = "%.2d:%.2d:%.2d" % (hours, mins, secs)

	if days:
		ret = "%d day(s) %s" % (days, ret)

	return ret


def adjust_for_timezone(tzo_seconds, time_string):

	return_string = time_string
	if time_string:
		seconds_past_epoch = calendar.timegm(time.strptime(time_string))
		seconds_past_epoch += int(tzo_seconds)
		return_string = time.asctime(time.gmtime(seconds_past_epoch))

	return return_string

def get_tz_string():
	tzs_offset = time.timezone / 60 / 60 * 100

	if tzs_offset > 0:
		tz_string = "-0%d" % tzs_offset
	else:
		tz_string = "+0%d" % tzs_offset

	return tz_string


def send_mail(fr, to, subject, body):

	# Construct date string
	# Date: Tue, 16 Jan 2007 23:33:55 -0500
	date = time.strftime("%a, %d %b %Y %H:%M:%S ") + get_tz_string()

        header = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n" % (fr, to, subject, date)
        msg = header + body

	try:
		server = smtplib.SMTP('mail.novell.com')
		server.sendmail(fr, to, msg)
		server.quit()
		val = True
	except:
		print "Error sending mail... ignoring."
		val = False

	return val


def unpack_source(filename, tar_path="tar"):
	"""Args: filename to extract
	Returns: directory of extracted source."""

	# Our tarballs require gnu tar, so allow this to be overridden
	# Make it possible to pass in an empty string
	if not tar_path: tar_path = "tar"

	if re.compile('\.zip$').search(filename):
		command = "unzip -q %s" % filename
	elif re.compile('\.tar\.bz2$').search(filename):
		command = "%s -jxf %s" % (tar_path, filename)
	elif re.compile('\.tar\.gz$').search(filename):
		command = "%s -zxf %s" % (tar_path, filename)
	else:
		print "Unknown filetype: " + filename
		sys.exit(1)

	current_files = os.listdir('.')

	# Extract source
	(code, output) = launch_process(command)

	if code:
		print 'Failed unpacking source: ' + command + filename
		sys.exit(1)

	new_files = os.listdir('.')
	# Difference (set command)
	#  (Would use sets, but they are new in ... python 2.4?)
	for f in new_files:
		if not current_files.count(f):
			source_dir = f 

	return source_dir

def get_dict_var(key, dict_hash):
	"""Get var from info dict if key exists, otherwise return empty string (or false?)"""

	return_val = ""
	if dict_hash.has_key(key):
		return_val = dict_hash[key]
	return return_val

def get_mac_filelists(include_ar_files=True):
	"""Return 2 lists: full filelist (excluding directories), mach-o filelist.  Each from current dir"""

	# Used both in do-install-zip-pkg and universal merge.  Consolidate here.

	full_filelist = []
	native_filelist = []

	candidate_filelist = []

	# Max files to pass on the command line (croaks if it's too long)
	max_num_files = 1000

	# Get a list of all files (which are not symlinks)
	for root, dirs, files in os.walk('.'):
		for file in files:
			full_path = root + os.sep + file
			full_filelist.append(full_path)
			if os.path.isfile(full_path) and not os.path.islink(full_path):
				candidate_filelist.append(full_path)

	# Get report from 'file' as to file types
	filelist_string = ""
	final_output = ""
	while len(candidate_filelist):
		(code, output) = launch_process('file ' + ' '.join(candidate_filelist[:max_num_files]), print_output=0)
		final_output += "\n" + output

		# Remove them from the list
		candidate_filelist = candidate_filelist[max_num_files:]

	# Find which files are native
	if include_ar_files:
		native_reg = re.compile('(.*):.*(Mach-O|ar archive)')
	else:   
		native_reg = re.compile('(.*):.*Mach-O')
	for match in native_reg.finditer(final_output):
		native_filelist.append(match.group(1))

	full_filelist.sort()
	native_filelist.sort()

	return full_filelist, native_filelist

 
