#!/usr/bin/perl

use strict;
use warnings;

# Read these in from a file later...
my @distros = ('nld-9-x86_64','rhel-3-i386','sles-9-i586','suse-92-i586','suse-93-x86_64',
		'fedora-3-i386','nld-9-i586','redhat-9-i386','rhel-4-i386','sles-9-x86_64','suse-93-i586', 'sparc','windows','mac');

my @components = ('gtk-sharp-2.0','mod_mono','monodoc',
		'gecko-sharp-2.0','gtksourceview-sharp-2.0','mono-1.1','xsp',
		'gtk-sharp','libgdiplus-1.1','monodevelop');


my $success_color = "#72ff75";
my $failed_color= "red";
my $inprogress_color = "yellow";

my $disabled;
my $rev;


print<<END;
Content-type: text/html

<HEAD>
<TITLE>Mono Build Control</TITLE>
<link rel="stylesheet" href="/build.css" type="text/css">
</HEAD>
<BODY>

<H2>Mono Build Control</H2>


<FORM ACTION=startbuild.html>

<table Border=2 cellpadding=3>
	<th><td></td>
END

foreach my $distro (sort @distros)
{
	print "<td>$distro</td>\n";
}

print "</th>";

foreach my $component (sort @components)
{
	print "<tr><td>$component</td>\n";

	foreach my $distro (sort @distros)
	{
		$disabled = "";
		print "<td ";
		my $rand = randomResult();	

		# Random status...
		if($rand > 8)
		{
			print "bgcolor=$inprogress_color";
			$disabled = "DISABLED"

		}
		elsif($rand > 7)
		{
			print "bgcolor=$failed_color";

		}
		else
		{
			print "bgcolor=$success_color";

		}

		$rev = "r4546";

		print ">";
		print "<INPUT type=checkbox $disabled NAME=$component-$distro >";
		#print "<BR><a href=logs/$component-$distro-$rev.log>$rev</a>";
		
		print "</td>\n";

	}
	print "</tr>";
	

}

sub randomResult
{
	return int(rand(10));
}


print<<END
</table>

<BR>
<INPUT TYPE=Submit VALUE=Build!>

</FORM>

Legend
<table border=1>

<tr><td>In Progress</td><td cellpadding=10 bgcolor=yellow></td></tr>
<tr><td>Success</td><td bgcolor=green></td></tr>
<tr><td>Failed</td><td bgcolor=red></td></tr>

</table>

<br>

</BODY>

END



