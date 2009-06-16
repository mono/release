#!/bin/bash

source versions.sh

NEW_VERSION=$PREVIEW

SERVER=mono-web@go-mono.com
DIR="go-mono/archive/moonlight-plugins/$NEW_VERSION"
UPDIR="go-mono/archive/moonlight-plugins/updates"

ssh $SERVER "mkdir -p $DIR"

scp novell-moonlight*.xpi sha1sums-$NEW_VERSION $SERVER:$DIR
scp info*.xhtml $SERVER:$DIR
scp update-2.0*.rdf $SERVER:$UPDIR

ssh $SERVER "cd $DIR;sha1sum -c sha1sums-$NEW_VERSION"


#update the download-page
svn co svn+ssh://rhowell@mono-cvs.ximian.com/source/trunk/release/website/moonlight-preview preview
cd preview
./make-release $NEW_VERSION
svn up -m "* Update preview download page for Moonlight $NEW_VERSION"
cd ..

# update directory on go-mono
ssh $SERVER "cd go-mono/archive/moonlight-preview; svn up;touch Default.aspx"

