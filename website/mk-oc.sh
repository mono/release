#!/bin/bash

confdir=$(dirname $(pwd)/$0)
. $confdir/distro-info.sh

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

		for distro_conf in $confdir/sources/*; do 
			distro_info `basename $distro_conf`
		
			grep -v "^#" $distro_conf | while read mod mloc
			do				
				if [ "x$package" = "x$mod" ]; then
					eval mloc=$mloc
					if [ ! -d $mloc/$mod/*/ ]; then
						continue
					fi
					
					VERSION=`ls -d $mloc/$mod/*/ -t -1 | head -n1`
					
					mkdir -p $chan/$DISTRO
					ln $VERSION/*.rpm $chan/$DISTRO
				fi
			done
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