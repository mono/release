#!/bin/bash

# Get these revision numbers from #moonlight

source versions.sh

echo -e "\n      PREVIEW = $PREVIEW"
echo -e "     Mono Rev = $MONOREV"
echo -e "Moonlight Rev = $MOONREV \n"

echo -n "Continue branching for Moonlight $PREVIEW? (yes,NO): "
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

echo      " * Branching mono r$MONOREV for Moonlight $PREVIEW"
svn cp -m " * Branching mono r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MONO $BRANCH

echo      " * Branching mcs r$MONOREV for Moonlight $PREVIEW"
svn cp -m " * Branching mcs r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MCS $BRANCH

echo      " * Branching moon r$MOONREV for Moonlight $PREVIEW"
svn cp -m " * Branching moon r$MOONREV for Moonlight $PREVIEW" -r$MOONREV $MOON $BRANCH

echo      " * Branching mono-basic r$MONOREV for Moonlight $PREVIEW"
svn cp -m " * Branching mono-basic r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MONOBASIC $BRANCH

# update the version numbers in configure.ac on branch and trunk
# update the version num in src/security.c MOON_DISABLE_SECURITY_PREVIEW_04

svn co -N $BRANCH/moon moon-$PREVIEW
echo -e "\nUpdate the version numbers in moon-$PREVIEW/configure.ac\n"


