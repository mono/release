#!/bin/bash

#DO THIS AFTER SIGNING THE XPIS WITH NOVELL'S KEY

# All the signed .xpis must be in this directory when this script is run

# This script create four update.rdf files, one for each arch/profile pair. 


sha=`which sha1sum 2>/dev/null`
if [ "$sha" == "" ]
then
	echo "Missing dependancy: sha1sum"
	exit 5
fi

if [ "$#" == "0" ] 
then
	echo "usage:  ./create_update_rdfs.sh <version>"
	exit 1
fi

version=$1

rm -rf *.rdf

for arch in i586 x86_64 sparc ppc
do
	for prof in 1.0.1 2.0
	do
		xpi="novell-moonlight-$prof-$arch.xpi"
		
		if [ ! -f "$xpi" ]
		then
			echo "File missing: $xpi  -  Skipping update.rdf creation"
			continue
		fi

		rdf=update-$prof-$arch.rdf
		echo "Creating $rdf"

		hash_sum=`sha1sum $xpi | awk '{print $1}'`
		sed -e "s/{VERSION}/$version/" -e "s/{XPI}/$xpi/" -e "s/{HASH}/sha1:$hash_sum/" update.rdf.template > $rdf

	done
done
