
import xml.xpath
import xml.dom.minidom
import fcntl
import stat
import os
import glob
import re

import config

all_rwx = stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU

# Locking wrappers
def lock_file(fd):
	fcntl.flock(fd, fcntl.LOCK_EX)

def unlock_file(fd):
	fcntl.flock(fd.fileno(), fcntl.LOCK_UN)


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

		# Why are these here?

                # Load file
                self.load_info()

                self.info = {}


        def add_file(self, RELEASE_or_HEAD, package_name, version, filename_path):

                #print "Adding file: %s %s %s %s"  % (package_name, version, snapshot_rev, filename_path)

                self.load_info()
                # Add to structure
                key = ":".join([RELEASE_or_HEAD, package_name, version])
                self.info[key] = filename_path

                # Lock file
                # Write out file
                self.write_info()

        def contains(self, RELEASE_or_HEAD, package_name, version):
                self.load_info()
                return self.info.has_key(":".join([RELEASE_or_HEAD, package_name, version]))


        # Probably won't need this...
        def remove_file(self):
                # Remove from map
                # delete file from disk?
                pass

        def load_info(self):
                # Ex: HEAD:mono-1.1.13:57664=snapshot_sources/mono-1.1.13/mono-1.1.13.4.57664.tar.gz

                self.info = {}

                fd = open(self.data_store_filename, 'r')
                lock_file(fd)

                for line in fd.readlines():
                        matches = re.compile('(.*)=(.*)').search(line)
                        self.info[matches.group(1)] = matches.group(2)

		# Not needed since we're closing the file
                #unlock_file(fd)
                fd.close()


        def write_info(self):

                fd = open(self.data_store_filename, 'w')
                lock_file(fd)

		keys = self.info.keys()
		keys.sort()
                for key in keys:
                        fd.write('%s=%s\n' % (key, self.info[key]))
                fd.close()


# XML data store
class build_info:

	def __init__(self, HEAD_or_RELEASE, distro, package_name, version):

		self.HEAD_or_RELEASE = HEAD_or_RELEASE
		self.distro = distro
		self.package_name = package_name
		self.version = version

		self.xml_file = os.path.join(config.build_info_dir, HEAD_or_RELEASE, distro, package_name, version, "info.xml")

		self.rel_files_dir = os.path.join(HEAD_or_RELEASE, distro, package_name, version)

		self.exists = self.build_exists()

		if self.exists:
			self.read_info_xml()


	#  This will probably mainly get used by ./build
	# TODO: create dir structure path
	def new_build(self):

		# Get a starter template if this doesn't exist

		xml_template = config.release_repo_root + "/monobuild/info.xml_new"
		fd = open(xml_template, 'r')
		xml_string = fd.read()
		fd.close()
		doc = xml.dom.minidom.parseString(xml_string)

		xml.xpath.Evaluate('/build/platform', doc.docmuentElement)[0].appendChild(doc.createTextNode(distro))
		xml.xpath.Evaluate('/build/package', doc.docmuentElement)[0].appendChild(doc.createTextNode(package_name))
		xml.xpath.Evaluate('/build/version', doc.docmuentElement)[0].appendChild(doc.createTextNode(version))

		# write new xml out
		self.doc = doc
		self.write_info_xml()

		# Mark build as exists
		self.exists = self.build_exists()

	def build_exists(self):
		return os.path.exists(self.xml_file)

	# Have one subroutine to do this because I'll want to considate options
	def read_info_xml(self):

		fd = open(self.xml_file, 'r')
		xml_string = fd.read()
		lock_file(fd)
		self.doc = xml.dom.minidom.parseString(xml_string)
		fd.close()


	# Consolidate options
	def write_info_xml(self):

		# Open a file
		file_obj = open(self.xml_file, 'w')

		# Blocking lock
		lock_file(file_obj)

		# Write out the file
		file_obj.write(self.doc.toprettyxml())

		# Close and unlock file
		file_obj.close()

		# Will this be needed?
		# Make it world writable (0x777)
		# Only do this if it's not already all_rwx
		try:
			os.chmod(filename, all_rwx)
		except OSError:
			pass


	# Args: $platform, $package, $revision, %hash of key values to put in info.xml
	#
	# platform, package, revision, state, buildhost, start, finish...
	def update_build(self, platform, package, revision, info):

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
	def update_step(platform, package, revision, step_name, info):

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


	# Get the state of a package on a platform
	def get_state(self):

		state = ""

		if self.exists:
			self.read_info_xml()

			state_node = xml.xpath.Evaluate('/build/state/text()', self.doc.documentElement)[0]
			if state_node:
				state = state_node.nodeValue

		return state


