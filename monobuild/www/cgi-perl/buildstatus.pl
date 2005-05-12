#!/usr/bin/perl

use strict;
use warnings;

use FindBin;
use lib "$FindBin::RealBin/../..";

use Mono::Build;

# Read these in from a file later...
my @linux_platforms = Mono::Build::getPlatforms();
my @linux_packages = Mono::Build::getPackages();

my @other_platforms = (
		'sparc',
		'windows',
		'mac'
		);

my @other_packages = ('mono-1.1');

my $rev;

print<<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>Mono Build Status</TITLE>
<link rel="stylesheet" href="/build.css" type="text/css">
</HEAD>
<BODY>

<H1>Mono Build Status</H1>

END

print<<END;
<h3>Linux Platforms</h3>

<p>
<table class="buildstatus">
	<thead><td></td>
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

	foreach my $platform (sort @linux_platforms)
	{
		print "<td ";
		my $rev = Mono::Build::getLatestRevision($platform, $package);
		my $state = Mono::Build::getState($platform, $package, $rev);

		unless (Mono::Build::arrayContains($platform, @buildhosts)) {
			$state = "notused"
		}

		# if it hasn't been been yet...
		if($rev eq "" && $state eq "")
		{
			$state = "new";
		}

		print "class=$state>";

		if($state ne 'notused')
		{
			print "<a href=packagestatus.pl?platform=$platform&package=$package&revision=$rev>$rev</a>";
		}
		
		print "</td>\n";

	}
	print "</tr>";
	

}


print "</tbody>
</table>
</p>";


# Other Systems
print<<END;
<h3>Other Platforms</h3>

<p>
<table class="buildstatus">
	<thead><td></td>
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
		print "<td ";
		my $rand;	
		my $state;


		# Make sure you don't get unused
		do 
		{
			$rand = randomRev();	
			$state = randomState($rand);
		} while($state eq 'notused');

		print "class=$state>";

		$rev = "r454";

		#print "<a href=logs/$package-$platform-$rev$rand.log>$rev$rand</a>";
		print "<a href=/package_status_example.html>$rev$rand</a>";

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
<tr><th>Never Built</td><td class=new></td></tr>

</tbody>
</table>
</p>

END

# Footer
print<<END;
<br>

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
