##
##  Shell script for making daily release-style mono tarballs
##
##  Author: Duncan Mak <duncan@ximian.com>
##

#!/bin/sh

DATE=`date +'%Y%m%d'`
SNAPSHOT=/tmp/snapshot/$DATE

# setup user
export CVS_RSH=/home/duncan/bin/ssh_wrapper
export CVSROOT=duncan@mono-cvs.ximian.com:/cvs/public

# setup new dir
mkdir -p $SNAPSHOT
cd $SNAPSHOT

# check out mcs
cvs -z3 co mono mcs;

# bump mono version number
cd $SNAPSHOT/mono
cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp
mv configure.tmp configure.in

# bump mcs version number
cd $SNAPSHOT/mcs
cd mcs
cat AssemblyInfo.cs | sed "s/AssemblyVersion.*(\"\(.*\)\")/AssemblyVersion(\"\\1.$DATE\"\)/" > AssemblyInfo.tmp
mv AssemblyInfo.tmp AssemblyInfo.cs

# # build mcs
cd $SNAPSHOT/mcs
make prefix=/usr

# build mono
cd $SNAPSHOT/mono
./autogen.sh
make

# copy new mcs assemblies to the mono runtime dir.
cd $SNAPSHOT/mono/runtime
rm *.dll *.exe # remove existing assemblies
make prefix=/usr

# do a make dist
cd $SNAPSHOT/mono
make dist

# copy resulting tarball to top-level dir
cd $SNAPSHOT/mono
cp *.tar.gz /tmp/snapshot/$DATE/

# make monolite tarball
LIBSDIR=$SNAPSHOT/mcs/class/lib
mkdir $SNAPSHOT/monolite-$DATE
cp $LIBSDIR/mscorlib.dll $LIBSDIR/System.dll $LIBSDIR/System.Xml.dll $LIBSDIR/Mono.CSharp.Debugger.dll $SNAPSHOT/mcs/mcs/mcs.exe $SNAPSHOT/monolite-$DATE
cd $SNAPSHOT
tar zcvpf monolite-$DATE.tar.gz monolite-$DATE/

# make monocharge tarball
mkdir $SNAPSHOT/monocharge-$DATE
cp $SNAPSHOT/mono/runtime/*.dll $SNAPSHOT/mono/runtime/*.exe $SNAPSHOT/monocharge-$DATE
tar zcvpf monocharge-$DATE.tar.gz monocharge-$DATE/

# upload the new tarball
cd $SNAPSHOT
pwd
scp -i /home/duncan/.ssh/cron_rsa *.tar.gz mono-web@go-mono.com:go-mono/daily

# cleanup
rm -rf mcs mono
