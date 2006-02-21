#!/bin/bash

if test "$1" = "1.1" ; then
	INFO=./mono-api-info.exe
else
	if test "$1" = "2.0" ; then
		INFO=./mono-api-info2.exe
	else
		echo "Need 1.1 or 2.0"
		exit 1
	fi
fi

if test "$#" -ne 2 ;
then
	echo "Syntax: $0 (1.1|2.0) listfile"
	exit 1
fi

rm -rf $1
mkdir $1 || exit 1

for i in $(cat $2)
do
	echo $i
	$INFO $i > $1/$i.xml
done

