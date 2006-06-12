#!/usr/bin/env python

import sys
import os.path
import re
import time
import signal
import threading
import smtplib

sys.path += [ '../pyutils' ]

import packaging
import build
import config
import src_repo_utils
import datastore
import logger
import utils


# Minutes
max_poll_interval = 5
#max_poll_interval = 1

# static list of packages to create tarballs for
# What packages should these be?
packages = ['mono', 'mono-1.1.13', 'libgdiplus']

src_repo = src_repo_utils.svn(config.MONO_ROOT)
distfiles = datastore.source_file_repo()

log = logger.Logger(filename='tarball_builder.log')

pack_objs = {}
for pack in packages:
	pack_objs[pack] = packaging.package("", pack)

#starting_rev = 61097

class mktarball_loop(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):

		while not sigint_event.isSet():

			# routinely check for updates (sleep every so often)

			# get latest version from the tree
			latest_tree_rev = src_repo.latest_tree_revision()
			log.log("Latest tree rev: %d\n" % latest_tree_rev)

			# Only do for the last couple of commits, rather than constantly updating a base revision
			starting_rev = latest_tree_rev - 10


			# Pretty much do every commit (for binary search on regressions) (should be adjustable)
			#  The + 1 is so that the latest tree revision will be checked (range func does not include the last number in the sequence)
			for i in range(starting_rev, latest_tree_rev + 1):

				for pack_name, pack_obj in pack_objs.iteritems():

					latest_for_package = src_repo.latest_path_revision(pack_obj.info['HEAD_PATH'], revision=i)
					if not distfiles.contains('HEAD', pack_name, str(latest_for_package)) and not sigint_event.isSet():
						command = "cd %s; ./mktarball %s snap %d" % (config.packaging_dir, pack_name, latest_for_package)
						log.log("Executing: %s\n" % command)
						# TODO: Logging
						#  daemon log

						# TODO: the system needs to be smarter about reinstalling the same rpms over and over...

						# This will show console output, but not write to the log
						#  Log will be for brief info, and the console will watch what's currently going on
						  # (For some reason my signal gets ignored if I'm using os.system... seems to work with popen)
						(code, output) = utils.launch_process(command)
						print "Exit code: %d" % code

						# handle jail busy errors (exit code of 2)
						if code == 2:
							print "Jail busy, retrying later..."

						# Handle failed tarballs...
						elif not distfiles.contains('HEAD', pack_name, str(latest_for_package)):
							log.log("Tarball creation failed...\n")
							distfiles.add_file('HEAD', pack_name, str(latest_for_package), "tarball_creation_failed")

							utils.send_mail('wberrier@novell.com', 'wberrier@novell.com', 'mktarball failed (%s %d)' % (pack_name, latest_for_package), "mktarball has failed for package %s revision %d" % (pack_name, latest_for_package))

			# TODO: Don't sleep if the above loop took longer than max_poll_interval
			if not sigint_event.isSet():
				log.log("Sleeping for %d minute(s)...\n" % max_poll_interval)
				time.sleep(60 * max_poll_interval)


# Signal handler routine
#  This will let the thread finish when CTRL-C is pushed
def keyboard_interrupt(signum, frame):
        print "*** Signaling thread to finish ***"
        sigint_event.set()

# Set up event object
sigint_event = threading.Event()

# Set signal handler
signal.signal(signal.SIGINT, keyboard_interrupt)

thread = mktarball_loop()
thread.start()

# Sleep in main thread if child thread is still alive (This allows correct signal handling)
while thread.isAlive():
	#print "Waiting for thread %s ..." % thread.getName()
	time.sleep(1)

