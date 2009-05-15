#!/bin/bash

VERSIONS=$(cat VERSIONS)  #read versions from file
NEW_VERSION=$(echo $VERSIONS | awk '{print $NF}') 

scp novell-moonlight*.xpi info*.xhtml mono-web@go-mono.com:go-mono/archive/moonlight-plugins/$NEW_VERSION

scp update-2.0*.rdf mono-web@go-mono.com:go-mono/archive/moonlight-plugins/updates
