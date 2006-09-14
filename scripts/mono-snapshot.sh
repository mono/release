#!/bin/sh -e

SCRIPTS_DIR=$(dirname $(which $0))
HOMEDIR=$(dirname $(which $0))/daily_build

## Script to build mono/mcs and create daily mono tarballs
unset MONO_PATH
unset LD_LIBRARY_PATH
DATE=`date +'%Y%m%d'`
REPO=$HOMEDIR/src/repo
DAILY_BUILD_DIR=$HOMEDIR/src/build
PREFIX=$HOMEDIR/src/install
export PATH=$PREFIX/bin:$PATH
export PKG_CONFIG_PATH=/opt/gnome/lib/pkgconfig
#export JAVA_HOME=/incoming/tmpinst/j2sdk1.4.1_03
#export BB_REPODIR=/nfs/release/source_repository

MSVN="svn://svn.myrealbox.com/source"
LOGFILE="$HOMEDIR/src/$DATE.log"

# Clean up and set up new dir
rm -Rf $DAILY_BUILD_DIR
rm -Rf $PREFIX
mkdir -p $DAILY_BUILD_DIR

# Start log
echo > $LOGFILE

# Check out repo source if it doesn't exist
if [ ! -e $REPO ] ; then
	mkdir -p $REPO
	cd $REPO
	echo "Check out mono and mcs" >> $LOGFILE 2>&1
	svn co -q $MSVN/trunk/mono >> $LOGFILE 2>&1 || exit 1
	svn co -q $MSVN/trunk/mcs >> $LOGFILE 2>&1 || exit 1

# Otherwise update the repo
else
	echo "Updating repo" >> $LOGFILE 2>&1
	cd $REPO/mono
	svn switch $MSVN/trunk/mono >> $LOGFILE 2>&1 || exit 1
	cd ../mcs
	svn switch $MSVN/trunk/mcs >> $LOGFILE 2>&1 || exit 1
fi

# rsync the clean source
echo "Copy fresh source..." >> $LOGFILE 2>&1
cd $DAILY_BUILD_DIR
rsync -a --exclude '.svn/' $REPO/* .

# Bump mono version number
echo "Bump mono version number" >> $LOGFILE 2>&1
(cd $DAILY_BUILD_DIR/mono && cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp && mv configure.tmp configure.in ) >> $LOGFILE 2>&1

# Build mono
echo "Building MONO" >> $LOGFILE 2>&1
(cd $DAILY_BUILD_DIR/mono && ./autogen.sh --prefix=$PREFIX || exit 1 ) >> $LOGFILE 2>&1

(cd $DAILY_BUILD_DIR/mono && make || exit 1 ) >> $LOGFILE 2>&1

# Install mono
echo "Installing mono" >> $LOGFILE 2>&1
(cd $DAILY_BUILD_DIR/mono && make install || exit 1 ) >> $LOGFILE 2>&1

LIBSDIR=$DAILY_BUILD_DIR/mcs/class/lib/net_1_1_bootstrap
cd $DAILY_BUILD_DIR
# make monolite tarball
mkdir -p $DAILY_BUILD_DIR/monolite-$DATE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/Mono.Security.dll $LIBSDIR/System.Xml.dll $LIBSDIR/mcs.exe $DAILY_BUILD_DIR/monolite-$DATE

tar zcvpf monolite-$DATE.tar.gz monolite-$DATE/ >> $LOGFILE 2>&1

# make monocharge tarball
mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE

# install script and readme
cp $HOMEDIR/../monocharge/* $DAILY_BUILD_DIR/monocharge-$DATE

# NET 1.0
mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE/1.0
cp $PREFIX/lib/mono/1.0/*.exe $DAILY_BUILD_DIR/monocharge-$DATE/1.0
cp $DAILY_BUILD_DIR/mcs/class/lib/default/*.dll $DAILY_BUILD_DIR/monocharge-$DATE/1.0

# NET 2.0
mkdir -p $DAILY_BUILD_DIR/monocharge-$DATE/2.0
cp $PREFIX/lib/mono/2.0/*.exe $DAILY_BUILD_DIR/monocharge-$DATE/2.0
cp $DAILY_BUILD_DIR/mcs/class/lib/net_2_0/*.dll $DAILY_BUILD_DIR/monocharge-$DATE/2.0

tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/ >> $LOGFILE 2>&1

# Make mono tarball and check
#(cd $DAILY_BUILD_DIR/mono && make distcheck || exit 1 ) >> $LOGFILE 2>&1
(cd $DAILY_BUILD_DIR/mono && make dist || exit 1 ) >> $LOGFILE 2>&1

# Copy resulting tarball to top-level dir
echo "Copy resulting tarball to top-level dir" >> $LOGFILE 2>&1
(cd $DAILY_BUILD_DIR/mono && cp *.tar.gz $DAILY_BUILD_DIR )
# Not sure what this is for
#(cd $DAILY_BUILD_DIR/mono && cp *mono-$DATE* $DAILY_BUILD_DIR )

echo "Copying daily files..." >> $LOGFILE 2>&1
scp -i $SCRIPTS_DIR/key/cron_key  *.tar.gz  mono-web@mono.ximian.com:go-mono/daily >> $LOGFILE 2>&1

# Run command to update webpage
ssh -i $SCRIPTS_DIR/key/cron_key mono-web@mono.ximian.com "go-mono/daily/make-html" >> $LOGFILE 2>&1

echo "Updating class status pages..." >> $LOGFILE 2>&1

cd $DAILY_BUILD_DIR
$SCRIPTS_DIR/class_status/update-status.sh 1.1 mono-HEAD-vs-fx-1-1 >> $LOGFILE 2>&1

cd $DAILY_BUILD_DIR
$SCRIPTS_DIR/class_status/update-status.sh 2.0 mono-HEAD-vs-fx-2 >> $LOGFILE 2>&1

# Keep log around, but compress it
echo "Compressing log..." >> $LOGFILE 2>&1
bzip2 $LOGFILE

