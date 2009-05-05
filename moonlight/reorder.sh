#!/bin/bash

# The purpose of this is the recreate the zip with zigbert.rsa as 
# the first file in the zip. Firefox 3 requires this.
# https://developer.mozilla.org/en/Signing_a_XPI#Prepare_XPI_file_for_signing

if [ ! -e $1 ]
then
	echo "missing file $1"
fi

function reorder()
{
rm -rf tmp

unzip -d tmp $1

cd tmp
zip $1 META-INF/zigbert.rsa
zip $1 META-INF/zigbert.sf
zip $1 META-INF/manifest.mf

zip $1 chrome.manifest
zip $1 install.rdf

zip -r $1 plugins 
zip -r $1 skin

cd ..

mv $1 $1.orig
mv tmp/$1 .

rm -rf tmp

}

funtion unzip()
{
	unzip $1
}

reorder $1

