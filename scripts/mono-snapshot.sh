#!/bin/bash -ex

SCRIPTS_DIR=$(dirname $(which $0))
HOMEDIR=$(dirname $(which $0))/daily_build
DATE=`date +'%Y%m%d'`

# Do the logfile the right way, with I/O redirection!
set -ex
LOGFILE="$HOMEDIR/src/$DATE.log"
exec 1> $LOGFILE # STDOUT > LOGFILE
exec 2>&1 # STDERR > STDOUT (> LOGFILE)

## Script to build mono/mcs and create daily mono tarballs
unset MONO_PATH
unset LD_LIBRARY_PATH
REPO=$HOMEDIR/src/repo
DAILY_BUILD_DIR=$HOMEDIR/src/build
PREFIX=$HOMEDIR/src/install
#export PATH=$PREFIX/bin:$PATH

GIT_BASE="git://github.com/mono"

# Clean up and set up new dir
rm -Rf $DAILY_BUILD_DIR
rm -Rf $PREFIX
mkdir -p $DAILY_BUILD_DIR

# Check out repo source if it doesn't exist
if [ ! -e $REPO ] ; then
	mkdir -p $REPO
	cd $REPO
	echo "Clone mono and mono-basic"
	git clone --quiet --no-checkout $GIT_BASE/mono.git
	git clone --quiet --no-checkout $GIT_BASE/mono-basic.git

# Otherwise update the repo
else
	echo "Updating repos"
	cd $REPO/mono
	git fetch --quiet
	cd ../mono-basic
	git fetch --quiet
fi

# rsync the clean source
echo "Copy fresh source..."
cd $REPO/mono
mkdir -p $DAILY_BUILD_DIR/mono
git archive origin/master | tar -x -C $DAILY_BUILD_DIR/mono
cd ../mono-basic
mkdir -p $DAILY_BUILD_DIR/mono-basic
git archive origin/master | tar -x -C $DAILY_BUILD_DIR/mono-basic

# Bump mono version number
echo "Bump mono version number"
(cd $DAILY_BUILD_DIR/mono && sed -i "s/\(AM_INIT_AUTOMAKE.*\))/AM_INIT_AUTOMAKE\(mono,$DATE)/" configure.in )

# Build mono
echo "Building MONO"
(cd $DAILY_BUILD_DIR/mono && ./autogen.sh --prefix=$PREFIX)

(cd $DAILY_BUILD_DIR/mono && make)

# Install mono
echo "Installing mono"
(cd $DAILY_BUILD_DIR/mono && make install)

export LD_LIBRARY_PATH="$PREFIX/lib:$LD_LIBRARY_PATH"
export C_INCLUDE_PATH="$PREFIX/include"
export ACLOCAL_PATH="$PREFIX/share/aclocal"
export PKG_CONFIG_PATH="$PREFIX/share/pkgconfig:$PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH"
export PATH="$PREFIX/bin:$PATH"

# Build and install basic
echo "Building basic"
(cd $DAILY_BUILD_DIR/mono-basic && ./configure --prefix=$PREFIX)
(cd $DAILY_BUILD_DIR/mono-basic && make)
(cd $DAILY_BUILD_DIR/mono-basic && make install)
# Copy the basic runtime to where the mcs class libs are so the class status will get properly generated
cp $DAILY_BUILD_DIR/mono-basic/class/lib/vbnc/*.dll $DAILY_BUILD_DIR/mono/mcs/class/lib/net_2_0

LIBSDIR=$DAILY_BUILD_DIR/mono/mcs/class/lib/basic
cd $DAILY_BUILD_DIR
# make monolite tarball
MONO_CORLIB_VERSION=$(sed -n "s/\#define MONO_CORLIB_VERSION //p" $DAILY_BUILD_DIR/mono/mono/metadata/appdomain.c)
MONOLITE=monolite-$MONO_CORLIB_VERSION-$DATE
mkdir -p $DAILY_BUILD_DIR/$MONOLITE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/Mono.Security.dll $LIBSDIR/System.Xml.dll $LIBSDIR/System.Core.dll $LIBSDIR/mcs.exe $DAILY_BUILD_DIR/$MONOLITE

tar zcvpf $MONOLITE.tar.gz $MONOLITE/

# make monocharge tarball
mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE

# install script and readme
cp $HOMEDIR/../monocharge/* $DAILY_BUILD_DIR/monocharge-$DATE

# NET 1.0
#mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE/1.0
#cp $PREFIX/lib/mono/1.0/*.exe $DAILY_BUILD_DIR/monocharge-$DATE/1.0
#cp $DAILY_BUILD_DIR/mono/mcs/class/lib/net_1_1/*.dll $DAILY_BUILD_DIR/monocharge-$DATE/1.0

# NET 2.0
mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE/2.0
cp $PREFIX/lib/mono/2.0/*.exe $DAILY_BUILD_DIR/monocharge-$DATE/2.0
cp $DAILY_BUILD_DIR/mono/mcs/class/lib/net_2_0/*.dll $DAILY_BUILD_DIR/monocharge-$DATE/2.0
cp $DAILY_BUILD_DIR/mono-basic/class/lib/vbnc/*.dll $DAILY_BUILD_DIR/monocharge-$DATE/2.0

tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/

# Make mono tarball
(cd $DAILY_BUILD_DIR/mono && make dist-bzip2)

# Copy resulting tarball to top-level dir
echo "Copy resulting tarball to top-level dir"
(cd $DAILY_BUILD_DIR/mono && cp *.tar.bz2 *.tar.gz $DAILY_BUILD_DIR )

echo "Copying daily files..."
scp -i $SCRIPTS_DIR/key/cron_key  *.tar.bz2 *.tar.gz mono-web@mono.ximian.com:go-mono/daily

# Run command to update webpage
ssh -i $SCRIPTS_DIR/key/cron_key mono-web@mono.ximian.com "release/scripts/make-html"

# Upload assemblies to class status page
echo "Updating class status pages..."
HOST="mono-web@www.go-mono.com:/srv/www/htdocs/mono-website/go-mono/status/binary/"
for profile in net_2_0:2.0 net_3_5:3.5 net_4_0:4.0; do
	SRC="$(echo $profile | cut -d : -f 1)"
	DEST="$(echo $profile | cut -d : -f 2)"
	scp -i $SCRIPTS_DIR/key/cron_key -q -C -o StrictHostKeyChecking=no $DAILY_BUILD_DIR/mono/mcs/class/lib/$SRC/*.dll $HOST/$DEST/
done

# Keep log around, but compress it
echo "Compressing log..."
bzip2 $LOGFILE
