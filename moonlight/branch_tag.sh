#!/bin/bash

# Get these revision numbers from #moonlight
MONOREV=135039
MOONREV=135062

#------------------------------------------------------------------

VERSIONS=$(cat VERSIONS)  #read versions from file
PREVIEW=$(echo $VERSIONS | awk '{print $NF}')

echo -e "\n      PREVIEW = $PREVIEW"
echo -e "     Mono Rev = $MONOREV"
echo -e "Moonlight Rev = $MOONREV \n"

echo -n "Continue branching for Preview $PREVIEW? (yes,NO): "
read -e CHAR

if [ x$CHAR != xyes ]
then
	echo "Aborting branch"
	exit 1
fi

echo "Branching Moonlight $PREVIEW"

HOST=svn+ssh://rhowell@mono-cvs.ximian.com/source
MONO=$HOST/trunk/mono
MCS=$HOST/trunk/mcs
MOON=$HOST/trunk/moon
MONOBASIC=$HOST/trunk/mono-basic
BRANCH=$HOST/branches/moon/$PREVIEW


# Create the branch
svn mkdir -m " * Creating branch for Moonlight $PREVIEW" $BRANCH

svn cp -m " * Branching mono r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MONO $BRANCH
svn cp -m " * Branching mcs r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MCS $BRANCH
svn cp -m " * Branching moon r$MOONREV for Moonlight $PREVIEW" -r$MOONREV $MOON $BRANCH
svn cp -m " * Branching mono-basic for Moonlight $PREVIEW" -rHEAD $MONOBASIC $BRANCH

