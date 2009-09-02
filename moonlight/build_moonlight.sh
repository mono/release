#!/bin/bash

source versions.sh

ARCH=$(uname -m | sed -e 's/i.86/i586/')

SRCDIR=$HOME/src


function fail
{
	echo "Failed: $1"
	exit 1
}

. ~/mono-dev-env || fail "Missing mono-dev-env"

cd $SRCDIR
svn co svn://anonsvn.mono-project.com/source/branches/moon/$PREVIEW

cd $SRCDIR/$PREVIEW/mono
./autogen.sh && make && sudo make install || fail

# remove all .la files 
find $MONO_PREFIX /opt/mono -name "*.la" | xargs sudo rm -rf

cd $SRCDIR/$PREVIEW/moon
./autogen.sh --without-performance --without-testing && make && sudo make install || fail
make user-plugin || fail
rm -rf $HOME/*.xpi
cp plugin/install/novell-moonlight.xpi $HOME/novell-moonlight-$PREVIEW-$ARCH.xpi

cd $HOME

