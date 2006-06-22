#!/usr/bin/env python

# Probably will only build HEAD packages for now...  No reason it couldn't build RELEASE... ?

# TODO: Logging
# TODO: Prioritize builds: Maybe there should be one thread per jail, and that thread chooses a tarball to build, and prioritizes.  That way, there are no wait times for startup (we'll only sleep when there are no tarballs available to build) But, if we have jail multiplicity, the current design would be better
# Possible TODO: For the slower build platforms, we could check to make sure the build succeeded on i386 before starting... ?

import sys
import os
import threading
import time
import re
import signal

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
latest_build_distros = [ 'sles-9-x86_64', 'macos-10-ppc', 'redhat-9-i386', 'win-4-i386', 'sunos-8-sparc', 'sles-9-ia64', 'sles-9-s390', 'sles-9-s390x' ]

latest_build_packages = [ 'mono', 'mono-1.1.13', 'mono-1.1.8', 'mono-1.1.7', 'libgdiplus' ]

# regex to grab version out of filename
# This only follows standards by autotools for now...
version_re = re.compile(".*-(.*).(tar.gz|tar.bz2|zip)")

tarballs = datastore.source_file_repo()


class build_latest(threading.Thread):

	def __init__(self, distro, package_name):
		threading.Thread.__init__(self)

		self.distro = distro
		self.package_name = package_name

		self.setName("%s - %s" % (distro, package))

		self.done = False

	def interrupt(self):
		self.done = True


	def run(self):

		distro = self.distro
		package_name = self.package_name

		pack_obj = packaging.package("", package_name)

		if not pack_obj.valid_build_platform(distro):
			print "%s does not build on %s (BUILD_HOSTS), thread exiting..." % (package_name, distro)
			return

		while not self.done:
			started_build = 0

			# Check to see what the latest tarball is
			tarball_filename = tarballs.get_latest_tarball("HEAD", package_name)

			if not tarball_filename:
				print "*** Error getting latest tarball (%s, %s) (Probably doesn't exist...)!!!" % (distro, package_name)
				print "Sleeping %d seconds..." % wakeup_interval

				time.sleep(wakeup_interval)

				# Break out of the while loop and finish if CTRL-C is pushed
				if sigint_event.isSet():
					self.interrupt()

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
					started_build = 1
					# Testing...
					#code = 2
					
					# Is the jail busy?  if so, just repeat this loop (and select a new tarball if a newer one exists)	
					if code == 2:
						print "Jail (%s) is busy or offline... will retry again" % distro
						started_build = 0
				else:
					print "Skipping existing build (%s, %s, %s)" % (distro, package_name, version)

			else:
				print "Skipping existing build (%s, %s, %s)" % (distro, package_name, version)


			if not started_build:
				print "Sleeping %d seconds..." % wakeup_interval
				time.sleep(wakeup_interval)

			# Break out of the while loop and finish if CTRL-C is pushed
			if sigint_event.isSet():
				self.interrupt()



# Signal handler routine
#  This will let each thread finish when CTRL-C is pushed
def keyboard_interrupt(signum, frame):
	print "*** Signaling threads to finish ***"
	sigint_event.set()

# Set up event object
sigint_event = threading.Event()

# Set signal handler
signal.signal(signal.SIGINT, keyboard_interrupt)
threads = []

for distro in latest_build_distros:
	for package in latest_build_packages:
		thread = build_latest(distro,package)
		thread.start()

		# For debugging (This will run each thread one at a time)
		#thread.run()

		threads.append(thread)

# Sleep if threads are still alive
#  Wow... here was the key... the main thread would exit, but pressing ctrl-c would go to the main thread (which had already exited)
#  source: http://groups.google.com/group/comp.lang.python/browse_thread/thread/bb177d4cff9cde4e/d39dbc7e71a897c2?lnk=st&q=threading+sigint+group%3Acomp.lang.python&rnum=4&hl=en#d39dbc7e71a897c2
for thread in threads:
	while thread.isAlive():
		#print "Waiting for thread %s ..." % thread.getName()
		time.sleep(1)

# Wrong!!
# This results blocks the main thread (and thus sigint gets ignored)
#for thread in threads:
#	thread.join()


