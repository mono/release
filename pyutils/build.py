
import os
import os.path
import tempfile
import commands
import sys
import string
import libxml2
import distutils.dir_util
import commands
import glob
import stat
import fcntl
import re

import pdb

# User packages...
import config

debug = 1

def getPlatforms():
	platforms = []

	for entry in os.listdir(Mono.Build.Config.platformDir):
		if entry != "." and entry != ".." and entry != ".svn" and entry != "hosts":
			platforms.append(entry)

	platforms.sort()
	return platforms


def getPackages():

	packages = []

	for entry in os.listdir(Mono.Build.Config.packageDir):
	
		# For some reason... .svn fails the -d perl test...???
		#  Ignore all dot files
		if not os.path.isdir(entry) and not re.compile('^\.').search(entry):
			packages.append(entry)

	packages.sort()
	return packages


def getLatestRevision(platform, package):

	revisions = []

	# If this doesn't get overwritten, a build hasn't been don for this platform/package combo
	revision = ""

	try:

		for entry in os.listdir(Mono.Build.Config.buildsDir + os.sep + platform + os.sep + package):
			# For some reason... .svn fails the -d perl test...???
			#if(!-d $dir)
			if dir != "." and dir != ".." and dir != ".svn":
				revisions.append(entry)
	

		revisions.sort()
		revision = revisions.pop()

	except OSError:
		pass

	return revision

# TODO:
def getLatestBuiltTarball(package):
	pass


# Args: platform, package
# Returns: success or fail
def scheduleBuild(platform, package, rev):

        #if debug:
        #        sys.stderr.write("scheduleBuild: Latest rev: %s\n" % rev)

        # Check to see if this isn't here already...

        # Start outputting the structure
	#if debug: sys.stderr.write(Mono.Build.Config.buildsDir)
        dir = os.path.join(Mono.Build.Config.buildsDir, platform, package, rev)

        # If it hasn't already been scheduled
        if not os.path.exists(dir):

		if debug: sys.stderr.write("Creating structure (%s)\n" % dir)
		#try:	
		distutils.dir_util.mkpath(dir)
		distutils.dir_util.mkpath(dir + os.sep + "files")
		distutils.dir_util.mkpath(dir + os.sep + "logs")

		os.chmod(dir, all_rwx)
		os.chmod(dir + os.sep + "files", all_rwx)
		os.chmod(dir + os.sep + "logs", all_rwx)

		# Make each one world writable

		#except:
		#	sys.stderr.write("Failed to create directory structure (%s)\n" % dir)
                #        return "create_dir error"

		#  TODO: new xml data store

                return ""

        else:

                # Either the data is bogus, or it's already been scheduled...

                # TODO What to do when the build exists?  Probably want to schedule it again if it's finished
                # If it's in the finished state, queue it again
                return "already scheduled"


