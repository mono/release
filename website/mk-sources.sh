#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh

WEB_DIR=$1

cd $WEB_DIR
OUT=index.html
rm $OUT

cat $confdir/sources | while read line
do
	if [ "x${line:0:1}" == "x#" ]; then
		ARGS=(${line:1})
		TARBALLS=()
		for package in ${ARGS[@]}; do 
			
			if [[ x$package == xgtk-sharp-2.0 ]]; then
				latest_tarball "$package/gtk-sharp-2.3.*.tar.gz"
				TARBALLS=(${TARBALLS[@]} $LATEST_VERSION)
			fi
			
			latest_tarball "$package/*.tar.gz"
			
			TARBALLS=(${TARBALLS[@]} $LATEST_VERSION)
		done
		echo ${TARBALLS[@]}
		echo "<ul>" >> $OUT
		for i in ${TARBALLS[@]}; do
			n=$(basename $i)
			echo "<li><a href='$i'>$n</a></li>" >> $OUT
		done
		
		echo "</ul>" >> $OUT
	else
		echo ${line} >> $OUT
	fi
done
