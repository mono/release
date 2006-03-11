

import libxml2
import fcntl
import stat
import os
import glob
import re

import config

all_rwx = stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU



# tarball datastore

# info for where tarballs are at and what's available
#  any reason for making this file xml?
class source_file_repo:

        def __init__(self):
                self.data_store_filename = config.packaging_dir + os.sep + 'tarball_map'

                # Create the file if it doesn't exist
                #  TODO: does this need locking?
                if not os.path.exists(self.data_store_filename):
                        fd = open(self.data_store_filename, 'w')
                        fd.write("")
                        fd.close()

                # Load file
                self.load_info()

                self.info = {}


        def add_file(self, package_name, version, snapshot_rev, filename_path):

                #print "Adding file: %s %s %s %s"  % (package_name, version, snapshot_rev, filename_path)

                self.load_info()
                # Add to structure
                key = ":".join([package_name, version, snapshot_rev])
                self.info[key] = filename_path

                # Lock file
                # Write out file
                self.write_info()

        def contains(self, package_name, version, snapshot_rev):
                self.load_info()
                return self.info.has_key(":".join([package_name, version, snapshot_rev]))


        # Probably won't need this...
        def remove_file(self):
                # Remove from map
                # delete file from disk?
                pass

        def load_info(self):
                # Ex: mono-1.1.13:snap:57664=snapshot_sources/mono-1.1.13/mono-1.1.13.4.57664.tar.gz

                self.info = {}

                fd = open(self.data_store_filename, 'r')
                fcntl.flock(fd, fcntl.LOCK_EX)

                for line in fd.readlines():
                        matches = re.compile('(.*)=(.*)').search(line)
                        self.info[matches.group(1)] = matches.group(2)

                fcntl.flock(fd.fileno(), fcntl.LOCK_UN)
                fd.close()


        def write_info(self):

                fd = open(self.data_store_filename, 'w')
                fcntl.flock(fd, fcntl.LOCK_EX)

                for key, value in self.info.iteritems():
                        fd.write('%s=%s\n' % (key, value))
                fd.close()


# XML data store
class build_info:

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

	def __init__(self):

		xmlFile = dir + os.sep + "info.xml"


		# load info, or start a new one
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


