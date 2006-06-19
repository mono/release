#!/usr/bin/env python

import sys
sys.path += ['../']

import build

platform = 'suse-93-i586';
package = 'gecko-sharp-2.0';

version = build.get_latest_version('HEAD', platform, package)

print "version: " + version

