#!/bin/bash

# MoonlightReleases.py needs to remain as a python module to be accessible
#  by other python scripts in this directory

# This script makes those vars accesible to bash scripts

data=$(python -c '
import MoonlightReleases

print "%(release)s %(monorev)s %(moonrev)s" % (MoonlightReleases.latest)

versions = ",".join(MoonlightReleases.old_versions)
print versions

')


PREVIEW=$(echo $data | awk '{print $1}')
MONOREV=$(echo $data | awk '{print $2}')
MOONREV=$(echo $data | awk '{print $3}')
OLD_VERSIONS=$(echo $data | awk '{print $4}')

