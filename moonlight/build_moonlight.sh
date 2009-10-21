#!/bin/bash

source versions.sh

ARCH=$(uname -m | sed -e 's/i.86/i586/')

SRCDIR=$HOME/src/$PREVIEW

mkdir -p $SRCDIR


function fail
{
	echo "Failed: $1"
	exit 1
}

. ~/mono-dev-env || fail "Missing mono-dev-env"

cd $SRCDIR
rm -rf *tar.bz2
wget http://ftp.novell.com/pub/mono/sources/moon/$PREVIEW/moonlight-$PREVIEW.tar.bz2
wget http://ftp.novell.com/pub/mono/sources/moon/$PREVIEW/mono-2.5.tar.bz2

tar -xjf *.tar.bz2

cd $SRCDIR/$PREVIEW/mono-2.5
./configure && make && sudo make install || fail

# remove all .la files 
find $MONO_PREFIX /opt/mono -name "*.la" | xargs sudo rm -rf

cd $SRCDIR/$PREVIEW/moonlight-$PREVIEW
./configure --without-performance --without-testing && make && sudo make install || fail
make user-plugin || fail
rm -rf $HOME/*.xpi
cp plugin/install/novell-moonlight.xpi $HOME/novell-moonlight-$PREVIEW-$ARCH.xpi

cd $HOME

