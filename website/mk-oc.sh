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
	echo "AddChannel $chan.conf" >> server.conf
	
	rm -rf $chan.conf
	
	cat $confdir/oc-config/$chan.chan | while read lline; do
		if [ "x${lline:0:1}" != "x!" ]; then
			echo ${lline//\\[\\[name\\]\\]/$serverconf} >> $chan.conf
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
					
					echo "AddDistro $DISTRO $VERSION" >> $chan.conf
				fi
			done
		done
		
	done
done

open-carpet