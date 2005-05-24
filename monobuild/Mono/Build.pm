#!/usr/bin/perl

package Mono::Build;

use XML::XPath;
use XML::Simple;
use File::Path;
use Data::Dumper;

# Local packages
use Mono::Build::Config;
use Env::Bash;

our $debug = 1;

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

	# If this doesn't get overwritten, a build hasn't been don for this platform/package combo
	my $revision = "";
	
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

	return $revision;
	
}

# Get the state of a package on a platform
sub getState
{

	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	my $xmlFile = "$Mono::Build::Config::buildsDir/$platform/$package/$revision/info.xml";

	my $state = "";

	my $xmlRef;

	eval {

		if( -e $xmlFile) {
			$xmlRef = readInfoXML($xmlFile);
			$state = $xmlRef->{'state'};
		}
	};


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

# Args: platform, package
# Returns: success or fail
sub scheduleBuild
{
	my $platform = shift;
	my $package = shift;
	my $rev = shift;


	if($debug) {
		print STDERR "scheduleBuild: Latest rev: $rev\n";
	}

	# Check to see if this isn't here already...

	# Start outputting the structure
	my $dir = "$Mono::Build::Config::buildsDir/$platform/$package/$rev";
	my $xmlFile = "$dir/info.xml";

	# If it hasn't already been scheduled
	if(! -e $xmlFile) {

		eval {	
			mkpath($dir);
			mkpath("$dir/files");
			mkpath("$dir/logs");
		};

		if($@) {
			print STDERR "Failed to create directory structure ($dir)\n";
			return "create_dir error";
		}
		
		# Get a starter structure...	
		my $xmlRef = readInfoXML("$Mono::Build::Config::releaseRepo/monobuild/info.xml_new");

		# Fill in what we know
		$xmlRef->{revision} = $rev;
		$xmlRef->{platform} = $platform;
		$xmlRef->{package} = $package;

		# Mark the build as queued
		$xmlRef->{state} = "queued";

		if($debug) {

			print STDERR Dumper($xmlRef);
		}

		writeInfoXML($xmlRef, $xmlFile);
		return "";

	} else {

		# Either the data is bogus, or it's already been scheduled...

		# TODO What to do when the build exists?  Probably want to schedule it again if it's finished
		# If it's in the finished state, queue it again
		return "already scheduled";
	}


}

# Have one subroutine to do this because I'll want to considate options
sub readInfoXML
{
	my $file = shift;

	my $ref = "";
	my $fh;

	# Open, lock, read, close
	eval {
		$fh = new IO::File($file);

		flock($fh, 2);

		# SuppressEmpty will use empty strings instead of empty hashes
		$ref = XMLin($fh, SuppressEmpty => undef);

		close($fh);

	};

	return $ref;

}

# Consolidate options
sub writeInfoXML
{

	my $xmlRef = shift;
	my $xmlFile = shift;

	my $fh;

	my $returnCode = 0;

	eval {

		# Open a file
		open($fh, ">$xmlFile");

		# Blocking lock
		flock($fh, 2);

		# Write out the file
		#XMLout($xmlRef, OutputFile => $xmlFile);
		#print STDERR XMLout($xmlRef, NoAttr => 1, RootName => "build");
		XMLout($xmlRef, NoAttr => 1, RootName => "build", OutputFile => $fh);

		# Close and unlock file
		close($fh);

		$returnCode = 1;

	};

	return $returnCode;

}

# Big NOTE: for this to work under apache, apache must have ssh set up
#   Just try it out (get-latest-rev) as the user apache is running as to make sure it works
#    Big NOTE 2: Also, make SURE the apache configs hide the ssh keys!!
sub getLatestTreeRevision
{
	my $revision;

	eval {

		$revision = `$Mono::Build::Config::releaseRepo/packaging/get-latest-rev`;
		chomp $revision;

		# Convention used thoughout the system
		$revision = "r$revision";
	};

	return $revision;
	
}

sub validBuild_PlatformPackage
{
	my $platform = shift;
	my $package = shift;

	my $return_val = 0;

	my @buildhosts = Mono::Build::getPackageInfo($package, "BUILD_HOSTS");

	if(Mono::Build::arrayContains($platform, @buildhosts)) {
		$return_val = 1;
	}

	return $return_val;
	
}


1;


