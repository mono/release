#!/usr/bin/perl

package Mono::Build::Config;

our $releaseRepo = "/home/wberrier/wa/msvn/release";

our $platformDir = "$releaseRepo/packaging/conf";
our $packageDir = "$releaseRepo/packaging/defs";

our $rootUrl = "";

# Full path to where the builds are output
our $buildsDir = "$releaseRepo/monobuild/www/builds";
# Url path from view of webserver
our $buildsUrl = "$rootUrl/builds";

our $mktarballPlatform = "suse-93-i586";

# Testing
$buildsDir = "$releaseRepo/monobuild/www/builds/testing";
$buildsUrl = "builds/testing";

#$releaseRepo = "/net/wberrier/home/wberrier/wa/msvn/release";
#$rootUrl = "/monobuild";

1;
