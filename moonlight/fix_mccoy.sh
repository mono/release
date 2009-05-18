#!/bin/bash

# This script applies a one-time patch for mccoy to run on the command line
# Pulled from https://bugzilla.mozilla.org/show_bug.cgi?id=396525#c7

if [ $# != 1 ]
then
	echo "Usage: $0 /path/to/mccoy"
	exit 1
fi

pushd $1

PATCH=mccoy.patch
curl -o $PATCH http://www.xuluwarrior.com/development/mccoy_cmdline_xuluwarrior.patch
dos2unix $PATCH

pushd chrome

cp mccoy.jar mccoy.jar.orig
unzip mccoy.jar

popd
patch -p0 < $PATCH || exit
pushd chrome
zip -r mccoy.jar content branding
popd
popd




