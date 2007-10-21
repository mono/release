#!/usr/bin/env python

import os
import shutil
import sys

sys.path.append("../pyutils")

import build

#output_dir = "tmp"
output_dir = "/var/www/mono-website/go-mono/class-status"

# Note: when modules start building on other distros, these need to be updated
# The wiki page pointing to these will also need to be updated
status_config = [
	['1.1',		'sles-9-i586',		'mono'],
	['2.0',		'sles-9-x86_64',	'mono'],
	['mono-basic',	'suse-100-i586',	'mono-basic'],
	['olive',	'suse-100-i586',	'olive'],
]

# Collect latest
for a in status_config:
	latest = build.get_latest_version("HEAD", a[1], a[2])
	dir = "www/builds/HEAD/%s/%s/%s/files/steps/api-diff" % (a[1], a[2], latest)
	if os.path.exists(dir):
		print dir
		a.append(dir)
	else:
		print dir + " doesn't exist"

print status_config

# Copy to tmp
if not os.path.exists(output_dir): os.mkdir(output_dir)

for a in status_config:
	out = output_dir + os.sep + a[0]
	os.system('rm -Rf %s; cp -a %s %s' % (out, a[3], out) )

