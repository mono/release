#!/usr/bin/perl

package Mono::Build;

use Mono::Build::Config;

sub getDistros
{
	my $dir = $Mono::Build::Config::distroDir;
	my @distros;

	opendir(DIR, $dir) or die "Can't open dir: $dir\n";


	while($dir = readdir(DIR))
	{
		# For some reason... .svn fails the -d perl test...???
		#if(!-d $dir)
		if($dir ne "." && $dir ne ".." && $dir ne ".svn" && $dir ne "hosts")
		{
			push @distros, $dir;
		}

	}

	closedir(DIR);

	return sort @distros;


}

sub getComponents
{
	my $dir = $Mono::Build::Config::componentDir;
	my @components;

	opendir(DIR, $dir) or die "Can't open dir: $dir\n";


	while($dir = readdir(DIR))
	{
		# For some reason... .svn fails the -d perl test...???
		if(!-d $dir && $dir ne ".svn")
		{
			push @components, $dir;
		}

	}

	closedir(DIR);

	return sort @components;


}


sub getState
{
	my $index = shift;
	# This info will eventually come out of a file or something...
	my @states = (
			'notused',
			'success', 
			'success', 
			'success', 
			'success', 
			'failure', 
			'building', 
			'building', 
		     );

	return $states[$index % @states];

}


# Read in distro->component map
sub getValidDistroComponents
{


}

sub arrayContains
{
	my $needle = shift;
	my @haystack = @_;

	foreach my $item (@haystack)
	{
		if ($item eq $needle)
		{
			return 1;

		}


	}
	return 0;


}


1;


