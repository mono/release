#!/usr/bin/env python

import sys
import os.path
import re
import time

import pdb

sys.path += [ '../pyutils' ]

import packaging
import build
import config
import src_repo_utils
import datastore
import logger


# Minutes
max_poll_interval = 5
#max_poll_interval = 1

# TODO: catch sig quit to allow finishing of last mktarball?


# Create tarballs starting from this point
#  Raise or lower this number as we go along...
#starting_rev = 57790
starting_rev = 57775

# static list of packages to create tarballs for
# What packages should these be?
packages = ['mono-1.1', 'mono-1.1.13']


src_repo = src_repo_utils.svn(config.MONO_ROOT)
distfiles = datastore.source_file_repo()

log = logger.Logger(filename='tarball_builder.log')


pack_objs = {}
for pack in packages:
	pack_objs[pack] = packaging.package("", pack)

while(1):

	# routinely check for updates (sleep every so often)

	# get latest version from the tree
	latest_tree_rev = src_repo.latest_tree_revision()
	log.log("Latest tree rev: %d" % latest_tree_rev)


	# Pretty much do every commit (for binary search on regressions) (should be adjustable)
	for i in range(starting_rev, latest_tree_rev):

		for pack_name, pack_obj in pack_objs.iteritems():

			latest_for_package = src_repo.latest_path_revision(pack_obj.info['HEAD_PATH'], revision=i)
			if not distfiles.contains(pack_name, "snap", str(latest_for_package)):
				command = "cd %s; ./mktarball %s %s snap %d" % (config.packaging_dir, config.mktarball_platform, pack_name, latest_for_package)
				log.log("Executing: " + command)
				# TODO: Logging
				#  daemon log

				# TODO: the system needs to be smarter about reinstalling the same rpms over and over...
				#  as well as not checking out the source each time (take advantage of 'svn update' somehow)

				# This will show console output, but not write to the log
				#  Log will be for brief info, and the console will watch what's currently going on
				os.system(command)

				# TODO: handle jail busy errors (exit code of 2)

				# Handle failed tarballs...
				if not distfiles.contains(pack_name, "snap", str(latest_for_package)):
					log.log("Tarball creation failed...")
					distfiles.add_file(pack_name, "snap", str(latest_for_package), "tarball_creation_failed")
			

	# TODO: Don't sleep if the above loop took longer than max_poll_interval
	log.log("Sleeping for %d minute(s)..." % max_poll_interval)
	time.sleep(60 * max_poll_interval)


