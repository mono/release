#!/usr/bin/env python

import os
import shutil
import sys

sys.path.append("../pyutils")

import build

# TODO: 
#  Instead, these urls: they are fully dynamic, and get updated more often.  Only problem: harder to bookmark.  Issue?

# http://mono.ximian.com/monobuild/python/monobuild.py/download_latest?platform=sles-9-i586&package=mono&HEAD_or_RELEASE=HEAD&step=api-diff
# http://mono.ximian.com/monobuild/python/monobuild.py/download_latest?platform=sles-9-x86_64&package=mono&HEAD_or_RELEASE=HEAD&step=api-diff
# http://mono.ximian.com/monobuild/python/monobuild.py/download_latest?platform=sles-10-i586&package=mono-basic&HEAD_or_RELEASE=HEAD&step=api-diff
# http://mono.ximian.com/monobuild/python/monobuild.py/download_latest?platform=sles-10-i586&package=olive&HEAD_or_RELEASE=HEAD&step=api-diff

# The class status pages are up in the air... wait until the new ones come to make any changes

#output_dir = "tmp"
output_dir = "/var/www/mono-website/go-mono/class-status"

# Note: when modules start building on other distros, these need to be updated
# The wiki page pointing to these will also need to be updated
status_config = [
	['1.1',		'sles-9-i586',		'mono'],
	['2.0',		'sles-9-x86_64',	'mono'],
	['mono-basic',	'sles-10-i586',	'mono-basic'],
	['olive',	'sles-10-i586',	'olive'],
]

# Collect latest
for a in status_config:
	versions = build.get_versions("HEAD", a[1], a[2])
	versions.reverse()

	dir = ""
	for v in versions:
		dir = "www/builds/HEAD/%s/%s/%s/files/steps/api-diff" % (a[1], a[2], v)
		if os.path.exists(dir):
			break
		else:
			print "Skipping: " + dir

	if dir:
		print dir
		a.append(dir)
	else:
		print "No valid api-diff steps for: " + a[0]


print status_config

# Copy to tmp
if not os.path.exists(output_dir): os.mkdir(output_dir)

for a in status_config:
	out = output_dir + os.sep + a[0]
	# If there's a valid step, copy it over
	if len(a) > 3:
		os.system('rm -Rf %s; cp -a %s %s' % (out, a[3], out) )

