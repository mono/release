#!/usr/bin/env python

# Check out the build rpm from ftp://ftp.suse.com/pub/suse/i386/9.3/suse/noarch/build-2005.5.12-0.1.noarch.rpm for ideas how to lay down a jail

# 
# Initialize the rpm database in the jail root
# 
# Get some base packages...
# 
# Resolve all of the dependencies (figure out what packages require, then find what packages provide)  red-carpet libraries may provide this (as well as some yum python bindings)
# 
# install all required users and groups (get this list as we process the rpms) (Doesn't seem to work, may have to install once, capture output of users/groups, and then reinstall with first adding certain users)
# 
# 
# set up resolv.conf
# 
# install rcd/rug
# 
# Add service
# activate the server
# subscribe to the correct channels
# activate the services for red-carpet
# 
# 
# 
# Then, any time a new package is added to the jail, just add the package to the jail definition
# 
# 

# Will be provided a list of rpms for jail

# Need to get the rpms' deps and requirements (might as well do this for all the rpms) (Could be lengthy!)

# Check to make sure the lists' requirements are provided for, and add to the list as needed

# Don't need to worry about other types of package managers (ex: dpkg) because debian have tools to build jails already (not sure how good they are)


import sys
import os
import commands
import re
import string
import tempfile
import shutil
import pdb


class Package:

	# "Static" Members/Methods
	# Being here they only get compiled once
	ignoresource = re.compile("\.(no)?src\.rpm$")
	matchrpm = re.compile("\.rpm$")
	marker = re.compile("^____")
	rpmlib_req = re.compile("^rpmlib(.*)")

	# Remove the versioned portion from a string (provides/requires)
	#  Assuming I can do this here because I'm dealing with a base distro
	def remove_version_req(class_object, string):
		string = string.split(' <= ')[0]
		string = string.split(' = ' )[0]
		string = string.split(' >= ')[0]
		return string
	# Make this a 'static' class method... weird?? 
	#supposed to be updated to be simpler syntax... ? first hackish thing I've seen in Python
	#  But there may be a clearer newer syntax I'm not aware of
	remove_version_req = classmethod(remove_version_req)


	def __init__(self, full_path):
		self.full_path = full_path
		self.rpm_filename = os.path.basename(full_path)

		self.provides = []
		self.requires = []

		# collect the users/groups we need to create in the jail (so everything doesn't get created as root)
		self.groups = []
		self.users = []

		print full_path

		self.valid_rpm_name()

		self.load_package_info()

	# rpm base name: NAME
	# provides: PROVIDES
	# requires: REQUIRES
	# users and groups? (FILEGROUPNAME, FILEUSERNAME)

	def load_package_info(self):
		(status, output) = commands.getstatusoutput("""rpm --nosignature -qp --queryformat "____NAME\n%{NAME}\n____REQUIRES\n" --requires --queryformat "____FILEUSERNAME\n%{FILEUSERNAME}\n____FILEGROUPNAME\n%{FILEGROUPNAME}\n____ARCH\n%{ARCH}\n____PROVIDES\n" --provides --list """ + self.full_path)

		#print output

		for line in output.split("\n"):
			line = line.strip()

			# If this is a marker, set the marker
			if Package.marker.search(line):
				marker = line
			else:
				if marker == "____PROVIDES":
					line = Package.remove_version_req(line)
					self.provides.append(line)
				elif marker == "____NAME":
					self.name = line.strip()
				elif marker == "____REQUIRES":
					# Ignore 'rpmlib(' requirements (don't know how to satisfy them)
					if not Package.rpmlib_req.search(line):
						line = Package.remove_version_req(line)
						self.requires.append(line)
				elif marker == "____FILEUSERNAME":
					self.users.extend(line.split())
				elif marker == "____FILEGROUPNAME":
					self.groups.extend(line.split())
				elif marker == "____ARCH":
					self.arch = line.strip()
				else:
					print "Unknown marker tag: " + marker
					sys.exit(1)



	def valid_rpm_name(self):

		if Package.matchrpm.search(self.full_path):
			return 1
		else:
			return 0


class Jail:

	def __init__(self, config, path):
		self.config = config
		self.jail_location = os.path.abspath(path)

		# These are base names of rpms
		#    for rpm based distros, you must add the rpm dep since we are ignoring rpmlib requirements
		self.orig_required_rpms = config.get_required_rpms()
		self.orig_required_rpms.append("rpm")
		self.required_rpms = []
		self.valid_arch_types = config.get_valid_arch()

		self.available_rpms = {} # map of rpm_name -> Package object
		self.provide_map = {} # Large map to have quick access to provides

		self.total_requirements = {}  # requirment -> true of false, whether it's been met
		self.requires = {}
		self.provides = {}

		self.users = {}
		self.groups = {}

		self.load_package_cache()

		#print self.provide_map

		# Start collecting/satisfying dependencies
		self.collect_required_packages()

		self.initialize_jail()

		# Lay down the rpms
		self.install_packages()

		self.post_config()



	# May be able to cache this later to speed things up
	def load_package_cache(self):

		files = os.listdir(self.config.get_rpm_repository_path())
		files.sort()

		for rpm_filename in files:
			my_package = Package(
				self.config.get_rpm_repository_path() + os.sep + 
				rpm_filename)

			# Make sure it's a valid architecture
			#print self.valid_arch_types
			#print my_package.arch
			# TODO What if there are two packages with each a different valid arch?  Probably won't
			#  matter because the packages are going to get updated with rug anyway... (or are they?)

			if self.valid_arch_types.count(my_package.arch):
				self.available_rpms[my_package.name] = my_package

				# Load up dictionary lookup to quickly resolve deps
				for provide in my_package.provides:
					self.provide_map[provide] = my_package.name
			else:
				print "Skipping %s package for arch %s" % (my_package.name, my_package.arch)
				# Don't need this object anymore
				del my_package



	def collect_required_packages(self):
		# Have two data structures: current requires, and current supplied provides (these structures deal with rpms names, not filenames)
		#  Start adding new packages to get rid of the requires list

		# Add initial deps
		for req_rpm in self.orig_required_rpms:
			self.add_package(req_rpm)

		#print "Current requires:"
		#for i in self.requires:
		#	print i


		# Solve remaining deps
		while(len(self.requires)):
			# remove requires that are provides by our current list of packages
			for req in self.requires.keys():
				if self.provides.has_key(req):
					# remove from requires
					self.requires.pop(req)

			# Add a package for each of the remaining requires
			for req in self.requires.keys():
				if self.provide_map.has_key(req):
					self.add_package(self.provide_map[req])
				else:
					print "ERROR!: need requirement '%s' but do not have a package to satisfy it!" % req
					print "\tmake sure you have the correct arch types in valid_arch in your jail config"
					print "Current Distro Hint:"
					(status, output) = commands.getstatusoutput("""rpm -q --whatprovides '%s' """ % req)
					print output
					sys.exit(1)

			#print self.requires
			#print "***provides***"
			#print self.provides

		# When you make it here, you've got all your deps!
		print self.required_rpms
		print self.groups
		print self.users




	# Add package to list of required rpms
	def add_package(self, package_name):

		#pdb.set_trace()

		# Only add the package if it's not there already
		if not self.required_rpms.count(package_name):
			if self.available_rpms.has_key(package_name):
				print "Adding %s to required_rpms" % package_name
				self.required_rpms.append(package_name)
				# Add the requirements
				for req in self.available_rpms[package_name].requires:
					# If it's not already provided, add to list of requires
					if not self.provides.has_key(req):
						self.requires[req] = 1 # don't want duplicates
				for prov in self.available_rpms[package_name].provides:
					self.provides[prov] = 1 # don't want duplicates

				for user in self.available_rpms[package_name].users:
					#print "User:" + user
					self.users[user] = 1 # Don't want duplicates
				for group in self.available_rpms[package_name].groups:
					#print "Group:" + group
					self.groups[group] = 1 # Don't want duplicates

			else:
				print "ERROR!: requesting package %s but do not have %s in available rpms!" % (package_name, package_name)
				sys.exit(1)
		else:
			print "-required_rpms already has " + package_name


	def initialize_jail(self):

		# Blow away the directory
			# How does this handle symbolic links?
		shutil.rmtree(self.jail_location)
		
		command = """rpm --root %s --initdb""" % self.jail_location
		print command
		(status, output) = commands.getstatusoutput(command)
		if status:
			print "Error initializing the rpm database inside the jail"
			sys.exit(1)
		

	def install_packages(self):

		# Generate a manifest file (list of rpm files)
		# Get a tmp filename

		manifest_filename = tempfile.mktemp()

		manifest = open(manifest_filename, 'w')

		for rpm in self.required_rpms:
			path = self.available_rpms[rpm].full_path
			#print path
			manifest.write(path + "\n")

		manifest.close()

		print manifest_filename

		command = """rpm --root %s -i %s""" % (self.jail_location, manifest_filename)
		print command
		(status, output) = commands.getstatusoutput(command)
		print output
		if status:
			print "Error installing rpms inside the jail"
			sys.exit(1)

		# Parse the output to get users and groups (don't know any other way to do it!!)
		# "warning: group rpm does not exist - using root"

		# Create the users and groups

		# Lay down the packages again



	def post_config(self):
		pass


# This will parse the config file and have values available (probably xml?  could be simpler...)
class Config:

	comment = re.compile("^[\s#]")

	def __init__(self, filename):
		self.setting = {}

		# Load all elements into a dictionary
		for line in open(filename).readlines():
			if not Config.comment.search(line):
				(key, value) = line.split("=")
				self.setting[key] = value.strip()

		
		print self.setting

	def get_setting(self, name):
		return self.setting[name]

	def get_rpm_repository_path(self):
		return self.get_setting("rpm_repository_path")

	def get_valid_arch(self):
		return self.get_setting("valid_arch").split()

	def get_required_rpms(self):
		return self.get_setting("required_rpms").split()




def commandline():
	if len(sys.argv) < 3:
		print "Usage: ./buildjail.py <config_file> <jail_dir>"
		sys.exit(1)
        
	# Collect args
        config_file = sys.argv[1]
        destdir = sys.argv[2]

	print "Are you sure you want to blow away %s and install a jail? [Y/n]" % destdir
	user_input = sys.stdin.readline().strip().lower()
	#print """'%s'""" % user_input
	if user_input == '': user_input = 'y'

	if not user_input[0] == 'n':
		print "Proceeding..."
		jail = Jail(Config(config_file), destdir)
		print "Jail creationg successful!"
	else:
		print "Exiting..."
		sys.exit(0)




# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
        commandline()
 

