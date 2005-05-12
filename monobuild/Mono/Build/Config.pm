#!/usr/bin/perl

package Mono::Build::Config;

our $releaseRepo = "/home/wberrier/wa/mono/msvn/release";

our $platformDir = "$releaseRepo/packaging/conf";
our $packageDir = "$releaseRepo/packaging/defs";

# Full path to where the builds are output
our $buildsDir = "$releaseRepo/monobuild/www/builds";
# Url path from view of webserver
our $buildsUrl = "builds";

# Testing
$buildsDir = "$releaseRepo/monobuild/www/builds/testing";
$buildsUrl = "builds/testing";

1;
