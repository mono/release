#!/bin/sh

##  Shell script for making daily libgdiplus tarballs
##  Assumption: Cairo is already installed.
 

DATE=`date +'%Y%m%d'`
SNAPSHOT=/home/build/src/$DATE
PREFIX=/home/build/src/install
export MONO_PATH=$PREFIX/lib
export PATH=$PREFIX/bin:$PATH

# Setup new dir
mkdir -p $SNAPSHOT
cd $SNAPSHOT
echo > libgdiplus-log

# Check out libgdiplus
#echo Checkout libgdiplus module 
svn co svn://anonsvn.mono-project.com/source/trunk/libgdiplus 2>&1 >> libgdiplus-log
#svn co svn+ssh://mritvik@mono-cvs.ximian.com/source/trunk/libgdiplus 2>&1 >> libgdiplus-log
#echo libgdipuls got checked out

#mv libgdiplus/ltmain.sh libgdiplus/ltmain.sh.old

# Bump libgdiplus version number
echo Bump libgdiplus version number
(cd $SNAPSHOT/libgdiplus && cat configure.in | sed "s/\(AM_INIT_AUTOMAKE.*\))/\1.$DATE)/" > configure.tmp && mv configure.tmp configure.in || exit 1 ) 2>&1 >> libgdiplus-log

#Create Backup of the checkout
echo Creating Backup for todays checkout | tee -a mono-log
(cd /tmp/snapshot/$DATE && tar -czvf libgdiplus.tar.gz libgdiplus/ && mv libgdiplus.tar.gz ../)
echo Finshed creating backups for libgdiplus | tee -a mono-log

# Build libgdiplus
echo Building libgdiplus
(cd $SNAPSHOT/libgdiplus && ./autogen.sh --prefix=$PREFIX && make && make install || exit 1)  2>&1 >> libgdiplus-log

# Running make distcheck: not working 
#echo Running make distcheck
#(cd $SNAPSHOT/libgdiplus && make distcheck  || exit 1 )  2>&1 >> libgdiplus-log 

# Copy resulting tarball to top-level dir
#echo Copying resulting tarball to top-level dir.
#(cd $SNAPSHOT/libgdiplus && cp *.tar.gz $SNAPSHOT )  2>&1 >> libgdiplus-log
