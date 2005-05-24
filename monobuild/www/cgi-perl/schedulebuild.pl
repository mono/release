#!/usr/bin/perl

use strict;
use warnings;

use CGI qw(:standard);
use CGI::Carp;

use Mono::Build;

my $rootUrl = $Mono::Build::Config::rootUrl;

my $html;


$html = qq(

	<HTML>
	<HEAD>
		<TITLE>Mono Build Control</TITLE>
		<link rel="stylesheet" href="$rootUrl/build.css" type="text/css">
	</HEAD>
	<BODY>

	<H1>Mono Build Control</H1>

	<H3>Scheduled the following builds</H3>

	<p>
	  );

my @builds = param('build');
my @builds_other =  param('build_other');
my $latest_rev;

if($latest_rev = Mono::Build::getLatestTreeRevision())
{
	$html .= "Error scheduling build<br>";

	print STDERR join("\n", keys %ENV);
}

my $platform;
my $package;

$html .= "Tree revision: $latest_rev<br>";

foreach my $build (@builds) {
	$html .= "$build<br>";
	
	($platform, $package) = split(/:/, $build);
	Mono::Build::scheduleBuild($platform, $package, $latest_rev);

}

foreach my $build (@builds_other) {
	$html .= "$build<br>";
}



$html .= qq(

	<a href=/>Back</a>

	</p>

	</BODY>
	</HTML>

	   );

print "Content-type: text/html\n\n";
print $html;

