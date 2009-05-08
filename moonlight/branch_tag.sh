#!/bin/bash

PREVIEW=1.9.1

MONOREV=133384
MOONREV=133784

HOST=svn+ssh://rhowell@mono-cvs.ximian.com/source
MONO=$HOST/trunk/mono
MCS=$HOST/trunk/mcs
MOON=$HOST/trunk/moon
MONOBASIC=$HOST/trunk/mono-basic
BRANCH=$HOST/branches/moon/$PREVIEW
TAG=$HOST/tags/moon/$PREVIEW


# Create the branch
svn mkdir -m " * Creating branch for $PREVIEW" $BRANCH

svn cp -m " * Branching mono r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MONO $BRANCH
svn cp -m " * Branching mcs r$MONOREV for Moonlight $PREVIEW" -r$MONOREV $MCS $BRANCH
svn cp -m " * Branching moon r$MOONREV for Moonlight $PREVIEW" -r$MOONREV $MOON $BRANCH
svn cp -m " * Branching mono-basic for Moonlight $PREVIEW" -rHEAD $MONOBASIC $BRANCH



# Create the tag
svn mkdir -m " * Creating tag for $PREVIEW" $TAG

svn cp -m " * Tagging Moonlight $PREVIEW from branches/moon/$PREVIEW" $BRANCH $TAG


