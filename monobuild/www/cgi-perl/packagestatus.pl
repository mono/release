#!/usr/bin/perl

use strict;
use warnings;

# Decided on XPath because it's simpler to install, even though it's probably slower than XML::LibXML
use XML::XPath;
use CGI qw(:standard);

# Local modules
use FindBin;
use lib "$FindBin::RealBin/../..";
use Mono::Build;

my $html;

my $xp;
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
eval {
	$xp = XML::XPath->new(filename => $xmlFile);
	$buildhost = $xp->findvalue('/build/buildhost');
	$start = $xp->findvalue('/build/start');
	$finish = $xp->findvalue('/build/finish');
};

if($@)
{
	$html = "<h1>Mono Build Status</h1>";
	$html .= "<p>No information found: $package -- $platform -- $revision</p>";

}
else
{

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
	
	# Start through the build steps...	

	my $steps = $xp->find('/build/steps/step');

	foreach my $step ($steps->get_nodelist())
	{

		# Get each data out of the step...
		my $name = $step->find('name'); 
		my $status = $step->find('status'); 
		my $log = "/$Mono::Build::Config::buildsUrl/$platform/$package/$revision/logs/" . $step->find('log'); 
		my $download_file = $step->find('download'); 
		my $download = "/$Mono::Build::Config::buildsUrl/$platform/$package/$revision/files/$download_file"; 
	
		$html .= qq(
				<tr>
				<th>$name</th>
				<td><a href="$log">$status</a></td>

			   );

		if($download)
		{
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

<title>Mono Build Status</title><link rel="stylesheet" href="/build.css" type="text/css"></head>

<body>

$html

</body>
</html>

END




