#!/usr/bin/env python

# My first python script...
# Get all the rpms from cd images or http/ftp sites and stick them in one directory
#  The idea is to gather rpms and then make a repository from them, (open-carpet) or use them to create a jail

# Usage: ./gatherrpms.py <method> <dest_dir> <iso files|url>
#  Where method is either iso, web, or ftp


import sys
import os
import commands
import re
import shutil
import tempfile
import urllib
import urlparse
import htmllib
import ftplib
import formatter
import string
import time

# For debugging
import pdb

############################################################
# Miscellaneous functions and vars
############################################################

# They only get compiled once here...
ignoresource = re.compile("\.(no)?src\.rpm$")
matchrpm = re.compile("\.rpm$")

def print_debug(string):
	global debug
	debug = 0
	if debug:
		print string


# Name pattern matching
def is_an_rpm(string):
	if not ignoresource.search(string) and matchrpm.search(string):
		return 1
	else:
		return 0

# Do an integrity check on an rpm
def valid_rpm(full_pathname):

	(status, output) = commands.getstatusoutput("rpm -K --nosignature " + full_pathname);
	status /= 256

	if status == 0:
		return 1
	else:
		return 0


############################################################
#  Get from iso images
############################################################
def get_from_cd(dest_dir, iso_files):

	# Get cwd
	cwd = os.getcwd()

	# find a temporary location
	tempdir = tempfile.mktemp()
	os.mkdir(tempdir)

	for iso in iso_files:

		# mount the iso image in a temp spot
		(status, output) = commands.getstatusoutput("mount -o loop " + iso + " " + tempdir);
		status /= 256

		if status > 0:
			print "Error mounting iso: " + output
			sys.exit(1)

		os.chdir(tempdir)

		for file in os.popen("find . -name *rpm").readlines():
			file = file.strip()

			print os.path.basename(iso), ":",
			# check so it's not a src rpm... or nosrc.rpm
			if is_an_rpm(file):
				if os.path.isfile(file):
					print file
					shutil.copy(file, os.path.join(cwd, dest_dir))
			else:
				print "Skipping: " + file

		# umount the iso
		os.chdir(cwd)
		print commands.getoutput("umount " + tempdir)


	# Clean up
	os.rmdir(tempdir)


############################################################
#  Get from ftp site
############################################################
def get_from_ftp(dest_dir, url):

	(scheme, network, path, query, frag) = urlparse.urlsplit(url)

	if url[-1] != "/":
		print "Url must end with '/'"
		sys.exit(1)

	if scheme.find("ftp") == -1:
		print "Url must start with ftp"
		sys.exit(1)

	global hostname, destdir, ftp
	hostname = "%s://%s" % (scheme, network)
	destdir = dest_dir

	# Put us in the destination directory where the rpms will get dumped
	os.chdir(dest_dir)

	# Connect
	ftp = ftplib.FTP(network)
	ftp.login()

	crawl_ftp(path)


# always takes a full path
def crawl_ftp(path):
	dir_list = []

	# Change to the path
	try:
		ftp.cwd(path)
	# Skip if we don't have permission
	except ftplib.error_perm:
		print_debug("Skipping (access denied): " + path)
		return

	print_debug("Executing dir command")
	ftp.retrlines('LIST', dir_list.append)

	for dir in dir_list:

		list = dir.split()
		name = list[8]

		# Skip these types of directories
		if name == "." or name == "..":
			print_debug("Skipping . and ..")
		# is it a file and an rpm
		elif list[0][0] == "-" and is_an_rpm(name):
			if not os.path.exists(name):
				try:
					print "* Downloading: " + hostname + path + os.sep + name
					ftp.cwd(path) # Make sure we're in the correct dir through amidst recursion
					ftp.retrbinary('RETR ' + name, open(name, 'wb').write)
				except :
					print_debug("Skipping (access denied): " + name)
			elif not valid_rpm(os.getcwd() + os.sep + name):
				print "Invalid digest: " + name
				sys.exit(1)
			else:
				print "%s already exists (integrity tested)" % name
				
		# it's a directory	
		elif list[0][0] == "d":
			ftp.cwd(path) # Make sure we're in the correct dir through amidst the recursion
			new_dir = ftp.pwd() + os.sep + name
			
			print_debug("Recursing: " + new_dir)
			crawl_ftp(new_dir)
		else:
			print_debug("Unknown list entry or ignoring file: " + dir)



############################################################
#  Get from http site
############################################################
def get_from_web(dest_dir, url):

	(scheme, network, path, query, frag) = urlparse.urlsplit(url)

	# Do some sanity checks
	if url[-1] != "/":
		print "Url must end with '/'"
		sys.exit(1)

	if scheme.find("http") == -1:
		print "Url must start with http"
		sys.exit(1)

	global hostname, destdir, source, visited
	visited = {}
	hostname = "%s://%s" % (scheme, network)
	destdir = dest_dir
	source = url

	crawl_web(url)


def crawl_web(url):

	global hostname, destdir, visited

	print_debug ("Walking url: " + url)

	if visited.has_key(url):
		print_debug( "Already been here, skipping: " + url)
	elif url.find("../") >= 0:
		print_debug("Skipping relativized links: " + url)
	else:
		# add this url to the "visited" list
		visited[url] = 1

		# Make sure we're not going above our source url...
		if not re.compile(source).search(url):
			print_debug ( "Out of bounds:: " + url )

		# Found an rpm
		elif is_an_rpm(url):
			# Download 
			(scheme, network, path, query, frag) = urlparse.urlsplit(url)
			filename = destdir + os.sep + os.path.basename(path)
			if not os.path.exists(filename):

				print "* Downloading: " + url
				try:
					urllib.urlretrieve(url, filename)
				except IOError:
					# How many times should I retry this?
					print "IOError, will try again in 5 secs"
					time.sleep(5)
					os.remove(filename)
					urllib.urlretrieve(url, filename)
						
			elif not valid_rpm(os.getcwd() + os.sep + filename):
				print "Invalid digest: " + filename
				sys.exit(1)
			else:
				print "%s already exists, not downloading (Integrity tested)" % filename

		# Recurse, it's a directory link
		elif url[-1] == "/":

			html = urllib.urlopen(url).read()

			p = Parser()
			p.feed(html)
			p.close()

			for link, target in p.anchors.items():
				print_debug ( "%s -> %s" % (link, target) )

				# Cases to cover:
				#  1. Full link
				#  2. relative to domain name
				#  3. relative to current url

				if target.find("://") >= 0:
					new_url = target
				elif target[0] == "/":
					new_url = hostname + target
				else:
					new_url = url + target

				crawl_web(new_url)
		else:
			print_debug( "Skipping link: " + url )



# Stolen from http://www.oreilly.com/catalog/pythonsl/chapter/ch05.html
class Parser(htmllib.HTMLParser):
	# return a dictionary mapping anchor texts to hpyerlinks

	def __init__(self, verbose=0):
		self.anchors = {}
		f = formatter.NullFormatter()
		htmllib.HTMLParser.__init__(self, f, verbose)

	def anchor_bgn(self, href, name, type):
		self.save_bgn()
		self.anchor = href

	def anchor_end(self):
		text = string.strip(self.save_end())
		if self.anchor and text:
			self.anchors[text] = self.anchor


############################################################
#  Main method to be called from the command line
############################################################
def commandline():
	# Need to look into some command line processing
	if len(sys.argv) < 4:
		print "Usage: ./gatherrpms.py <method> <distro_name> <iso files|url>"
		print "\tWhere method is either iso, http, or ftp"
		print "\tand distro_name can be in the format of these examples: suse-93 or suse-93-x86_64"
		print "\t (reason for suse-93 or suse-93-x86_64 is that multiple archs are often hosted in one location)"
		print "\t(iso files is a space delimited list, useful for bash globbings)"
		sys.exit(1)

	# Collect args
	method = sys.argv[1]
	distro_name = sys.argv[2]

	destdir = "rpms" + os.sep + distro_name

	if os.path.exists(destdir) and not os.path.isdir(destdir):
		print "%s exists, but is not a directory, exiting..." % destdir
		sys.exit(1)

	if not os.path.exists(destdir):
		os.mkdir(destdir)

	if method == "iso":
		fetch = get_from_cd
		# Get everything from index 2 on
		source = sys.argv[3:]
	elif method == "http":
		fetch = get_from_web
		source = sys.argv[3]
	elif method == "ftp":
		fetch = get_from_ftp
		source = sys.argv[3]
	else:
		print "Unknown method: %s" % method
		sys.exit(1)

	fetch(destdir, source)


# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
	commandline()


