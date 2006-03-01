#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh

ARCHIVE_DIR=$1
VERSION=$2

if test x$VERSION = x; then
	echo "Usage: mk-history-index.sh <archive_dir> <version>"
	exit 1
fi

HISTORY_OUT=$ARCHIVE_DIR/$VERSION/download/index.html
rm -f $HISTORY_OUT

#### Sources ####
sources="<p> <a href='../sources'>Sources</a> </p>"


#### Installers ####
# Linux 
latest_version $ARCHIVE_DIR/$VERSION/linux-installer
revision=$(basename $LATEST_VERSION)
installer_dir="$ARCHIVE_DIR/$VERSION/linux-installer/$revision"
ref_dir="../linux-installer/$revision"

filename=$(basename $installer_dir/*.bin)
sum_filename=$(basename $installer_dir/*.md5)

installers="$installers <p>Linux Installer: <a href='$ref_dir/$filename'>$filename</a> [<a href='$ref_dir/$sum_filename'>MD5SUM</a>] </p>"

# Windows
latest_version $ARCHIVE_DIR/$VERSION/windows-installer
revision=$(basename $LATEST_VERSION)
installer_dir="$ARCHIVE_DIR/$VERSION/windows-installer/$revision"
ref_dir="../windows-installer/$revision"

filename=$(basename $installer_dir/*.exe)
sum_filename=$(basename $installer_dir/*.md5)

installers="$installers <p>Windows Installer: <a href='$ref_dir/$filename'>$filename</a> [<a href='$ref_dir/$sum_filename'>MD5SUM</a>] </p>"

# Mac
latest_version $ARCHIVE_DIR/$VERSION/macos-10-ppc
revision=$(basename $LATEST_VERSION)
installer_dir="$ARCHIVE_DIR/$VERSION/macos-10-ppc/$revision"
ref_dir="../macos-10-ppc/$revision"

filename=$(basename $installer_dir/*.dmg)
sum_filename=$(basename $installer_dir/*.md5)

installers="$installers <p>Mac OSX Installer: <a href='$ref_dir/$filename'>$filename</a> [<a href='$ref_dir/$sum_filename'>MD5SUM</a>] </p>"

#### Packages ####
packages="<ul>"

# Links to distros
for distro_conf in $packagingdir/conf/*-*-*; do

	# Skip the distros that use zip packaging system
	! egrep "^USE_ZIP_PKG" $distro_conf > /dev/null 2>&1 || continue

	distro_info `basename $distro_conf`

	packages="$packages <li><a href='$DISTRO'>$DISTRO</a></li>"
done

packages="$packages </ul>"

cat $confdir/history | while read line
do
	line=${line//\\[\\[version\\]\\]/$VERSION}
	line=${line//\\[\\[sources\\]\\]/$sources}
	line=${line//\\[\\[installers\\]\\]/$installers}
	line=${line//\\[\\[packages\\]\\]/$packages}

	echo $line >> $HISTORY_OUT
done

