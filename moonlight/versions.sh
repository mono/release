#!/bin/bash

# MoonlightReleases.py needs to remain as a python module to be accessible
#  by other python scripts in this directory

# This script makes those vars accesible to bash scripts

data=$(python -c '
import MoonlightReleases

print "%(release)s %(monorev)s %(moonrev)s" % (MoonlightReleases.latest)

versions = ""
tmp_releases = MoonlightReleases.releases.keys()
tmp_releases.sort()

for release in tmp_releases:
	if release != MoonlightReleases.latest["release"]:
		versions += release + ","

print versions[0:-1] # dont print out the last comma

')


PREVIEW=$(echo $data | awk '{print $1}')
MONOREV=$(echo $data | awk '{print $2}')
MOONREV=$(echo $data | awk '{print $3}')
OLD_VERSIONS=$(echo $data | awk '{print $4}')

