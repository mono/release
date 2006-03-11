#!/usr/bin/env python

import sys
import pdb

import Mono.Build

if not len(sys.argv) > 1:
	print "Usage: schedule-build.pl <platform:package>"
	print "\t Can also be a comma separated list of platform:package pairs"
	sys.exit(1)
else:
	arg = sys.argv[1]

invalid = 0

pairs = arg.split(",")

# Verify the platform and package...
for pair in pairs:

	(platform, package) = pair.split(":")

	#print "Checking $platform:$package\n";

	if not (platform and package):
		invalid = 1
		print "Invalid format: " + arg
		break

	if not Mono.Build.validBuild_PlatformPackage(platform, package):
		invalid = 1
		print "Invalid platform:package combo: " + pair
		break

if invalid:
	print "Invalid build request: " + arg
	print "No builds scheduled"
	sys.exit(1)


#my $latest_rev = 44840;
# TODO

for pair in pairs:
	(platform, package) = pair.split(":")

	latest_rev = "r" + Mono.Build.getLatestTreeRevision(package)
	Mono.Build.scheduleBuild(platform, package, latest_rev)
	print "Scheduled " + platform + ":" + package


sys.exit(0)


