#!/bin/bash


VERSIONS=$(cat VERSIONS)  #read versions from file
PREVIEW=$(echo $VERSIONS | awk '{print $NF}')
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

cd $SRCDIR/$PREVIEW/moon
./autogen.sh --without-performance --without-testing && make && sudo make install || fail
make user-plugin || fail
cp plugin/install/novell-moonlight.xpi ~/novell-moonlight-$PREVIEW-$ARCH.xpi

cd ~

