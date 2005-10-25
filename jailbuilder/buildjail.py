#!/usr/bin/env python

# See README for instructions on how to use buildjail.py
# Basic technique for creating the jail:
#   -Read in package info for all rpms in the rpm_repository_path specified in jail_config.txt
#   -Get list of base packages from jail_config.txt
#   -Resolve all dependencies in order to install the base packages (as well as add the rpm package to the list)
#   -Initialize an rpm database in the jail_directory
#   -Install all required rpms in the jail_directory
#   -Copy rpms into the jail
#   -Remove the jail's rpm database
#   -Enter the jail with chroot:
#     -Reinitialize the rpm database
#     -Reinstall all the rpms
#   -Clean up rpms and rpmorig and rename rpmnew to overwrite current config files
#   -Set up some config options (resolv.conf, user creation, etc)
#   
# 
# Typical jail creation (not including collecting the rpms with gatherrpms.py) can be processed in less than 10 minutes

#TODO: add proc filesystem to /etc/fstab (or at least make sure it's there)




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
		string = string.split(' >= ')[0]
		string = string.split(' = ' )[0]
		string = string.split(' < ' )[0]
		string = string.split(' > ' )[0]
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

		print full_path

		if self.valid_rpm_name():
			self.load_package_info()


	# Get metadata for an rpm
	# (Reference website: http://rikers.org/rpmbook/node30.html)
	# TODO: do a hash of the filename, and check a cache for the data before reloading
	def load_package_info(self):
		(status, output) = commands.getstatusoutput("""rpm -qp --queryformat "____NAME\n%{NAME}\n____ARCH\n%{ARCH}\n____FILELIST\n[%{FILENAMES}\n]" --queryformat "____REQUIRES\n" --requires --queryformat "____PROVIDES\n" --provides """ + self.full_path)

		#print output

		for line in output.split("\n"):
			line = line.strip()

			# Ignore rpm warnings...
			if line.count("warning:"):
				pass
			# If this is a marker, set the marker
			elif Package.marker.search(line):
				marker = line
			else:
				if marker == "____NAME":
					self.name = line.strip()
				elif marker == "____ARCH":
					self.arch = line.strip()
				elif marker == "____REQUIRES":
					# Ignore 'rpmlib(' requirements (don't know how to find out what the rpm binary provides)
					#  If the rpm binary cannot resolv, something will fail later anyway
					if not Package.rpmlib_req.search(line):
						line = Package.remove_version_req(line)
						self.requires.append(line)
				elif marker == "____PROVIDES":
					line = Package.remove_version_req(line)
					self.provides.append(line)
				elif marker == "____FILELIST":
					self.provides.append(line)
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

		if not os.path.exists(self.jail_location):
			print("Target jail location does not exists: %s" % self.jail_location)
			sys.exit(1)

		# These are base names of rpms
		#    for rpm based distros, you must add the rpm dep since we are ignoring rpmlib requirements
		self.orig_required_rpms = config.get_required_rpms()
		self.orig_required_rpms.append("rpm")
		self.required_rpms = []
		self.valid_arch_types = config.get_valid_arch()

		# Get and set environment
		self.environment = self.config.get_environment()

		self.available_rpms = {} # map of rpm_name -> Package object
		self.provide_map = {} # Large map to have quick access to provides

		self.total_requirements = {}  # requirment -> true of false, whether it's been met
		self.requires = {}
		self.provides = {}

		self.load_package_cache()

		#print self.provide_map

		# Start collecting/satisfying dependencies
		self.collect_required_packages()

		self.initialize_jail()

		# Lay down the rpms
		self.bootstrap_install()

		# Install rpms from inside jail
		self.install_packages()

		self.post_cleanup()
		self.post_config()



	# May be able to cache this later to speed things up
	def load_package_cache(self):

		files = os.listdir(self.config.get_rpm_repository_path())
		files.sort()


		for rpm_filename in files:
			my_package = Package(
				os.path.join(self.config.get_rpm_repository_path(), rpm_filename))
				

			# If the package is a valid arch, and
			# It hasn't been loaded yet, or if this arch has a priority over the loaded package
			if self.valid_arch_types.count(my_package.arch) and ( not self.available_rpms.has_key(my_package.name) or self.valid_arch_types.index(self.available_rpms[my_package.name].arch) > self.valid_arch_types.index(my_package.arch)):
				# If the package is going to be overwritten, clean the old one up
				if self.available_rpms.has_key(my_package.name):
					del self.available_rpms[my_package.name]

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

		print "Required packages:"

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


	# Add package to list of required rpms
	def add_package(self, package_name):

		# Only add the package if it's not there already
		if not self.required_rpms.count(package_name):
			if self.available_rpms.has_key(package_name):
				self.required_rpms.append(package_name)
				# Add the requirements
				for req in self.available_rpms[package_name].requires:
					# If it's not already provided, add to list of requires
					if not self.provides.has_key(req):
						self.requires[req] = 1 # don't want duplicates
				for prov in self.available_rpms[package_name].provides:
					self.provides[prov] = 1 # don't want duplicates

			else:
				print "ERROR!: requesting package %s but do not have %s in available rpms!" % (package_name, package_name)
				sys.exit(1)

	def initialize_jail(self):

		# Blow away the directory
		# Unmount the possible proc dir just in case
		commands.getstatusoutput("umount %s" % self.jail_location + os.sep + "proc")
		print "Removing jail target dir..."
		shutil.rmtree(self.jail_location)
		
		os.makedirs(self.jail_location + os.sep + "var/lib/rpm") # Needed for rpm version 3
		command = """rpm --root %s --initdb""" % self.jail_location
		print command
		(status, output) = commands.getstatusoutput(command)
		if status:
			print "Error initializing the rpm database inside the jail"
			sys.exit(1)


	def bootstrap_install(self):

		# Generate a manifest file (list of rpm files)
		manifest_filename = tempfile.mktemp()
		manifest = open(manifest_filename, 'w')

		for rpm in self.required_rpms:
			path = self.available_rpms[rpm].full_path
			manifest.write(path + "\n")
		manifest.close()

		# This will work (using a manifest filename) as long as you're using rpm version 4 and above on the host machine
		command = """rpm --root %s -i %s""" % (self.jail_location, manifest_filename)
		print command
		(status, output) = commands.getstatusoutput(command)
		print output
		if status:
			print "Error installing rpms inside the jail!!!"
			print "***Usually this is ok for now***"

		# Cleanup...
		os.unlink(manifest_filename)

	
	def install_packages(self):

		# Copy all required rpms to inside the jail
		package_dir = self.jail_location + os.sep + "jailbuilder"
		os.mkdir(package_dir)

		# write a new manifest file 
		#(can't use manifest file on rpm < 4)
		#jail_manifest = open(self.jail_location + os.sep + "jailbuilder" + os.sep + "manifest", 'w')
		rpm_list = ""
		for rpm in self.required_rpms:
			rpm_path = self.available_rpms[rpm].full_path
			shutil.copy(rpm_path, package_dir)
			#jail_manifest.write("jailbuilder" + os.sep + os.path.basename(rpm_path) + "\n")
			rpm_list = rpm_list + " jailbuilder" + os.sep + os.path.basename(rpm_path)
		#jail_manifest.close()

		# Is this location ever going to be different for different distros?
		shutil.rmtree(self.jail_location + os.sep + "var/lib/rpm")
		os.mkdir(self.jail_location + os.sep + "var/lib/rpm")

		# Add chroot path to environment for redhat based systems
		os.environ['PATH'] = os.environ['PATH'] + ":/usr/sbin"
	
		# Reinitialize the rpm database with the jail's version of rpm	
		command = "chroot %s env %s rpm --initdb" % (self.jail_location, self.environment)
		print command
		(status, output) = commands.getstatusoutput(command)
		print "Status: %d" % status
		print "Output: " + output

		# Reinstall the rpms from inside the jail		
		# manifest files don't work on rpm 3 and below...
		#command = "chroot %s env %s rpm --force -U %s" % (self.jail_location, self.environment, "jailbuilder" + os.sep + "manifest")

		# But, this method may be a problem because of the length of the arguments
		command = "chroot %s env %s rpm --force -U %s" % (self.jail_location, self.environment, rpm_list)
		print command
		(status, output) = commands.getstatusoutput(command)
		print "Status: %d" % status
		print "Output: " + output


	def post_cleanup(self):
		# Remove rpms inside jail
		shutil.rmtree(self.jail_location + os.sep + "jailbuilder")

		# Remove rpmorig and rpmnew files from the jail
		match_rpmorig = re.compile("rpmorig$")
		match_rpmnew = re.compile("rpmnew$")
		for root, dirs, files in os.walk(self.jail_location):
			for file in files:
				full_path = os.path.join(root, file)
				if match_rpmorig.search(full_path):
					print "Removing: " + full_path
					os.remove(full_path)
				if match_rpmnew.search(full_path):
					# Remove .rpmnew from string
					new_full_path = full_path.replace(".rpmnew", "")
					os.rename(full_path, new_full_path)
					print "Renamed file:" + full_path



	def post_config(self):
		
		# Process resolv.conf
		name_servers = self.config.get_nameservers()
		
		if name_servers:
			resolv_conf = open(os.path.join(self.jail_location, "etc", "resolv.conf"), 'w')
			for server in name_servers:
				resolv_conf.write("nameserver %s\n" % server)
			resolv_conf.close()


		# Process user creation


# This will parse the config file and have values available (probably xml?  could be simpler...)
class Config:

	comment = re.compile("^[\s#]")

	def __init__(self, filename):
		self.setting = {}

		# Load all elements into a dictionary
		for line in open(filename).readlines():
			if not Config.comment.search(line):
				(key, value) = line.split("=", 1)
				self.setting[key] = value.strip()

		
		print self.setting

	def get_setting(self, name):
		if self.setting.has_key(name):
			return self.setting[name]
		else:
			return ""

	def get_rpm_repository_path(self):
		return self.get_setting("rpm_repository_path")

	def get_valid_arch(self):
		return self.get_setting("valid_arch").split()

	def get_required_rpms(self):
		return self.get_setting("required_rpms").split()

	def get_nameservers(self):
		return self.get_setting("nameservers").split()

	def get_environment(self):
		return self.get_setting("environment")


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
 

