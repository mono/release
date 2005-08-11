#!/usr/bin/perl


# You can use either the server or the client scheduler...  I'm going to implement the server scheduler first, because it's easier.

use FindBin;
use lib "$FindBin::RealBin";

# Used for forking
use Errno qw(EAGAIN);


use Mono::Build;

my $pollInterval = 60;

# What to do: mktarball on the mktarball platform...
my $tarballPlatform = $Mono::Build::mktarballPlatform;

# read in all of the distro info from /conf/<distro>
	# Only useful for Load balancing at this point

# keep track of how many jobs each build server has...
	# Only useful for Load balancing at this point

# The web page will lay down very simple scheduling information... and this file will take care of the details



# Main loop ##############

while(1) {

	print "Polling...\n";

	# Will be provided: which packages need to be built on what platforms
	# Get list of packages in the queued state
	my @queuedPackages = Mono::Build::getQueuedPackages();


	foreach my $queuedPackage (@queuedPackages) {

		print "Queued package: $queuedPackage\n";

		# Here would be the place to do the dependency/sanity checks...

		# I'm all good to go for this package... build baby!
		my ($platform, $package, $revision) = split(/:/, $queuedPackage);

		startBuild($platform, $package, $revision);

	}

	sleep($pollInterval);


}



# Needs to figure out dependencies (the webpage shouldn't really do this, the web will be very simple)

# If there are multiple packaging requests and are in the same dependency chain, make sure no duplicate builds are done

# Really, all you need to check is to see if a certain revision for a platform exists, or is in progress

# In the depencency chain, what to do if a build fails?  If the build was psudo scheduled, remove it, if it was scheduled for real, leave it.



# Main loop ##############


sub startBuild
{

	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	my $package_version;

	# fork and build ze package

	FORK: 
	{
		if($pid = fork())
		{
			# Parent
			#   Go on my merry way...

		}
		elsif(defined($pid))
		{
			#child
			Mono::Build::updateBuild($platform, $package, $revision, state => "inprogress");

			$package_version = mktarball($platform, $package, $revision);

			if($!) {

			}

			build($platform, $package, $revision, $package_version);
	
			my $state = "success";

			Mono::Build::updateBuild($platform, $package, $revision, state => $state);

		}
		# Try to recover from a fork error
		elsif($! == EAGAIN)
		{
			#Recoverable Fork error
			print ("Recoverable fork error: Sleeping 5 seconds before retrying...\n");
			sleep 5;
			redo FORK;

		}
	}


}



sub mktarball
{
	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	chdir("$Mono::Build::Config::releaseRepo/packaging");

	my @results;

	# Need to post state
	updateStep($platform, $package, $revision, "Make Tarballs", state => "In Progress"); # Will update or create a new step...

	@results = Mono::Build::executeCommand("./mktarball $Mono::Build::Config::mktarballPlatform $package snap $revision");


	# Find out what version the file is (to pass to the build script)

	my $last_line = pop @results;

	my @temp = split(/-/, $last_line);

	my $package_version = pop @temp;

	# Will this actually work in all cases...?  We shall see... will need to have some serious error checking...
	$package_version =~ /(.*)\.tar\.gz/;

	my $state = "Success";

	# Need to post state and logs 
	updateStep($platform, $package, $revision, "Make Tarballs", state => $state); # Will update or create a new step...

	return $1;
}


sub build
{
	my $platform = shift;
	my $package = shift;
	my $revision = shift;

	updateStep($platform, $package, $revision, "Build", state => "In Progress"); # Will update or create a new step...

	# Validate to make sure this is a valid platform?  Probably don't need to... because this info 
	#    has already been validated from the command line schedule build, and the webpage... 
	#    it's harder to submit invalid data... although surely possible... hmm...

	chdir("$Mono::Build::Config::releaseRepo/packaging");

	executeCommand("./build $platform $package snap $revision");

	my $state = "Successful";

	# Post the results (state, log, etc...)
	updateStep($platform, $package, $revision, "Build", state => $state); # Will update or create a new step...



}



