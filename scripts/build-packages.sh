#!/bin/sh

## Script to submit a mono tarball to repoman, 
## update module version in conf file,
## and submit a build request to the BB daemon

DATE=`date +'%Y%m%d'`
SNAPSHOT=/tmp/snapshot/$DATE
export CVS_RSH=/home/skumar/bin/ssh_wrapper
export CVSROOT=sachin@cvs.ximian.com:/cvs/helix-gnome
export BB_REPODIR=/nfs/release/source_repository/
. ./build-package.settings

cd $SNAPSHOT
MONOTAR=`ls mono-*.tar.gz`
echo Mono daily tarball: $MONOTAR

# Submit a tarball to repoman
#bb_submit $MONOTAR || echo Could not submit tarball ; exit 1

# get version
VERSION=`echo $MONOTAR | sed "s/mono-\(.*\)\.tar\.gz/\1/"`
echo Verion: $VERSION

mkdir -p $SNAPSHOT/tmp
cd $SNAPSHOT/tmp

# check out mono-conf module
cvs -z3 co mono-conf/mono

cd mono-conf/mono

# Update version in conf file
perl -pi -e "s,<version>.*</version>,<version>$VERSION</version>," ximian-build.conf

# Update source file in mono-conf
perl -pi -e "s,<i>mono-.*\.tar\.gz.*</i>,<i>$MONOTAR-1</i>," ximian-build.conf

# commit the update version to cvs
cvs commit -m "Update version in conf file" ximian-build.conf

# Remove the tmp dir
cd $SNAPSHOT
rm -rf tmp

# submit request to BB to build mono rpms
bb_client -m $BUILD_MASTER -t redhat-9-i386 -u $USER -p $PASSWORD --cvsroot 'distro@cvs.ximian.com:/cvs/helix-gnome' --cvsmodule mono-conf mono > jobid
