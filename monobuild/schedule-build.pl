#!/usr/bin/perl

use warnings;
use strict;

use FindBin;
use lib "$FindBin::RealBin";

use Mono::Build;

my $arg = shift;

unless($arg)
{
	print "Usage: schedule-build.pl <platform:package>\n";
	print "\t Can also be a comma separated list of platform:package pairs\n";
	exit 1;
}

my $invalid = 0;

my @pairs = split(/,/, $arg);

# Verify the platform and package...
foreach my $pair (@pairs) {

	my ($platform, $package) = split(/:/, $pair);

	#print "Checking $platform:$package\n";

	unless ($platform && $package) {
	
		$invalid = 1;
		print "Invalid format: $arg\n";
		last;
	}

	unless(Mono::Build::validBuild_PlatformPackage($platform, $package)) {
		$invalid = 1;
		print "Invalid platform:package combo: $pair\n";
		last;

	}
}

if($invalid) {

	print "Invalid build request: $arg\n";
	print "No builds scheduled\n";
	exit 1;
}


#my $latest_rev = 44840;
my $latest_rev = Mono::Build::getLatestTreeRevision();

foreach my $pair (@pairs) {

	my ($platform, $package) = split(/:/, $pair);

	Mono::Build::scheduleBuild($platform, $package, $latest_rev);
	print "Scheduled $platform:$package\n";
}


exit 0;


