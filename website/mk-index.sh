#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh



WEB_DIR=$1

cd $WEB_DIR

for distro_conf in $packagingdir/conf/*-*-*; do
	
	distro_info `basename $distro_conf`
	
	mkdir -p $DISTRO
	
	OUT=$DISTRO/index.html
	

	rm -rf $OUT
	
	cat $confdir/groups | while read line
	do
		if [ "x${line:0:1}" == "x#" ]; then
			package=$(echo ${line:1})

			. $packagingdir/defs/$package
			
			if ships_package; then
				get_destroot
		
				if [ ! -d $DEST_ROOT/$package/*/ ]; then 
							
					VERSION=`ls -d $DEST_ROOT/$package/*/ -t -1 | head -n1`
						
					for i in $VERSION/*.rpm; do
					
						[[ $i == *.src.rpm ]] && continue
						
						base=`basename $i`
						
						echo "<ul><a href='../$i'>$base</a></ul>" >> $OUT
					done
				fi
			fi
			
		elif [ "x${line:0:1}" == "x!" ]; then
			line=$(echo ${line:1})
			
			. $confdir/$line >> $OUT
			
		else
			echo ${line//\\[\\[arch\\]\\]/$(basename $distro_conf)} >> $OUT
		fi
	done
done