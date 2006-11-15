#!/usr/bin/env python

# Script to clean out builds produced by the build scheduler.  Even though RELEASE is an option, it should pretty much never be used.
#
# remove_build_info removes the build info dir, which has the xml status file, and the build logs, as well as any links
# remove_builds removes the links in the files dir, as well as the actual rpm or zip files
# remove_tarball_logs removes the links in the logs dir, as well as the actual mktarball log file

# TODO: what about sources that were never built?

import sys
import os
import shutil
import getopt
import re 

import pdb

sys.path += ['../pyutils']

import config
import build

def usage_and_exit():
	print "Usage: ./clean-builds.py [ --remove_tarball_logs --remove_builds --remove_build_info | --remove_all ] [--execute ] <HEAD|RELEASE> <num_builds_to_keep>"
	sys.exit(1)


# TODO: This in forming invalid paths...  try this to see:
# ./clean-builds.py --remove_builds HEAD 1000
def handle_link_files(path):
	full_path = config.build_info_dir + os.sep + path
	if os.path.exists(path):
		for f in os.listdir(full_path):
			if os.path.islink(full_path + os.sep + f):
				link_target = os.readlink(os.path.join(full_path, f) )
				link_target = os.path.join(path, link_target)

				# Only add this to the link if it exists
				if os.path.exists(link_target):
					link_targets.append(link_target)
				else:
					print "link_target doesn't exist: " + link_target

				# Also remove the symlink
				links.append(os.path.join(path, f))

def get_size_of_files(files):
	sum = 0
	for f in files:
		# Skip missing files
		if not os.path.exists(f):
			pass
		elif os.path.isdir(f):
			new_files = []
			for f2 in os.listdir(f):
				new_files.append(f + os.sep + f2)
			sum += get_size_of_files(new_files)
		else:
			sum += os.path.getsize(f)
	return sum



def cleanup(files, type):
	size = get_size_of_files(files)
	print "Total size for %s: %d (MB)" % (type, size / 1024 / 1024)
	space_summary.append("Total size for %s: %d (MB)" % (type, size / 1024 / 1024))
	for f in files:
		# os.path.exists doesn't check existance of the link, but the target
		if os.path.islink(f):
			print "Removing (%s) " % type + f,
			if execute:
				print "for real..."
				os.unlink(f)
			else:
				print
		elif os.path.exists(f):
			print "Removing (%s) " % type + f,
			if execute:
				print "for real..."
				# rmtree dies if removing a link pointing to an invalid file, or if it's a file
				if os.path.isdir(f):
					shutil.rmtree(f)
				else:
					os.unlink(f)
			else:
				print


remove_tarball_logs = False
remove_builds = False
remove_build_info = False
remove_all = False
execute = False

opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "remove_tarball_logs", "remove_builds", "remove_build_info", "remove_all", "execute" ])
for option, value in opts:
        if option == "--remove_tarball_logs":
		remove_tarball_logs = True
        if option == "--remove_builds":
		remove_builds = True
        if option == "--remove_build_info":
		remove_build_info = True
        if option == "--remove_all":
		remove_all = True
        if option == "--execute":
		execute = True

if remove_all:
	remove_tarball_logs = True
	remove_builds = True
	remove_build_info = True

try:
	HEAD_or_RELEASE, num_builds = remaining_args
	num_builds = int(num_builds)
	if HEAD_or_RELEASE != "HEAD" and HEAD_or_RELEASE != "RELEASE":
		throw
except:
	usage_and_exit()

# Exit if no remove options specified
if not (remove_tarball_logs or remove_builds or remove_build_info):
	usage_and_exit()


# Gather all the files
space_summary = []
dirs = []
links = []
link_targets = []

os.chdir(config.build_info_dir)

for distro in os.listdir(config.build_info_dir + os.sep + HEAD_or_RELEASE):
	for component in os.listdir(config.build_info_dir + os.sep + HEAD_or_RELEASE + os.sep + distro):
		# Get the last 'num_builds' number of elements from the list
		versions = build.get_versions(HEAD_or_RELEASE, distro, component)
		num_to_remove = len(versions) - num_builds

		if num_to_remove > 0:
			versions = versions[:num_to_remove]
			for j in versions:
				my_path = os.path.join(HEAD_or_RELEASE, distro, component, j)
				if remove_build_info:
					dirs.append(os.path.join(HEAD_or_RELEASE, distro, component, j))
					if remove_tarball_logs:
						handle_link_files(my_path + os.sep + 'logs')
				if remove_builds:
					handle_link_files(my_path + os.sep + 'files')
							

# Start removing files
cleanup(link_targets, "link_target")
cleanup(dirs, "dir")
cleanup(links, "link")

# The space summary isn't accurate and will always over estimate
#  Just gives an idea of about how much space to recover
#  (the same sources are listed as taking up space for each platform)
print "\n".join(space_summary)

