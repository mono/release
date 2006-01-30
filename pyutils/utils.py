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

import pdb

# Full path to the rpmvercmp binary, maybe this could be done in python
#  So it's not arch specific
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
rpmvercmp = os.path.abspath(module_dir + "../rpmvercmp/rpmvercmp")

debug=0

# Get vars out of shell scripts (def files)
def get_env_var(var_name, source):

	if not os.path.exists(source):
		print "File not found: %s" % source
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
def extract_file(filename):
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

                (status, output) = launch_process("rpm2cpio %s | cpio -idv" % filename, print_output=debug)
                #print output
                #print "Status: %d" % status
                if status:
                        print "Error extracting rpm file: %s" % filename
                        sys.exit(1)

                os.chdir("usr")
                #(status, output) = commands.getstatusoutput("cp -Rf * ../..")
                #(status, output) = commands.getstatusoutput("find . -print | cpio -pdum ../..")
		# Launch process doesn't work well with find on cygwin...
		#(status, output) = launch_process("find . -print | cpio -pdum ../..")
		recursive_copy(".", "../..")

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

                #(status, output) = launch_process("find . -print | cpio -pdum ../../..")
                #if status:
                #        print "Error massaging files from solaris package: %s" % filename
                #        sys.exit(1)

                recursive_copy(".", "../../..")

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


def launch_process(command, capture_stderr=1, print_output=1):
	"""Execute a command, return output (stdout and optionally stderr), and optionally print as we go.

	Returns a tuple: exit code, output
	Like commands.getstatusoutput, except this is portable, where 'commands' is unix only
	Also, this can print it's output as it runs, where as commands captures output and returns it later
	If you want to do this and you need input/output handles, you'll need to use popen2, or os.open2
	"""

	execute_option = ""
	if capture_stderr: execute_option = " 2>&1 "

	# bufsize=1 makes it line buffered, -1, unbuffered
	#process = os.popen("%s %s" % ( command, execute_option), 'r', 1)
	# I'm not noticing a difference
	process = os.popen("%s %s" % ( command, execute_option), 'r', 1)

	collected = []
	# How to iterate over this so it's not so choppy?
	for line in process:
		if print_output:
			print line,
		collected += line

	exit_code = process.close()
	
	if exit_code:
		exit_code /= 256

	# Yikes, hope this doesn't break anything
	#  Concat array elements into a string 
	#  strip the whitespace off the end (makes it behave more like commands.getxxx)
	return exit_code, "".join(collected).rstrip()

# This isn't buildenv or package specific, leave it here
def get_latest_ver(dir):
        files = os.listdir(dir)

        (code, output) = launch_process(rpmvercmp + " " + string.join(files), print_output=debug)

        # Get last line of output
        latest_version = output.split().pop()

        return latest_version

def recursive_copy(src, dest):
	"""Args: src dir, dest dir: copies everything in src to dest.

	Differs from shutil.copy_tree in that the destination can exist
	"""

	for root, dirs, files in os.walk('.'):
		for dir in dirs:
			# TODO: Do we need to take care of symlinked directories?
			   # os.walk doesn't follow them
			dest_dir = os.path.join(dest, root, dir)
			if not os.path.exists(dest_dir):
				os.mkdir(dest_dir)
		for file in files:
			src_file = os.path.join(root, file)
			dest_file = os.path.join(dest, root, file)
			if not os.path.exists(dest_file):
				# Check to see if it's a symlink
				try:
					target = os.readlink(src_file)
					if debug: print "Read link: %s" % target
					do_link = 1
				except OSError:
					do_link = 0
				# Avoid nested try blocks...
				if do_link:
					os.symlink(target, dest_file)
					if debug: print "Created symlink: %s to %s" % (target, dest_file)
				else:
					shutil.copy2(src_file, dest_file)
					if debug: print "Copied %s to %s" % (src_file, dest_file)

			else:
				print "Warning! %s exists in destination already" % src_file


def remove_list_duplicates(my_list):
	copy = my_list
	files = []
	for file in copy:
		if not file in files:
			files += [ file ]
	return files


