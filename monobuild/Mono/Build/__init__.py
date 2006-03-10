__all__ = ["Config"]

import Mono.Build.Config
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

all_rwx = stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU
debug = 1

def get_env_var(var_name, source):

        tmp_script = tempfile.mktemp()

	my_script = open(tmp_script, 'w')
	my_script.write(". %s\n" % source)
	my_script.write("echo ${%s[@]}\n" % var_name)
	my_script.close()

	(status, output) = commands.getstatusoutput("sh %s" % tmp_script)

	os.unlink(tmp_script)

	return output

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

def getPackageInfo(pkg, var):

	return get_env_var( var, Mono.Build.Config.packageDir + os.sep + pkg )

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

# Get the state of a package on a platform
def getState(platform, package, revision):

	xmlFile = os.path.join(Mono.Build.Config.buildsDir, platform, package, revision, "info.xml")

	state = ""
	if os.path.exists(xmlFile):
		try:
			doc = readInfoXML(xmlFile)
			state = doc.xpathEval("build/state")[0].content
			doc.freeDoc()
		except libxml2.parserError:
			state = ""

	return state

# Args: platform, package
# Returns: success or fail
def scheduleBuild(platform, package, rev):

        #if debug:
        #        sys.stderr.write("scheduleBuild: Latest rev: %s\n" % rev)

        # Check to see if this isn't here already...

        # Start outputting the structure
	#if debug: sys.stderr.write(Mono.Build.Config.buildsDir)
        dir = os.path.join(Mono.Build.Config.buildsDir, platform, package, rev)
        xmlFile = dir + os.sep + "info.xml"

        # If it hasn't already been scheduled
        if not os.path.exists(xmlFile):

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

                # Get a starter structure...
                xmlRef = readInfoXML(Mono.Build.Config.releaseRepo + "/monobuild/info.xml_new")

                # xmlFile
		xmlRef.xpathEval("build/package")[0].setContent(package)
		xmlRef.xpathEval("build/platform")[0].setContent(platform)
		xmlRef.xpathEval("build/revision")[0].setContent(rev)
		# TODO
		xmlRef.xpathEval("build/state")[0].setContent("queued")

                writeInfoXML(xmlRef, xmlFile)
		xmlRef.freeDoc()
                return ""

        else:

                # Either the data is bogus, or it's already been scheduled...

                # TODO What to do when the build exists?  Probably want to schedule it again if it's finished
                # If it's in the finished state, queue it again
                return "already scheduled"


# Have one subroutine to do this because I'll want to considate options
def readInfoXML(file):

	xmldoc = ""

	try:
		file_obj = open(file, 'r')
		fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)

		text = file_obj.read()
		xmldoc = libxml2.parseMemory(text, len(text))

		# Not necessary if we're going to close the file (maybe this is only for writing?)
		fcntl.flock(file_obj.fileno(), fcntl.LOCK_UN)

                file_obj.close()

        except:
		sys.stderr.write("Error reading xml file! (%s)" % file)

        return xmldoc

# Consolidate options
def writeInfoXML(xmlRef, filename):

	returnCode = 0

	# Open a file
	file_obj = open(filename, 'w')

	# Blocking lock
	fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX)

	# Write out the file
	xmlRef.dump(file_obj)

	# Close and unlock file
	file_obj.close()

	# Make it world writable (0x777)
	# (Gotta be a prettier way to do this... oh well)
	# Only do this if it's not already all_rwx
	try:
		os.chmod(filename, all_rwx)
	except OSError:
		pass

	returnCode = 1


        return returnCode;

# Big NOTE: for this to work under apache, apache must have ssh set up
#   Just try it out (get-latest-rev) as the user apache is running as to make sure it works
#    Big NOTE 2: Also, make SURE the apache configs hide the ssh keys!!
def getLatestTreeRevision(package):

	dir_loc = Mono.Build.Config.releaseRepo + "/packaging"
	revision = commands.getoutput("cd %s; ./get-latest-rev %s" % (dir_loc, package) )

	return revision

def getLatestBuiltTarball(package):

	tarball_map = Mono.Build.Config.releaseRepo + "/packaging/tarball_map"
	revision = commands.getoutput("cd %s; ./get-latest-rev %s" % (dir_loc, package) )

	return revision


def validBuild_PlatformPackage(platform, package):

        return_val = 0

        buildhosts = Mono.Build.getPackageInfo(package, "BUILD_HOSTS")

	if buildhosts.count(platform):
                return_val = 1

        return return_val


def getQueuedPackages():

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



# Args: $platform, $package, $revision, %hash of key values to put in info.xml
#
# platform, package, revision, state, buildhost, start, finish...
def updateBuild(platform, package, revision, info):

        xmlFile = os.path.join(Mono.Build.Config.buildsDir, platform, package, revision, "info.xml")

        # Get a starter structure...
        xmlRef = readInfoXML(xmlFile)

        # If something was passed in, put it into the
        for key,value in info.iteritems():
                if value:
			xmlRef.xpathEval("build/%s" % key)[0].setContent(value)

        writeInfoXML(xmlRef, xmlFile)

	# These freeDocs are getting annoying... switch to pyxml?  lxml? 4suite?
	xmlRef.freeDoc()


# Args: $platform, $package, $revision, $stepName, %hash of key values to put in the step
#
# platform, package, revision, state, buildhost, start, finish...
#  TODO: Does this step need to be mutexed?
def updateStep(platform, package, revision, stepName, info):

        xmlFile = os.path.join(Mono.Build.Config.buildsDir, platform, package, revision, "info.xml")

        # Get a starter structure...
        xmlRef = readInfoXML(xmlFile)

        # Find out if this is a new step...

        # If not, get a new index

        # If something was passed in, put it into the

	for key, value in info.iteritems():
                if key:
                        xmlRef.xpathEval("build/%s" % key)[0].setContent(value)

        writeInfoXML(xmlRef, xmlFile)

	xmlRef.freeDoc()

