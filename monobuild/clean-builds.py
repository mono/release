#!/usr/bin/env python

# Script to clean out builds produced by the build scheduler.  Even though RELEASE is an option, it should pretty much never be used.
#
# remove_build_info removes the build info dir, which has the xml status file, and the build logs, as well as any links
# remove_builds removes the links in the files dir, as well as the actual rpm or zip files
# remove_tarball_logs removes the links in the logs dir, as well as the actual mktarball log file

import sys
import os
import shutil
import getopt

import pdb

sys.path += ['../pyutils']

import config
import build

def usage_and_exit():
	print "Usage: ./clean-builds.py [ --remove_tarball_logs --remove_builds --remove_build_info | --remove_all ] [--execute ] <HEAD|RELEASE> <num_builds_to_keep>"
	sys.exit(1)


def handle_link_files(path):
	full_path = config.build_info_dir + os.sep + path
	if os.path.exists(path):
		for f in os.listdir(full_path):
			if os.path.islink(full_path + os.sep + f):
				link_target = os.readlink(os.path.join(full_path, f) )
				link_targets.append(os.path.join(path, f, link_target))

				# Also remove the symlink
				links.append(os.path.join(path, f))

def cleanup(files, type):
	for f in files:
		if os.path.exists(f):
			print "Removing (%s) " % type + f,
			if execute:
				print "for real..."
				shutil.rmtree(f)
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
dirs = []
links = []
link_targets = []
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
					# TODO: remove from [snapshot][zip_]packages as well ... ?  will have to follow the symlink
					if remove_tarball_logs:
						handle_link_files(my_path + os.sep + 'logs')
				if remove_builds:
					handle_link_files(my_path + os.sep + 'files')
							

# Start removing files
os.chdir(config.build_info_dir)

cleanup(link_targets, "link_target")
cleanup(dirs, "dir")
cleanup(links, "link")


