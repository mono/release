#!/usr/bin/env python

releaseRepo = "/home/wade/wa/msvn/release"

platformDir = releaseRepo + "/packaging/conf"
packageDir = releaseRepo + "/packaging/defs"

rootUrl = ""

# Full path to where the builds are output
buildsDir = releaseRepo + "/monobuild/www/builds"
# Url path from view of webserver
buildsUrl = rootUrl + "/builds"

mktarballPlatform = "suse-93-i586"

# Testing
buildsDir = releaseRepo + "/monobuild/www/builds/testing"
buildsUrl = "builds/testing"

#releaseRepo = "/net/wberrier/home/wberrier/wa/msvn/release";
#rootUrl = "/monobuild";


