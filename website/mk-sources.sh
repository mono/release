#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh

WEB_DIR=$1
VERSION=$2

if test x$VERSION = x; then
	echo "Usage: mk-sources.sh <web_dir> <version>"
	exit 1
fi


# Also generate a sources index for archive history
mkdir -p $WEB_DIR/../archive/$VERSION/sources

cd $WEB_DIR
OUT=index.html
HISTORY_OUT=../archive/$VERSION/sources/index.html
rm -f $OUT
rm -f $HISTORY_OUT

cat $confdir/sources | while read line
do
	if [ "x${line:0:1}" == "x#" ]; then
		ARGS=(${line:1})
		TARBALLS=()
		for package in ${ARGS[@]}; do 
			
			if [[ x$package == xgtk-sharp-2.0 ]]; then
				latest_tarball "$package/gtk-sharp-2.4.*.tar.gz"
			else
				latest_tarball "$package/*"
			fi
			
			TARBALLS=(${TARBALLS[@]} $LATEST_VERSION)
		done
		echo ${TARBALLS[@]}
		echo "<ul>" >> $OUT
		echo "<ul>" >> $HISTORY_OUT
		for i in ${TARBALLS[@]}; do
			n=$(basename $i)
			echo "<li><a href='$i'>$n</a></li>" >> $OUT
			echo "<li><a href='../../../sources/$i'>$n</a></li>" >> $HISTORY_OUT
		done
		
		echo "</ul>" >> $OUT
		echo "</ul>" >> $HISTORY_OUT
	else
		line=${line//\\[\\[version\\]\\]/$VERSION}

		echo $line >> $OUT
		echo $line >> $HISTORY_OUT
	fi
done
