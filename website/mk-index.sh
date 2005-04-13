#!/bin/sh

confdir=$(dirname $(pwd)/$0)
. $confdir/distro-info.sh



WEB_DIR=$1

cd $WEB_DIR

for distro_conf in $confdir/sources/*; do 
	
	distro_info `basename $distro_conf`
	
	mkdir -p $DISTRO
	
	OUT=$DISTRO/index.html
	

	rm -rf $OUT
	
	cat $confdir/groups | while read line
	do
		if [ "x${line:0:1}" == "x#" ]; then
			line=$(echo ${line:1})
			
			grep -v "^#" $distro_conf | while read mod mloc
			do
				if [[ x$line = x$mod ]]; then
					
					eval mloc=$mloc
					if [ ! -d $mloc/$mod/*/ ]; then
						continue
					fi
					
					VERSION=`ls -d $mloc/$mod/*/ -t -1 | head -n1`
					VERSION=`dirname $VERSION`/`basename $VERSION`
					
					for i in $VERSION/*.rpm; do
						base=`basename $i`
						
						echo "<ul><a href='../$i'>$base</a></ul>" >> $OUT
					done
				fi
			done
		elif [ "x${line:0:1}" == "x!" ]; then
			line=$(echo ${line:1})
			
			sh $confdir/$line >> $OUT
			
		else
			echo ${lline//\\[\\[arch\\]\\]/$(basename $distroconf)} >> $OUT
		fi
	done
done