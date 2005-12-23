#!/bin/bash

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh

WEB_DIR=$1
serverconf=$2
cd $WEB_DIR

rm -rf server.conf

cp $confdir/oc-config/distributions.xml .

cat $confdir/oc-config/$serverconf.conf | while read line; do
	if [ "x${line:0:1}" != "x!" ]; then
		echo $line >> server.conf
		continue
	fi
	#trim whitespace
	chan=$(echo ${line:1})
	echo "AddChannel $chan" >> server.conf
	
	rm -rf $chan
	mkdir $chan
	
	cat $confdir/oc-config/$chan.chan | while read lline; do

		# If line starts with '+'
		if [ "x${lline:0:1}" == "x+" ]; then

			external_dir=$(echo ${lline:1})

			for distro_conf in $packagingdir/conf/*-*-* ; do

				# Only do this for non-zip package type distros
				! egrep "^USE_ZIP_PKG" $distro_conf > /dev/null 2>&1 || continue

				distro_info `basename $distro_conf`

				mkdir -p $chan/$DISTRO

				for rpm_file in `ls $external_dir/$DISTRO/*.rpm 2> /dev/null ` ; do
					# Skip source rpms
					if [ ${rpm_file//\.src\.rpm/} != $rpm_file ] ; then
						continue
					fi

					# Add rpm to the channel distro
					ln $rpm_file $chan/$DISTRO
				done

			done
			continue
		fi


		# If line doesn't start with '!' (Normal text)
		if [ "x${lline:0:1}" != "x!" ]; then
			echo ${lline//\\[\\[name\\]\\]/$serverconf} >> $chan/channel.conf
			continue
		fi
		
		
		package=$(echo ${lline:1})

		. $packagingdir/defs/$package

		for distro_conf in $packagingdir/conf/*-*-*; do 

			# Skip the distros that use zip packaging system
			! egrep "^USE_ZIP_PKG" $distro_conf > /dev/null 2>&1 || continue

			distro_info `basename $distro_conf`
			ships_package || continue
			get_destroot

			latest_version $DEST_ROOT/$package || continue
					
			mkdir -p $chan/$DISTRO
			ln $LATEST_VERSION/*.rpm $chan/$DISTRO
		done		
	done
	
	
	for i in $chan/*-*-*; do

		# Skip distros that use zip packaging system
		! egrep "^USE_ZIP_PKG" $i > /dev/null 2>&1 || continue

		distro_info `basename $i`
		
		DISTRO_STRING=$DISTRO
		
		for a in ${DISTRO_ALIASES[@]}; do
			DISTRO_STRING="$DISTRO_STRING:$a"
		done
		
		echo "AddDistro $DISTRO_STRING $DISTRO" >> $chan/channel.conf
		
		case $DISTRO in
			fedora-* )
				createrepo $i
			;;
		esac
		
	done
done

open-carpet
