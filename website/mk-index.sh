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
			ARGS=(${line:1})
			RPMS=()
			for package in ${ARGS[@]:1}; do 
				. $packagingdir/defs/$package
				
				ships_package || continue
				get_destroot
			
				latest_version $DEST_ROOT/$package/*/ || continue
						
				for i in $LATEST_VERSION/*.rpm; do
					[[ $i == *.src.rpm ]] && continue
					RPMS=(${RPMS[@]} $i)
				done
			done
			
			if [ ${#RPMS[@]} -eq 0 ]; then
				echo "<p>Not available for this platform</p>" >> $OUT
				continue
			fi
			
			zipname=${ARGS[0]}
			
			rm -rf $DISTRO/$zipname.zip
			# rpms are compressed anyways -- doing any compression is a waste of time
			zip -j -0 $DISTRO/$zipname.zip ${RPMS[@]}
			
			echo "<p><a href='$zipname.zip'><img src='/zip-icon.png' />All of these files in a ZIP file</a></p>" >> $OUT
			echo "<ul>" >> $OUT
			
			for i in ${RPMS[@]}; do
				NAME=$(rpm_query NAME $i)
				DESC=$(rpm_query SUMMARY $i)
				echo "<li><a href='../$i'>$NAME</a> -- $DESC</li>" >> $OUT
			done
			
			echo "</ul>" >> $OUT
			
		elif [ "x${line:0:1}" == "x!" ]; then
			line=$(echo ${line:1})
			
			. $confdir/$line >> $OUT
			
		else
			echo ${line//\\[\\[arch\\]\\]/$(basename $distro_conf)} >> $OUT
		fi
	done
done