#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh


WEB_DIR=$1
VERSION=$2

if test x$VERSION = x; then
	echo "Usage: mk-index.sh <web_dir> <version>"
	exit 1
fi

cd $WEB_DIR

for distro_conf in $packagingdir/conf/*-*-*; do

	# Skip the distros that use zip packaging system
	! egrep "^USE_ZIP_PKG" $distro_conf > /dev/null 2>&1 || continue
	
	distro_info `basename $distro_conf`
	
	mkdir -p $DISTRO
	mkdir -p $WEB_DIR/../archive/$VERSION/download/$DISTRO
	
	OUT=$DISTRO/index.html
	HISTORY_OUT=$WEB_DIR/../archive/$VERSION/download/$DISTRO/index.html

	rm -rf $OUT
	rm -rf $HISTORY_OUT
	
	cat $confdir/groups | while read line
	do
		if [ "x${line:0:1}" == "x#" ]; then
			ARGS=(${line:1})
			RPMS=()
			SPECS=()
			for package in ${ARGS[@]:1}; do 
				. $packagingdir/defs/$package
				
				ships_package || continue
				get_destroot
			
				latest_version $DEST_ROOT/$package || continue
						
				for i in $LATEST_VERSION/*.rpm; do
					[[ $i == *.src.rpm ]] && continue
					RPMS=(${RPMS[@]} $i)
				done

				for i in $LATEST_VERSION/*.spec; do
					if [ -e $i ] ; then
						SPECS=(${SPECS[@]} $i)
					fi
				done

			done
			
			if [ ${#RPMS[@]} -eq 0 ]; then
				echo "<p>Not available for this platform</p>" >> $OUT
				echo "<p>Not available for this platform</p>" >> $HISTORY_OUT
				continue
			fi
			
			zipname=${ARGS[0]}
			
			rm -rf $DISTRO/$zipname.zip
			# rpms are compressed anyways -- doing any compression is a waste of time
			zip -j -0 $DISTRO/$zipname.zip ${RPMS[@]}
			
			echo "<p><a href='$zipname.zip'><img src='/zip-icon.png' />All of these RPMs in a ZIP file</a></p>" >> $OUT
			echo "<ul>" >> $OUT
			echo "<ul>" >> $HISTORY_OUT
			
			for i in ${RPMS[@]}; do
				NAME=$(rpm_query NAME $i)
				DESC=$(rpm_query SUMMARY $i)
				echo "<li><a href='../$i'>$NAME</a> -- $DESC</li>" >> $OUT
				echo "<li><a href='../../../../download/$i'>$NAME</a> -- $DESC</li>" >> $HISTORY_OUT
			done
			
			echo "</ul>" >> $OUT
			echo "</ul>" >> $HISTORY_OUT

			# Print links to spec files
			if [ ${#SPECS[@]} -eq 0 ]; then
				continue
			fi

			echo "<p>RPM Spec files: " >> $OUT
			echo "<p>RPM Spec files: " >> $HISTORY_OUT
			for i in ${SPECS[@]}; do
				NAME=$(basename $i)
				echo "<a href='../$i'>$NAME</a> " >> $OUT
				echo "<a href='../../../../download/$i'>$NAME</a> " >> $HISTORY_OUT
			done
			echo "</p>" >> $OUT
			echo "</p>" >> $HISTORY_OUT

			
		elif [ "x${line:0:1}" == "x!" ]; then
			line=$(echo ${line:1})
			
			. $confdir/$line >> $OUT

			# Provide url path for the HISTORY external deps
			if test x$line == xget_external_deps ; then
				EXTERNAL_PATH="../../../../external_packages"
			fi

			# Don't display repository information for history pages
			if test x$line != xget_rpm_install ; then
				. $confdir/$line >> $HISTORY_OUT
			fi

			unset EXTERNAL_PATH

		else
			line=${line//\\[\\[arch\\]\\]/$(basename $distro_conf)}
			line=${line//\\[\\[version\\]\\]/$VERSION}

			echo $line >> $OUT
			echo $line >> $HISTORY_OUT
		fi
	done
done
