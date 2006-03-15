
import os
import os.path
import sys
import distutils.dir_util
import re

import pdb

# User packages...
import config

debug = 1

def get_platforms():
	platforms = []

	for entry in os.listdir(config.platform_conf_dir):
		if entry != ".svn" and entry != "hosts":
			platforms.append(entry)

	platforms.sort()
	return platforms


def get_packages():

	packages = []

	for entry in os.listdir(config.def_dir):
	
		# For some reason... .svn fails the -d perl test...???
		#  Ignore all dot files
		if not os.path.isdir(entry) and not re.compile('^\.').search(entry):
			packages.append(entry)

	packages.sort()
	return packages


def get_latest_version(HEAD_or_RELEASE, platform, package):

	versions = []

	# If this doesn't get overwritten, a build hasn't been don for this platform/package combo
	version = ""

	try:

		for entry in os.listdir(os.path.join(config.build_info_dir, HEAD_or_RELEASE, platform, package)):
			if dir != ".svn":
				versions.append(entry)

		versions.sort()
		version = versions.pop()

	except OSError:
		pass

	return version

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


# Hmm... does this method make sense anymore... ?
def get_queued_packages(self):

	queuedPackages = []

	distros = []
	packages = []
	revisions = []
	latestRev = ""
	state = ""

	platforms = glob.glob(Mono.Build.Config.buildsDir + "/*")

	for platform in platforms:

		platform = os.path.basename(platform)

		packages = glob.glob(Mono.Build.Config.buildsDir + os.sep + platform + os.sep + "*");

		for package in packages:

			package = os.path.basename(package)

			revisions = glob.glob(Mono.Build.Config.buildsDir + os.sep + platform + os.sep + package + os.sep + "*")
			revisions.sort()

			latestRev = revisions.pop()

			latestRev = os.path.basename(latestRev)

			state = getState(platform, package, latestRev)

			if state == "queued":
				queuedPackages.append(":".join([platform, package, latestRev]))

	return queuedPackages


