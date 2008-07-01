#!/usr/bin/env python

import sys
import os

sys.path.append('../pyutils')

import utils

try:
	me, dir = sys.argv
except:
	print "Usage: ./svn_clean_ignores.py <path to svn work area>"
	sys.exit(1)


def clean_dir(dir):

	os.chdir(dir)

	# Get svn:ignore for this dir
	code, files = utils.launch_process('svn propget svn:ignore .', print_output=0)

	# If there's some valid data
	if not code:
		for f in files.split():
			if os.path.isdir(f):
				utils.launch_process('rm -Rf ' + f, print_command=1)
			else:
				utils.launch_process('rm -f ' + f, print_command=1)


		# Remove the ignored files

		for d in os.listdir('.'):
			if os.path.isdir(d):
				clean_dir(d)

	os.chdir('..')


# Clean up a repo
clean_dir(dir)

# Don't think I want to do this yet...  (keep local changes)
#utils.launch_process("cd %s; svn -R revert ." % dir)

utils.launch_process("cd %s; svn update" % dir)

