##
## mono-snapshot.sh:Shell script for checking out and building mono/mcs and making daily release-style mono tarballs
##
## Authors: Duncan Mak <duncan@ximian.com>
##	    Sachin Kumar <skumar1@novell.com>
##          Roopa Wilson <wroopa@novell.com>
##	    Satya Sudha K <ksathyasudha@novell.com>
##	    Ritvik Mayank <mritvik@novell.com>
##

#!/bin/sh -e`


DATE=`date +'%Y%m%d'`
SNAPSHOT=/tmp/snapshot/$DATE
PREFIX=/tmp/prefix
export PATH=$PREFIX/bin:$PATH

# Setup new dir
mkdir -p $SNAPSHOT
cd $SNAPSHOT
echo > mono-log

# Check out mono and mcs
echo Check out mono and mcs
svn co svn+ssh://USER@mono-cvs.ximian.com/source/trunk/mono |tee -a mono-log
svn co svn+ssh://USER@mono-cvs.ximian.com/source/trunk/mcs |tee -a mono-log

# Bump mono version number
echo Bump mono version number | tee -a mono-log
(cd $SNAPSHOT/mono && cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp && mv configure.tmp configure.in ) | tee -a mono-log

# Build mono
echo Building MONO | tee -a mono-log
(cd $SNAPSHOT/mono && ./autogen.sh --prefix=$PREFIX --with-preview=yes && make || exit 1 ) | tee -a mono-log

# Install mono
echo Installing mono | tee -a mono-log
(cd $SNAPSHOT/mono && make install || exit 1 ) | tee -a mono-log

# Running make dist
echo Running make dist | tee -a mono-log
(cd $SNAPSHOT/mono && make dist || exit 1 ) | tee -a mono-log

# Copy resulting tarball to top-level dir
echo Copy resulting tarball to top-level dir | tee -a mono-log
(cd $SNAPSHOT/mono && cp *.tar.gz $SNAPSHOT )

LIBSDIR=$SNAPSHOT/mcs/class/lib/net_1_1_bootstrap

# make monolite tarball
cd $SNAPSHOT
mkdir $SNAPSHOT/monolite-$DATE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/Mono.Security.dll $LIBSDIR/System.Xml.dll $LIBSDIR/mcs.exe $SNAPSHOT/monolite-$DATE
tar zcvpf monolite-$DATE.tar.gz monolite-$DATE/ | tee -a mono-log

# make monocharge tarball
mkdir $SNAPSHOT/monocharge-$DATE

# Install script and readme
cp /home/sudha/scripts/monocharge/* $SNAPSHOT/monocharge-$DATE

# Copy the files for NET 1.0
mkdir -p $SNAPSHOT/monocharge-$DATE/1.0
cp $PREFIX/lib/mono/1.0/*.exe $SNAPSHOT/monocharge-$DATE/1.0
cp $SNAPSHOT/mcs/class/lib/default/*.dll $SNAPSHOT/monocharge-$DATE/1.0

# Copy the files for NET 2.0
mkdir -p $SNAPSHOT/monocharge-$DATE/2.0
cp $PREFIX/lib/mono/2.0/*.exe $SNAPSHOT/monocharge-$DATE/2.0
cp $SNAPSHOT/mcs/class/lib/net_2_0/*.dll $SNAPSHOT/monocharge-$DATE/2.0

tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/ | tee -a mono-log

# Upload the tarballs on go-mono/daily
scp -i /home/sudha/tmp/ssh/cron_dsa  *.tar.gz  mono-web@mono.ximian.com:go-mono/daily 
