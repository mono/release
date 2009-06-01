#!/bin/bash

VERSIONS=$(cat VERSIONS)  #read versions from file
NEW_VERSION=$(echo $VERSIONS | awk '{print $NF}')

ssh mono-web@go-mono.com "mkdir -p go-mono/archive/moonlight-plugins/$NEW_VERSION"

scp novell-moonlight*.xpi sha1sums-$NEW_VERSION mono-web@go-mono.com:go-mono/archive/moonlight-plugins/$NEW_VERSION
scp info*.xhtml mono-web@go-mono.com:go-mono/archive/moonlight-plugins/$NEW_VERSION
scp update-2.0*.rdf mono-web@go-mono.com:go-mono/archive/moonlight-plugins/updates

ssh mono-web@go-mono.com "cd go-mono/archive/moonlight-plugins/$NEW_VERSION;sha1sum -c sha1sums-$NEW_VERSION"
