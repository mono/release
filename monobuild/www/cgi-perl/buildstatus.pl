#!/usr/bin/perl

use strict;
use warnings;

use FindBin;
use lib "$FindBin::RealBin/../..";

use Mono::Build;

# Read these in from a file later...
my @linux_distros = Mono::Build::getDistros();
my @linux_components = Mono::Build::getComponents();

my @other_platforms = (
		'sparc',
		'windows',
		'mac'
		);

my @other_components = ('mono-1.1');

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
<h3>Linux Distros</h3>

<p>
<table class="buildstatus">
	<thead><td></td>
END

foreach my $distro (sort @linux_distros)
{
	print "<td>$distro</td>\n";
}

print "</thead><tbody>";

foreach my $component (sort @linux_components)
{
	print "<tr><td>$component</td>\n";
	my @buildhosts;
	@buildhosts = Mono::Build::getPackageInfo($component, "BUILD_HOSTS");

	foreach my $distro (sort @linux_distros)
	{
		print "<td ";
		my $rand = randomResult();
		my $state = Mono::Build::getState($rand);


		unless (Mono::Build::arrayContains($distro, @buildhosts)) {
			$state = "notused"
		}

		print "class=$state>";

		$rev = "r454";

		if($state ne 'notused')
		{
			#print "<a href=logs/$component-$distro-$rev$rand.log>$rev$rand</a>";
			print "<a href=/package_status_example.html>$rev$rand</a>";
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

foreach my $distro (sort @other_platforms)
{
	print "<td>$distro</td>\n";
}

print "</thead><tbody>";

foreach my $component (sort @other_components)
{
	print "<tr><td>$component</td>\n";

	foreach my $distro (sort @other_platforms)
	{
		print "<td ";
		my $rand;	
		my $state;


		# Make sure you don't get unused
		do 
		{
			$rand = randomResult();	
			$state = Mono::Build::getState($rand);
		} while($state eq 'notused');

		print "class=$state>";

		$rev = "r454";

		#print "<a href=logs/$component-$distro-$rev$rand.log>$rev$rand</a>";
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
<tr><th>In Progress</th><td class=building></td></tr>
<tr><th>Success</td><td class=success></td></tr>
<tr><th>Failed</td><td class=failure></td></tr>

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

sub randomResult
{
	return int(rand(3)) + 1;
}


