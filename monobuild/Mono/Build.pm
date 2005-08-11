#!/usr/bin/perl

use warnings;
use strict;

package Mono::Build;

use XML::Simple;
use File::Path;
use Data::Dumper;
use IO::File;
use File::Basename;
use Cwd qw( cwd );

# Local packages
use Mono::Build::Config;
use Env::Bash;

our $debug = 1;

# TODO For consistency... ...?
our $queued = "queued";
our $notused = "notused";
our $inprogress = "inprogress";
our $success = "success";
our $failure = "failure";
our $new = "new";

our %descriptiveState = (
	$queued 	=> "Queued",
	$notused 	=> "Not Used",
	$inprogress 	=> "In Progress",
	$success 	=> "Success",
	$failure 	=> "Failure",
	$new 		=> "New",
);

sub getPlatforms
{
	my $platform_dir = $Mono::Build::Config::platformDir;
	my @platforms;

	opendir(DIR, $platform_dir) or die "Can't open dir: $platform_dir\n";

	my $dir;

	while($dir = readdir(DIR))
	{
		# If it's not a directory, not the "hosts" file...
		if(! -d "$platform_dir/$dir" && $dir ne "hosts" && $dir !~ /^\./)
		{
			push @platforms, $dir;
		}

	}

	closedir(DIR);

	return sort @platforms;


}

sub getPackages
{
	my $package_dir = $Mono::Build::Config::packageDir;
	my @packages;

	opendir(DIR, $package_dir) or die "Can't open dir: $package_dir\n";

	my $dir;

	while($dir = readdir(DIR))
	{
		#  Ignore files/directores that start with a period
		if(! -d "$package_dir/$dir" && $dir !~ /^\./)
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

	my @revisions;

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

	if($@) {
		print STDERR "Error reading xml file!: $file\n";
	}

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

sub getQueuedPackages
{

	my @queuedPackages;

	my @distros;
	my @packages;
	my @revisions;
	my $latestRev;
	my $state;

	my @platforms = glob("$Mono::Build::Config::buildsDir/*");

	foreach my $platform (@platforms) {

		$platform = File::Basename::basename($platform);

		@packages = glob("$Mono::Build::Config::buildsDir/$platform/*");

		foreach my $package (@packages) {

			$package = File::Basename::basename($package);

			@revisions = sort( glob("$Mono::Build::Config::buildsDir/$platform/$package/*"));

			$latestRev = pop @revisions;

			$latestRev = File::Basename::basename($latestRev);

			$state = getState($platform, $package, $latestRev);

			if($state eq "queued") {
				push @queuedPackages, "$platform:$package:$latestRev";

			}
		}



	}

	return @queuedPackages;

}

################################################################
## Name: executeCommand                                        
################################################################
sub executeCommand
{
	my $command = shift;

	print "Current working directory: " . cwd() . "\n";
	print "Executing: $command\n";

	my @results;

	open IN, "$command 2>&1 |";
	@results = <IN>;
	close IN;

	#unshift @results,($?/256);
	chomp @results;

	return @results;

}

# Args: $platform, $package, $revision, %hash of key values to put in info.xml
#
# platform, package, revision, state, buildhost, start, finish...
sub updateBuild
{

	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	my %info = @_;

	my $xmlFile = "$Mono::Build::Config::buildsDir/$platform/$package/$revision/info.xml";

	# Get a starter structure...	
	my $xmlRef = readInfoXML($xmlFile);

	# If something was passed in, put it into the 
	foreach my $key (keys %info) {
		if($info{$key}) { 
			$xmlRef->{$key} = $info{$key};
		}
	}

	if($debug) {

		print STDERR Dumper($xmlRef);
	}

	writeInfoXML($xmlRef, $xmlFile);

}

# Args: $platform, $package, $revision, $stepName, %hash of key values to put in the step
#
# platform, package, revision, state, buildhost, start, finish...
#  TODO: Does this step need to be mutexed?
sub updateStep
{

	my $platform = shift;
	my $package = shift;
	my $revision = shift;
	my $stepName = shift;

	my %info = @_;

	my $xmlFile = "$Mono::Build::Config::buildsDir/$platform/$package/$revision/info.xml";

	# Get a starter structure...	
	my $xmlRef = readInfoXML($xmlFile);

	# Find out if this is a new step...
	
	# If not, get a new index

	# If something was passed in, put it into the 
	
	
	foreach my $key (keys %info) {
		if($info{$key}) { 
			$xmlRef->{$key} = $info{$key};
		}
	}

	if($debug) {

		print STDERR Dumper($xmlRef);
	}

	writeInfoXML($xmlRef, $xmlFile);

}




1;


