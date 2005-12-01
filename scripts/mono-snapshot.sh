#!/bin/sh -e

HOMEDIR=$(dirname $(which $0))/daily_build

## Script to build mono/mcs and create daily mono tarballs
unset MONO_PATH
unset LD_LIBRARY_PATH
DATE=`date +'%Y%m%d'`
SNAPSHOT=$HOMEDIR/src/$DATE
PREFIX=$HOMEDIR/src/install
export PATH=$PREFIX/bin:$PATH
export PKG_CONFIG_PATH=/opt/gnome/lib/pkgconfig
#export JAVA_HOME=/incoming/tmpinst/j2sdk1.4.1_03
#export BB_REPODIR=/nfs/release/source_repository

# Setup new dir
mkdir -p $SNAPSHOT
cd $SNAPSHOT
echo > mono-log

# Check out mono and mcs
echo Check out mono and mcs
svn export -q svn://svn.myrealbox.com/source/trunk/mono |tee -a mono-log
svn export -q svn://svn.myrealbox.com/source/trunk/mcs |tee -a mono-log

#Create Backup of the checkout
echo Creating Backup for todays checkout | tee -a mono-log
#(cd $HOMEDIR/src && tar -czvf $DATE.tar.gz $DATE/) 
echo Finshed creating backups | tee -a mono-log

# Bump mono version number
#echo Bump mono version number | tee -a mono-log
(cd $SNAPSHOT/mono && cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp && mv configure.tmp configure.in ) | tee -a mono-log

# Build mono
echo Building MONO | tee -a mono-log
(cd $SNAPSHOT/mono && ./autogen.sh --prefix=$PREFIX || exit 1 ) | tee -a mono-log

(cd $SNAPSHOT/mono && make || exit 1 ) | tee -a mono-log

# Install mono
echo Installing mono | tee -a mono-log
(cd $SNAPSHOT/mono && make install || exit 1 ) | tee -a mono-log

LIBSDIR=$SNAPSHOT/mcs/class/lib/net_1_1_bootstrap
cd $SNAPSHOT
# make monolite tarball
mkdir $SNAPSHOT/monolite-$DATE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/Mono.Security.dll $LIBSDIR/System.Xml.dll $LIBSDIR/mcs.exe $SNAPSHOT/monolite-$DATE

tar zcvpf monolite-$DATE.tar.gz monolite-$DATE/ | tee -a mono-log

# make monocharge tarball
mkdir $SNAPSHOT/monocharge-$DATE

# install script and readme
cp $HOMEDIR/../monocharge/* $SNAPSHOT/monocharge-$DATE

# NET 1.0
mkdir -p $SNAPSHOT/monocharge-$DATE/1.0
cp $PREFIX/lib/mono/1.0/*.exe $SNAPSHOT/monocharge-$DATE/1.0
cp $SNAPSHOT/mcs/class/lib/default/*.dll $SNAPSHOT/monocharge-$DATE/1.0

# NET 2.0
mkdir -p $SNAPSHOT/monocharge-$DATE/2.0
cp $PREFIX/lib/mono/2.0/*.exe $SNAPSHOT/monocharge-$DATE/2.0
cp $SNAPSHOT/mcs/class/lib/net_2_0/*.dll $SNAPSHOT/monocharge-$DATE/2.0

tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/ | tee -a mono-log

# Make mono tarball and check
#(cd $SNAPSHOT/mono && make distcheck || exit 1 ) | tee -a mono-log
(cd $SNAPSHOT/mono && make dist || exit 1 ) | tee -a mono-log

# Copy resulting tarball to top-level dir
echo Copy resulting tarball to top-level dir | tee -a mono-log
(cd $SNAPSHOT/mono && cp *.tar.gz $SNAPSHOT )
# Not sure what this is for
#(cd $SNAPSHOT/mono && cp *mono-$DATE* $SNAPSHOT )

scp -i $HOMEDIR/../key/cron_key  *.tar.gz  mono-web@mono.ximian.com:go-mono/daily |tee -a mono-log

# Run command to update webpage
ssh mono-web@mono.ximian.com "go-mono/daily/make-html" |tee -a mono-log

