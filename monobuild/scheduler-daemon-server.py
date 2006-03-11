#!/usr/bin/env python

# You can use either the server or the client scheduler...  I'm going to implement the server scheduler first, because it's easier.

import time
import os
import commands

import pdb

import Mono.Build

pollInterval = 60

# What to do: mktarball on the mktarball platform...
tarballPlatform = Mono.Build.Config.mktarballPlatform

# read in all of the distro info from /conf/<distro>
	# Only useful for Load balancing at this point

# keep track of how many jobs each build server has...
	# Only useful for Load balancing at this point

# The web page will lay down very simple scheduling information... and this file will take care of the details


# BIG NOTE: Only linux should be able to build each revision, otherwise, windows, sparc, etc... will get way way over loaded... how to handle this?
# That's only the scheduler, not the tarball creator...

# tarball map has the available tarballs, get the latest version from there




def startBuild(platform, package, revision):

	# fork and build ze package

	#pid = os.fork()
	pid = 0

	if pid:
		pass
		# Parent
		#   Go on my merry way...

	elif pid == 0:

		#child
		Mono.Build.updateBuild(platform, package, revision, dict(state='inprogress') )

		package_version = mktarball(platform, package, revision)

		build(platform, package, revision, package_version)

		my_state = "success"

		Mono.Build.updateBuild(platform, package, revision, dict(state=my_state) )



def mktarball(platform, package, revision):

	pdb.set_trace()

	results = []

	# Need to post state
	# Will update or create a new step...
	#Mono.Build.updateStep(platform, package, revision, "Make Tarballs", dict(state='In Progress') )

	# Format revision
	revision = revision[1:]

	results = commands.getoutput("cd %s; ./mktarball %s %s snap %s" % (Mono.Build.Config.releaseRepo + "/packaging", Mono.Build.Config.mktarballPlatform, package, revision) )

	# Find out what version the file is (to pass to the build script)
	last_line = results.pop()

	temp = last_line.split("-")

	package_version = temp.pop()

	# Will this actually work in all cases...?  We shall see... will need to have some serious error checking...
	name = re.compile("(.*)\.tar\.gz").search(package_version).group(1)

	my_state = "Success"

	# Need to post state and logs 
	# Will update or create a new step...
	Mono.Build.updateStep(platform, package, revision, "Make Tarballs", dict(state=my_state) )

	return name


def build(platform, package, revision):

	# Will update or create a new step...
	Mono.Build.updateStep(platform, package, revision, "Build", dict(state="In Progress") ); 

	# Validate to make sure this is a valid platform?  Probably don't need to... because this info 
	#    has already been validated from the command line schedule build, and the webpage... 
	#    it's harder to submit invalid data... although surely possible... hmm...

	output = commands.getoutput("cd %s; ./build %s %s snap %s" % (Mono.Build.Config.releaseRepo + os.sep + packaging, platform, package, revision) )

	my_state = "Successful"

	# Post the results (state, log, etc...)
	 # Will update or create a new step...
	Mono.Build.updateStep(platform, package, revision, "Build", dict(state=my_state) ) 



# Main loop ##############

while 1:

	print "Polling..."

	# Will be provided: which packages need to be built on what platforms
	# Get list of packages in the queued state
	queuedPackages = Mono.Build.getQueuedPackages()


	for queuedPackage in queuedPackages:

		#pdb.set_trace()

		print "Queued package: " + queuedPackage

		# Here would be the place to do the dependency/sanity checks...

		# I'm all good to go for this package... build baby!
		(platform, package, revision) = queuedPackage.split(":")

		startBuild(platform, package, revision)

	time.sleep(pollInterval)

# This may work better if it just looks for new tarballs and another daemon cranks out tarballs

# Needs to figure out dependencies (the webpage shouldn't really do this, the web will be very simple)

# If there are multiple packaging requests and are in the same dependency chain, make sure no duplicate builds are done

# Really, all you need to check is to see if a certain revision for a platform exists, or is in progress

# In the depencency chain, what to do if a build fails?  If the build was psudo scheduled, remove it, if it was scheduled for real, leave it.



# Main loop ##############
