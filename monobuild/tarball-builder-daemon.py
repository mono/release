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

log = logger.Logger(filename='tarball_builder.log')

class tarball_builder(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

	def load_info(self):

		# reload list of packages (allows us to update the list without restarting the daemon)
		reload(config)

		self.max_poll_interval = config.td_max_poll_interval
		self.network_error_interval = config.td_network_error_interval

		self.num_sequential = config.td_num_sequential

		self.sequential = config.td_sequential

		self.src_repo = src_repo_utils.svn(config.MONO_ROOT)
		self.distfiles = datastore.source_file_repo()

		self.pack_objs = {}
		for pack in config.td_packages:
			self.pack_objs[pack] = packaging.package("", pack)
		

        def run(self):

		while not sigint_event.isSet():

			start_time = utils.get_time()

			self.load_info()

			# routinely check for updates (sleep every so often)
			for pack_name, pack_obj in self.pack_objs.iteritems():

				# get latest version from the tree
				latest_tree_rev = self.src_repo.latest_tree_revision()
				print "Latest tree rev: %d (%s)" % (latest_tree_rev, pack_name) 

				if not latest_tree_rev:
					log.log("Error getting latest tree rev, trying later... (%s)\n" % pack_name)

					# Restart for loop over...
					break

				# Only do for the last couple of commits, rather than constantly updating a base revision
				if latest_tree_rev <= self.num_sequential:
					starting_rev = 1
				else:
					starting_rev = latest_tree_rev - self.num_sequential

				# If we're not building each and every checkin, only build the latest
				if not self.sequential:
					starting_rev = latest_tree_rev

				# Pretty much do every commit (for binary search on regressions) (should be adjustable)
				#  The + 1 is so that the latest tree revision will be checked (range func does not include the last number in the sequence)
				for i in range(starting_rev, latest_tree_rev + 1):

					latest_for_package = self.src_repo.latest_path_revision(pack_obj.info['HEAD_PATH'], revision=i)
					if not latest_for_package:
						log.log("Error getting revision %d, trying later... (%s)\n" % (i, pack_name) )
						# Skip to next pack...
						break

					if not self.distfiles.contains('HEAD', pack_name, str(latest_for_package)) and not sigint_event.isSet():
						command = "cd %s; ./mktarball %s snap %d" % (config.packaging_dir, pack_name, latest_for_package)
						log.log("Executing: %s\n" % (command) )

						# TODO: the system needs to be smarter about reinstalling the same rpms over and over...

						# This will show console output, but not write to the log
						#  Log will be for brief info, and the console will watch what's currently going on
						  # (For some reason my signal gets ignored if I'm using os.system... seems to work with popen)
						(code, output) = utils.launch_process(command)
						log.log("Exit code: %d (%s)\n" % (code, pack_name))

						# handle jail busy errors (exit code of 2)
						if code == 2:
							print "Jail busy, retrying later... (%s)" % pack_name

						# Handle failed tarballs...
						elif code:
							log.log("Tarball creation failed...(%s)\n" %pack_name)

							# Send out the log with the tarball, or at least a link... ?
							link = "http://monobuild1.boston.ximian.com/tarball_logs/HEAD/%s/%d.log" % (pack_name, latest_for_package)
							utils.send_mail('wberrier@novell.com', 'wberrier@novell.com', 'mktarball failed (%s %d)' % (pack_name, latest_for_package), "mktarball has failed for package %s revision %d\n\n%s" % (pack_name, latest_for_package, link))

			time_duration = utils.time_duration_asc(start_time, utils.get_time()) * 60

			# Only sleep if this loop was shorter than max_poll_interval
			#  and if we do sleep, discount the time_duration
			if not sigint_event.isSet() and time_duration < self.max_poll_interval:
				print "Sleeping for %d seconds..." % (self.max_poll_interval - time_duration)
				time.sleep(self.max_poll_interval - time_duration)


# Signal handler routine
#  This will let the thread finish when CTRL-C is pushed
def keyboard_interrupt(signum, frame):
        print "*** Signaling thread to finish ***"
        sigint_event.set()

# Set up event object
sigint_event = threading.Event()

# Set signal handler
signal.signal(signal.SIGINT, keyboard_interrupt)

thread = tarball_builder()
thread.start()

# Sleep in main thread if child thread is still alive (This allows correct signal handling)
while thread.isAlive():
	#print "Waiting for thread %s ..." % thread.getName()
	time.sleep(1)

