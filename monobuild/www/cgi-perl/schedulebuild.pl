#!/usr/bin/perl

use strict;
use warnings;

use CGI qw(:standard);
use CGI::Carp;

use Mono::Build;

my $rootUrl = $Mono::Build::Config::rootUrl;

my $debug = 1;

print<<END;
Content-type: text/html

<HEAD>
	<TITLE>Mono Build Control</TITLE>
	<link rel="stylesheet" href="$rootUrl/build.css" type="text/css">
</HEAD>
<BODY>

<H1>Mono Build Control</H1>

<H3>Scheduled the following builds</H3>

<p>

END

my @builds = param('build');
my @builds_other =  param('build_other');

my $latest_rev = Mono::Build::getLatestTreeRevision();

my $platform;
my $package;

print "Tree revision: $latest_rev<br>";

foreach my $build (@builds) {
	print "$build<br>";
	
	($platform, $package) = split(/:/, $build);
	Mono::Build::scheduleBuild($platform, $package, $latest_rev);

}

foreach my $build (@builds_other) {
	print "$build<br>";
}



print<<END;

<a href=/>Back</a>

</p>

</BODY>
</HTML>

END

