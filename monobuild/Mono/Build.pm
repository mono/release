#!/usr/bin/perl

package Mono::Build;

use XML::XPath;

# Local packages
use Mono::Build::Config;
use Env::Bash;

sub getPlatforms
{
	my $dir = $Mono::Build::Config::platformDir;
	my @platforms;

	opendir(DIR, $dir) or die "Can't open dir: $dir\n";

	while($dir = readdir(DIR))
	{
		# For some reason... .svn fails the -d perl test...???
		#if(!-d $dir)
		if($dir ne "." && $dir ne ".." && $dir ne ".svn" && $dir ne "hosts")
		{
			push @platforms, $dir;
		}

	}

	closedir(DIR);

	return sort @platforms;


}

sub getPackages
{
	my $dir = $Mono::Build::Config::packageDir;
	my @packages;

	opendir(DIR, $dir) or die "Can't open dir: $dir\n";


	while($dir = readdir(DIR))
	{
		# For some reason... .svn fails the -d perl test...???
		if(!-d $dir && $dir ne ".svn")
		{
			push @packages, $dir;
		}

	}

	closedir(DIR);

	return sort @packages;
}


sub getPackageInfo
{
	my $pkg = shift;
	my $var = shift;
	
	my $dir = $Mono::Build::Config::packageDir;
	
	return get_env_var( $var, Source => "$dir/$pkg", );
}

sub getLatestRevision
{
	my $platform = shift;
	my $package = shift;

	my $revision;
	
	my $dir = "$Mono::Build::Config::buildsDir/$platform/$package";

	eval {

		opendir(DIR, $dir) or die "Can't open dir: $dir\n";

		while($dir = readdir(DIR))
		{
			# For some reason... .svn fails the -d perl test...???
			#if(!-d $dir)
			if($dir ne "." && $dir ne ".." && $dir ne ".svn")
			{
				push @revisions, $dir;
			}

		}

		closedir(DIR);

		@revisions = sort @revisions;
		$revision = pop @revisions;

	};

	if($@)
	{
		# No builds done with this platform or package
		$revision = "";
	}

	return $revision;
	
}

# Get the state of a package on a platform, not of a particular step
sub getState
{


	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	my $xp;
	my @states;

	my $nodeset;
	my $node;
	my $state;

	my $xmlFile = "$Mono::Build::Config::buildsDir/$platform/$package/$revision/info.xml";

	eval {
		$xp = XML::XPath->new(filename => $xmlFile);
		$nodeset = $xp->find('/build/steps/step/status');

		foreach my $node ($nodeset->get_nodelist)
		{
			$state = XML::XPath::Node::Text::string_value($node); 

			#print "State: $state\n";
			push @states, $state;

		}
	};

	if($@)
	{
		$state = "";

	}

	# State order of preference: inprogress, failure, success, <null>
	
	if(arrayContains("inprogress", @states))
	{
		$state = "inprogress";
	}

	elsif(arrayContains("failure", @states))
	{
		$state = "failure";
	}

	# If I get this far, I assume everything succeeded
	elsif(arrayContains("success", @states))
	{
		$state = "success";
	}

	else
	{
		$state = "";
	}

	return $state;

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


