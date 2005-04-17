#!/bin/bash

confdir=$(dirname $(pwd)/$0)
packagingdir= $confdir/../packaging
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
		if [ "x${lline:0:1}" != "x!" ]; then
			echo ${lline//\\[\\[name\\]\\]/$serverconf} >> $chan/channel.conf
			continue
		fi
		
		
		package=$(echo ${lline:1})

		. $packagingdir/defs/$package

		for distro_conf in $packagingdir/conf/*-*-*; do 
			distro_info `basename $distro_conf`
			ships_package || continue
			get_destroot

			[ -d $DEST_ROOT/$mod/*/ ] || continue
					
			VERSION=`ls -d $DEST_ROOT/$mod/*/ -t -1 | head -n1`
					
			mkdir -p $chan/$DISTRO
			ln $VERSION/*.rpm $chan/$DISTRO
		done		
	done
	
	
	for i in $chan/*-*-*; do
		distro_info `basename $i`
		
		DISTRO_STRING=$DISTRO
		
		for a in ${DISTRO_ALIASES[@]}; do
			DISTRO_STRING="$DISTRO_STRING:$a"
		done
		
		echo "AddDistro $DISTRO_STRING $DISTRO" >> $chan/channel.conf 
	done
done

open-carpet