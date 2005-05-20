#!/usr/bin/perl

use strict;
use warnings;

use FindBin;
use CGI qw(:standard);
use CGI::Carp;
use lib "$FindBin::RealBin/../..";

use Mono::Build;

my $rootUrl = $Mono::Build::Config::rootUrl;

# Pull this in from the release repo
my @linux_platforms = Mono::Build::getPlatforms();
my @linux_packages = Mono::Build::getPackages();

# Come up with common way to build things not in this framework...
my @other_platforms = (
		'sparc',
		'windows',
		'mac'
		);
my @other_packages = ('mono-1.1');

my $schedule_flag = param('schedule');

print<<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Mono Build Status</TITLE>
<link rel="stylesheet" href="$rootUrl/build.css" type="text/css">
<script language="javascript" src="$rootUrl/build.js"></script>
</HEAD>
<BODY>

<H1>Mono Build Status</H1>

<FORM name=buildform action="schedulebuild.pl" method=post enctype="multipart/form-data">

END

if($schedule_flag) {
	print qq(<p><INPUT type=submit Value="Build Selected Packages"></p>);
}

my $checkbox_html = "";

if($schedule_flag) {
	$checkbox_html = qq(Select All <INPUT type=checkbox name=linux onClick=toggleCheckBoxes(document.buildform.build)>);
}
 
print<<END;
<h3>Linux Platforms</h3>

<p>
<table class="buildstatus">
	<thead><td>$checkbox_html</td>
END

foreach my $platform (sort @linux_platforms)
{
	print "<td>$platform</td>\n";
}

print "</thead><tbody>";


foreach my $package (sort @linux_packages)
{
	print "<tr><td>$package</td>\n";
	my @buildhosts;
	@buildhosts = Mono::Build::getPackageInfo($package, "BUILD_HOSTS");

	my $rev = "";
	my $state = "";

	foreach my $platform (sort @linux_platforms)
	{
	
		# If this is a valid package for this platform...	
		if(Mono::Build::arrayContains($platform, @buildhosts)) {
			# Then start reading the xml...
				# Currently this reads a ton of xml files... might need to aggregate these later...
					# But, that means it's more difficult to remove builds...  issue? 
			$rev = Mono::Build::getLatestRevision($platform, $package); # in r<num> format
			$state = Mono::Build::getState($platform, $package, $rev);

			# if it's a valid package, but hasn't been built yet...
			if($rev eq "" && $state eq "")
			{
				$state = "new";
			}
		}
		else
		{
			$state = "notused"
		}


		print "<td class=$state>";

		# Print a link if there has been a build, and we're not in schedule mode
		if($state ne 'notused' && $state ne 'new' && !$schedule_flag)
		{
			print "<a href=packagestatus.pl?platform=$platform&package=$package&revision=$rev>$rev</a>";
		}

		# Print a checkbox if we're in schedule mode and it's a valid BUILD_HOSTS
		if($schedule_flag && $state ne "notused") {
			print qq(<input type=checkbox name=build value="$platform:$package")
		}
		
		print "</td>\n";

	}
	print "</tr>";
	

}


print "</tbody>
</table>
</p>";

if($schedule_flag) {
	$checkbox_html = qq(Select All <INPUT type=checkbox name=other onClick=toggleCheckBoxes(document.buildform.build_other)>);
} else {
	$checkbox_html = "";
}


# Other Systems
print<<END;
<h3>Other Platforms</h3>

<p>
<table class="buildstatus">
	<thead><td>$checkbox_html</td>
END

foreach my $other_platform (sort @other_platforms)
{
	print "<td>$other_platform</td>\n";
}

print "</thead><tbody>";

foreach my $other_package (sort @other_packages)
{
	print "<tr><td>$other_package</td>\n";

	foreach my $other_platform (sort @other_platforms)
	{
		my $rand;	
		my $state;

		# Make sure you don't get unused
		do 
		{
			$rand = randomRev();	
			$state = randomState($rand);
		} while($state eq 'notused');

		print "<td class=$state>";

		my $rev = "r454";

		#print "<a href=logs/$package-$platform-$rev$rand.log>$rev$rand</a>";

		if($schedule_flag) {
			print qq(<input type=checkbox name=build_other value="$other_platform:$other_package")
		} else {
			print "<a href=$rootUrl/package_status_example.html>$rev$rand</a>";
		}


		print "</td>\n";

	}
	print "</tr>";
	

}


print "</tbody>
</table>
</p>";


# Legend
print<<END;

<h3>Legend</h3>
<p>
<table class=legend>

<tbody>
<tr><th>In Progress</th><td class=inprogress></td></tr>
<tr><th>Success</td><td class=success></td></tr>
<tr><th>Failed</td><td class=failure></td></tr>
<tr><th>Queued</td><td class=queued></td></tr>
<tr><th>New</td><td class=new></td></tr>

</tbody>
</table>
</p>

END

if($schedule_flag) {
	print qq(<p><a href="$ENV{SCRIPT_NAME}">Build Status</a></p>);
} else {
	print qq(<p><a href="$ENV{SCRIPT_NAME}?schedule=true">Schedule Builds</a></p>);
}

# Footer
print<<END;

</FORM>

</BODY>
</HTML>

END

sub randomRev
{
	return int(rand(3) + 1);
}

sub randomState
{
	my $index = shift;
	my @states = (
			'notused',
			'success', 
			'failure', 
			'inprogress', 
		     );
 
	return $states[$index % @states];
}
