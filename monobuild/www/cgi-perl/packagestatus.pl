#!/usr/bin/perl

use strict;
use warnings;

# Decided on XPath because it's simpler to install, even though it's probably slower than XML::LibXML
use XML::Simple;
use CGI qw(:standard);
use CGI::Carp;
use Data::Dumper;

# Local modules
use FindBin;
use lib "$FindBin::RealBin/../..";
use Mono::Build;

my $rootUrl = $Mono::Build::Config::rootUrl;

my $html;

my $xml_ref;
my $buildhost;
my $start;
my $finish;

my $platform = param('platform');
my $package = param('package');
my $revision = param('revision');

# Just for testing...
#$platform = "suse-93-i586";
#$package = "gecko-sharp-2.0";
#$revision = "r4543";

# Figure out where the xml file is at
my $xmlFile = "$Mono::Build::Config::buildsDir/$platform/$package/$revision/info.xml";

# Try to open and get data out of the xml document
$xml_ref = Mono::Build::readInfoXML($xmlFile);

if($Mono::Build::debug) {
	print STDERR Dumper($xml_ref);

}

# Couldn't find the xml file...
unless($xml_ref) {
	$html = "<h1>Mono Build Status</h1>";
	$html .= "<p>No information found: $package -- $platform -- $revision</p>";

} else {

	$buildhost = $xml_ref->{'buildhost'};
	$start = $xml_ref->{'start'};
	$finish = $xml_ref->{'finish'};

	$html = qq(

		<h1>$package -- $platform -- $revision</h1>

		<h3>Build status</h3>

		<p>
		<table>
		<tbody>
		<tr>
		<th>Build started:</th>

		<td>$start</td>

		<th>Build completed:</th>
		<td>$finish</td>

		</tr>

		<tr>
		<th>Build host</th>
		<td>$buildhost</td>

		</tr>
		</tbody></table>

		<h3>Build Steps</h3>
		<p>
		<table>
		<tbody>);
	
	# Convert steps to an ordered array
	my @steps;
	foreach my $step_name (keys %{ $xml_ref->{'steps'}{'step'} }) {

		# Create a hash 
		my %hash;
		$hash{$step_name} = $xml_ref->{'steps'}{'step'}{$step_name};

		# Insert into an array, by current step's index, a reference to the above hash
		$steps[$xml_ref->{'steps'}{'step'}{$step_name}{'index'}] = \%hash;

	}

	if($Mono::Build::debug) {
		print STDERR Dumper(@steps);
	}


	# Start through the build steps...	
	foreach my $hash_ref (@steps)
	{
		# There's only going to be one key in the hash...
		my ($name) = keys %$hash_ref;

		my $state = $hash_ref->{$name}{'state'};
		my $log = "/$Mono::Build::Config::buildsUrl/$platform/$package/$revision/logs/$hash_ref->{$name}{'log'}";
	
		$html .= qq(
				<tr>
				<th>$name</th>
				<td><a href="$log">$state</a></td>
			   );

		my $download_file;
		my $download;

		# If there's download info, add it to the html
		if($hash_ref->{$name}{'download'}) {
			$download_file = $hash_ref->{$name}{'download'};
			$download = "/$Mono::Build::Config::buildsUrl/$platform/$package/$revision/files/$download_file";

			$html .= qq(
					<td><a href="$download">$download_file</a></td>
					</tr>
				   );

		}
	}
	
	$html .= "</tbody></table></p>";


}

# Print out the html    

print<<END;
Content-type: text/html

<html><head>

<title>Mono Build Status</title><link rel="stylesheet" href="$rootUrl/build.css" type="text/css"></head>

<body>

$html

</body>
</html>

END


