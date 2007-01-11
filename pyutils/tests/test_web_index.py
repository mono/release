#!/usr/bin/env python

import sys

import pdb

sys.path += [ ".." ]

import build

print "Platforms:"
objs = build.get_platform_objs()
for i in objs:
	print i.name

print "packs:"
objs2, objs3 = build.get_package_objs()
for i in objs2:
	print i.name

print "noarch packs:"
for i in objs3:
	print i.name
