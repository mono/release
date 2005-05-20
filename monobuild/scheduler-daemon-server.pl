#!/usr/bin/perl


# You can use either the server or the client scheduler...  I'm going to implement the server scheduler first, because it's easier.

use FindBin;
use lib "$FindBin::RealBin";

use Mono::Build;

# read in all of the distro info from /conf/<distro>

# keep track of how many jobs each build server has...

# The web page will lay down very simple scheduling information... and this file will take care of the gory details


# Will be provided: which packages need to be built on what platforms

# What to do: mktarball on a platform (mktarball seems to be possible on whatever platform...)

# Needs to figure out dependencies (the webpage shouldn't really do this, the web will be very simple)

# If there are multiple packaging requests and are in the same dependency chain, make sure no duplicate builds are done

# Really, all you need to check is to see if a certain revision for a platform exists, or is in progress

# In the depencency chain, what to do if a build fails?  If the build was psudo scheduled, remove it, if it was scheduled for real, leave it.




