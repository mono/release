#!/bin/sh -e

HOMEDIR=$(dirname $(which $0))/daily_build

## Script to build mono/mcs and create daily mono tarballs
unset MONO_PATH
unset LD_LIBRARY_PATH
DATE=`date +'%Y%m%d'`
REPO=$HOMEDIR/src/repo
DAILY_BUILDIR=$HOMEDIR/src/build
PREFIX=$HOMEDIR/src/install
export PATH=$PREFIX/bin:$PATH
export PKG_CONFIG_PATH=/opt/gnome/lib/pkgconfig
#export JAVA_HOME=/incoming/tmpinst/j2sdk1.4.1_03
#export BB_REPODIR=/nfs/release/source_repository

export MSVN="svn://svn.myrealbox.com/source"
export LOGFILE="$HOMEDIR/src/$DATE.log"

# Clean up and set up new dir
rm -Rf $DAILY_BUILDIR
rm -Rf $PREFIX
mkdir -p $DAILY_BUILDIR

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
cd $DAILY_BUILDIR
rsync -a --exclude '.svn/' $REPO/* .

# Bump mono version number
echo "Bump mono version number" >> $LOGFILE 2>&1
(cd $DAILY_BUILDIR/mono && cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp && mv configure.tmp configure.in ) >> $LOGFILE 2>&1

# Build mono
echo "Building MONO" >> $LOGFILE 2>&1
(cd $DAILY_BUILDIR/mono && ./autogen.sh --prefix=$PREFIX || exit 1 ) >> $LOGFILE 2>&1

(cd $DAILY_BUILDIR/mono && make || exit 1 ) >> $LOGFILE 2>&1

# Install mono
echo "Installing mono" >> $LOGFILE 2>&1
(cd $DAILY_BUILDIR/mono && make install || exit 1 ) >> $LOGFILE 2>&1

LIBSDIR=$DAILY_BUILDIR/mcs/class/lib/net_1_1_bootstrap
cd $DAILY_BUILDIR
# make monolite tarball
mkdir $DAILY_BUILDIR/monolite-$DATE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/Mono.Security.dll $LIBSDIR/System.Xml.dll $LIBSDIR/mcs.exe $DAILY_BUILDIR/monolite-$DATE

tar zcvpf monolite-$DATE.tar.gz monolite-$DATE/ >> $LOGFILE 2>&1

# make monocharge tarball
mkdir $DAILY_BUILDIR/monocharge-$DATE

# install script and readme
cp $HOMEDIR/../monocharge/* $DAILY_BUILDIR/monocharge-$DATE

# NET 1.0
mkdir -p $DAILY_BUILDIR/monocharge-$DATE/1.0
cp $PREFIX/lib/mono/1.0/*.exe $DAILY_BUILDIR/monocharge-$DATE/1.0
cp $DAILY_BUILDIR/mcs/class/lib/default/*.dll $DAILY_BUILDIR/monocharge-$DATE/1.0

# NET 2.0
mkdir -p $DAILY_BUILDIR/monocharge-$DATE/2.0
cp $PREFIX/lib/mono/2.0/*.exe $DAILY_BUILDIR/monocharge-$DATE/2.0
cp $DAILY_BUILDIR/mcs/class/lib/net_2_0/*.dll $DAILY_BUILDIR/monocharge-$DATE/2.0

tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/ >> $LOGFILE 2>&1

# Make mono tarball and check
#(cd $DAILY_BUILDIR/mono && make distcheck || exit 1 ) >> $LOGFILE 2>&1
(cd $DAILY_BUILDIR/mono && make dist || exit 1 ) >> $LOGFILE 2>&1

# Copy resulting tarball to top-level dir
echo "Copy resulting tarball to top-level dir" >> $LOGFILE 2>&1
(cd $DAILY_BUILDIR/mono && cp *.tar.gz $DAILY_BUILDIR )
# Not sure what this is for
#(cd $DAILY_BUILDIR/mono && cp *mono-$DATE* $DAILY_BUILDIR )

scp -i $HOMEDIR/../key/cron_key  *.tar.gz  mono-web@mono.ximian.com:go-mono/daily >> $LOGFILE 2>&1

# Run command to update webpage
ssh -i $HOMEDIR/../key/cron_key mono-web@mono.ximian.com "go-mono/daily/make-html" >> $LOGFILE 2>&1

# Keep log around, but compress it
bzip $LOGFILE

