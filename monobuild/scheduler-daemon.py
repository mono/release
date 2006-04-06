#!/usr/bin/env python

# Probably will only build HEAD packages for now...  No reason it couldn't build RELEASE... ?

# TODO: Logging

import sys
import os
import threading
import time
import re

import pdb

sys.path += [ '../pyutils' ]

import config
import datastore
import packaging
import utils

#wakeup_interval = 60
wakeup_interval = 600

# Probably have to start a separate thread for each of these cases...
# Build every tarball that is popped out
sequential_build_distros = [ 'redhat-9-i386' ]
sequential_build_packages = [ 'mono', 'mono-1.1.13' ]

# Only build the latest tarball available
# Some of these platforms take much longer, and one platform shouldn't hold them all up
#latest_build_distros = [ 'sles-9-x86_64', 'macos-10-ppc', 'redhat-9-i386', 'win-4-i386', 'sunos-8-sparc', 'sles-9-ia64', 'sles-9-s390', 'sles-9-s390x' ]
latest_build_distros = [ 'sles-9-x86_64', 'macos-10-ppc', 'redhat-9-i386', 'win-4-i386', 'sunos-8-sparc', 'sles-9-ia64', 'sles-9-s390' ]

latest_build_packages = [ 'mono', 'mono-1.1.13' ]
#latest_build_packages = [ 'mono' ]


# regex to grab version out of filename
# This only follows standards by autotools for now...
version_re = re.compile(".*-(.*).(tar.gz|tar.bz2|zip)")

tarballs = datastore.source_file_repo()


def build_latest(distro, package_name):

	pack_obj = packaging.package("", package_name)

	if not pack_obj.info['BUILD_HOSTS'].count(distro):
		print "%s does not build on %s (BUILD_HOSTS), thread exiting..." % (package_name, distro)
		return

	while(1):
		#print "Build %s on %s" % (distro, package_name)

		# Check to see what the latest tarball is
		tarball_filename = tarballs.get_latest_tarball("HEAD", package_name)

		if not tarball_filename:
			print "*** Error getting latest tarball (%s, %s) (Probably doesn't exist...)!!!" % (distro, package_name)
			print "Sleeping %d seconds..." % wakeup_interval
			time.sleep(wakeup_interval)
			continue

		#print "Latest tarball: " + tarball_filename

		# Get version
		version, ext = version_re.search(tarball_filename).groups()

		info = datastore.build_info("HEAD", distro, package_name, version)

		# Build if the build doesn't exist already
		if not info.exists:
			# TODO: this double check needs to be more accurate
			# Check one more time to make sure the build doesn't exist
			time.sleep(2)
			if not info.exists:
				#print "Build! (%s, %s, %s)" % (distro, package_name, version)

				command = "cd %s; ./build %s %s %s" % (config.packaging_dir, distro, package_name, version)
				print command

				(code, output) = utils.launch_process(command, print_output=0)

				# Testing...
				#exit = 2
				
				# Is the jail busy?  if so, just repeat this loop (and select a new tarball if a newer one exists)	
				if code == 2:
					print "Jail (%s) is busy or offline... will retry again" % distro
			else:
				print "Skipping existing build (%s, %s, %s)" % (distro, package_name, version)

		else:
			print "Skipping existing build (%s, %s, %s)" % (distro, package_name, version)

		print "Sleeping %d seconds..." % wakeup_interval
		time.sleep(wakeup_interval)


threads = []
for distro in latest_build_distros:
	for package in latest_build_packages:
		thread = threading.Thread(target=build_latest, args=(distro,package,))
		thread.start()

		# For debugging (This will run each thread one at a time)
		#thread.run()

		threads.append(thread)


# Needed? (This will run forever...)
# Wait for all to finish
for thread in threads:
        if thread.isAlive(): thread.join()


