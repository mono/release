#!/usr/bin/env python

import sys
import os
import os.path
import pdb
import time

sys.path += [ '../pyutils' ]

import config
import build
import utils

# Use rsync to synchronize the last n builds

# TODO: Run a later cronjob on mono.ximian.com that deletes all but the latest n builds (probably 10 or 20)

# Target information
host = 'mono-web@mono.ximian.com'
target_dir = 'release/monobuild/www/builds'

# Testing
#host = 'wberrier@wblinux.provo.novell.com'
#target_dir = 'wa/msvn/release/monobuild/www/builds'

#num_builds = 50 # 880 MB in one test...
#num_builds = 20 # 434 MB in one test...
num_builds = 10 # 268 MB in one test...


def sync_dirs():

	dirs = []
	# Gather dirs to synchronize
	for i in ['HEAD', 'RELEASE']:
		for distro in os.listdir(config.build_info_dir + os.sep + i):
			for component in os.listdir(config.build_info_dir + os.sep + i + os.sep + distro):
				# Get the last 'num_builds' number of elements from the list
				versions = build.get_versions(i, distro, component)[-num_builds:]
				for j in versions:
					dirs.append(os.path.join(i, distro, component, j))


	os.chdir(config.build_info_dir)

	#  For some reason the --delete option crashes when running the second time to go-mono.com and mono.ximian.com ... ?
	# rsync all files over, and don't include the builds... just logs and info.xml
	status, output = utils.launch_process('rsync -avzR -e ssh --copy-links --exclude=files %s %s:%s' % (" ".join(dirs), host, target_dir))


while(1):
	print " *** Syncing ***"
	sync_dirs()
	print " *** Sleeping ***"
	time.sleep(10)

