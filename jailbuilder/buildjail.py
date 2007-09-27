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
 # Should probably mount proc before running reinstalling all rpms inside chroot (this matters on fedora5)




import sys
import os
import re
import string
import tempfile
import shutil
import pickle
import distutils.dir_util

import pdb

sys.path+=['../pyutils']

import utils
import jail_config


class Package:

	# "Static" Members/Methods
	# Being here they only get compiled once
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
	def load_package_info(self):
		(status, output) = utils.launch_process("""rpm -qp --queryformat "____NAME\n%{NAME}\n____ARCH\n%{ARCH}\n____FILELIST\n[%{FILENAMES}\n]" --queryformat "____REQUIRES\n" --requires --queryformat "____PROVIDES\n" --provides """ + self.full_path, print_output=0)

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

		if jail_config.matchrpm.search(self.full_path):
			return 1
		else:
			return 0

class rpm_query_cache:
	"""Front loader to the Package class, checking a cached version first."""

	def __init__(self, my_dir):

		# Filename to pickle load/unload
		self.cache_dir = 'rpm_cache' + os.sep + os.path.basename(my_dir)

		if not os.path.exists(self.cache_dir):
			distutils.dir_util.mkpath(self.cache_dir)

	def retrieve(self, dir_and_filename):
		"""Load Package object from cache, otherwise create a new one, store it in the cache,
		and return the new object."""

		filename = os.path.basename(dir_and_filename)

		pickle_path = self.cache_dir + os.sep + filename + ".Package.pickle"

		load_success = False
		if os.path.exists(pickle_path):
			pickle_fd = open(pickle_path, 'r')
			try:
				package = pickle.load(pickle_fd)
				pickle_fd.close()
				load_success = True
				print dir_and_filename + " (*Cache hit*)"
			except:
				#Pickling failed... remove .pickle
				pickle_fd.close()
				os.unlink(pickle_path)

		# Load new package
		if not load_success:
			package = Package(dir_and_filename)
			pickle_fd = open(pickle_path, 'w')
			pickle.dump(package, pickle_fd)
			pickle_fd.close()

		return package


class Jail:

	def __init__(self, distro_name):
		self.config = Config(distro_name)

		if not os.path.exists(self.config.jail_dir):
			distutils.dir_util.mkpath(self.config.jail_dir)

		self.cache = rpm_query_cache(self.config.name_ver)

		# These are base names of rpms
		#    for rpm based distros, you must add the rpm dep since we are ignoring rpmlib requirements
		self.orig_required_rpms = self.config.required_rpms
		self.orig_required_rpms.append("rpm")
		self.required_rpms = []

		self.available_rpms = {} # map of rpm_name -> Package object
		self.provide_map = {} # Large map to have quick access to provides

		self.total_requirements = {}  # requirment -> true of false, whether it's been met
		self.requires = {}
		self.provides = {}

		self.load_package_cache(self.config.rpm_source_dir)

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


	def load_package_cache(self, package_dir):
	
		for rpm_filename in os.listdir(package_dir):

			f = package_dir + os.sep + rpm_filename

			# Recursively descend through dir structure
				# This will allow skipping copying rpm files from isos
			if os.path.isdir(f):
				self.load_package_cache(f)
			# Ignore non rpm files, as well as .src.rpm files
			elif jail_config.ignoresource.search(f) or not jail_config.matchrpm.search(f):
				continue
			else:
				my_package = self.cache.retrieve(f)

				# If the package is a valid arch, and
				# It hasn't been loaded yet, or if this arch has a priority over the loaded package
				if self.config.valid_arch.count(my_package.arch) and ( not self.available_rpms.has_key(my_package.name) or self.config.valid_arch.index(self.available_rpms[my_package.name].arch) > self.config.valid_arch.index(my_package.arch)):
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
		missing_packs = []
		for req_rpm in self.orig_required_rpms:
			if not self.add_package(req_rpm):
				missing_packs.append(req_rpm)

		if missing_packs:
			print "ERROR!: missing requested packages: %s" % (" ".join(missing_packs))
			sys.exit(1)

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
					(status, output) = utils.launch_process("""rpm -q --whatprovides '%s' """ % req)
					print output
					sys.exit(1)

			#print self.requires
			#print "***provides***"
			#print self.provides

		# When you make it here, you've got all your deps!
		self.required_rpms.sort()
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
				return False

		return True

	def initialize_jail(self):

		# Blow away the directory
		# Unmount the possible proc dir just in case
		utils.launch_process("umount %s" % self.config.jail_dir + os.sep + "proc")
		print "Removing jail target dir..."
		shutil.rmtree(self.config.jail_dir)
		
		os.makedirs(self.config.jail_dir + os.sep + "var/lib/rpm") # Needed for rpm version 3
		command = """rpm --root %s --initdb""" % self.config.jail_dir
		print command
		(status, output) = utils.launch_process(command)
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
		command = """rpm --nodeps --root %s -i %s""" % (self.config.jail_dir, manifest_filename)
		print command
		(status, output) = utils.launch_process(command)
		print output
		if status:
			print "Error installing rpms inside the jail!!!"
			print "***Usually this is ok for now***"

		# Cleanup...
		os.unlink(manifest_filename)

	
	def install_packages(self):

		# Copy all required rpms to inside the jail
		package_dir = self.config.jail_dir + os.sep + "jailbuilder"
		os.mkdir(package_dir)

		# write a new manifest file 
		#(can't use manifest file on rpm < 4)
		#jail_manifest = open(self.config.jail_dir + os.sep + "jailbuilder" + os.sep + "manifest", 'w')
		rpm_list = ""
		for rpm in self.required_rpms:
			rpm_path = self.available_rpms[rpm].full_path
			shutil.copy(rpm_path, package_dir)
			#jail_manifest.write("jailbuilder" + os.sep + os.path.basename(rpm_path) + "\n")
			rpm_list = rpm_list + " jailbuilder" + os.sep + os.path.basename(rpm_path)
		#jail_manifest.close()

		# Is this location ever going to be different for different distros?
		shutil.rmtree(self.config.jail_dir + os.sep + "var/lib/rpm")
		distutils.dir_util.mkpath(self.config.jail_dir + os.sep + "var/lib/rpm")

		# Add chroot path to environment for redhat based systems
		os.environ['PATH'] = os.environ['PATH'] + ":/usr/sbin"
	
		# Reinitialize the rpm database with the jail's version of rpm	
		command = "chroot %s env %s rpm --initdb" % (self.config.jail_dir, self.config.environment)
		print command
		(status, output) = utils.launch_process(command)
		print "Status: %d" % status
		print "Output: " + output
		if status:
			sys.exit(1)

		# Reinstall the rpms from inside the jail		
		# manifest files don't work on rpm 3 and below...
		#command = "chroot %s env %s rpm --force -U %s" % (self.config.jail_dir, self.environment, "jailbuilder" + os.sep + "manifest")

		# But, this method may be a problem because of the length of the arguments
		command = "chroot %s env %s rpm --force -U %s" % (self.config.jail_dir, self.config.environment, rpm_list)
		print command
		(status, output) = utils.launch_process(command)
		print "Status: %d" % status
		print "Output: " + output


	def post_cleanup(self):
		# Remove rpms inside jail
		shutil.rmtree(self.config.jail_dir + os.sep + "jailbuilder")

		# Remove rpmorig and rpmnew files from the jail
		match_rpmorig = re.compile("rpmorig$")
		match_rpmnew = re.compile("rpmnew$")
		for root, dirs, files in os.walk(self.config.jail_dir):
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
		name_servers = self.config.settings['nameservers'].split()
		
		if name_servers:
			resolv_conf = open(os.path.join(self.config.jail_dir, "etc", "resolv.conf"), 'w')
			for server in name_servers:
				resolv_conf.write("nameserver %s\n" % server)
			# Add search domain for lab... keeps some tests from failing
			resolv_conf.write("search mono.lab.novell.com\n")
			resolv_conf.close()


		# Process user creation


# This will parse the config file and have values available (probably xml?  could be simpler...)
class Config:

	def __init__(self, distro_name):

		execfile('jail_config.py')

		(name, ver, arch) = distro_name.split('-')
		self.name_ver = name + '-' + ver

		self.jail_dir = os.path.abspath("jails" + os.sep + distro_name)

		self.valid_arch = locals()['valid_arch'][arch].split()
		self.required_rpms = locals()['required_rpms'][self.name_ver].split()

		self.settings = locals()['settings']

		# These are optional
		try:
			self.environment = locals()['environment'][self.name_ver]
		except:
			self.environment = ""
		try:
			self.post_install_notes = locals()['post_install_notes'][self.name_ver]
		except:
			self.post_install_notes = ""

		if os.path.exists("rpms" + os.sep + distro_name):
			self.rpm_source_dir = distro_name
		elif os.path.exists("rpms" + os.sep + self.name_ver):
			self.rpm_source_dir = self.name_ver
		else:
			print "Can't find rpms in either rpms/%s or rpms/%s, exiting..." % (distro_name, self.name_ver)
			sys.exit(1)

		self.rpm_source_dir = "rpms" + os.sep + self.rpm_source_dir
		

def commandline():
	if len(sys.argv) < 2:
		print "Usage: ./buildjail.py <distro_name>"
		print "\tExample: ./buildjail.py suse-100-ppc"
		sys.exit(1)
        
	# Collect args
	distro_name = sys.argv[1]

        destdir = "jails" + os.sep + distro_name

	# Make sure we are root
	if not os.getuid() == 0:
		print "Must be super user to run this script..."
		sys.exit(1)

	if os.path.exists(destdir):
		print "Are you sure you want to blow away %s and install a jail? [Y/n]" % destdir
		user_input = sys.stdin.readline().strip().lower()
		#print """'%s'""" % user_input
		if user_input == '': user_input = 'y'
	else:
		user_input = 'y'

	if not user_input[0] == 'n':
		print "Proceeding..."
		jail = Jail(distro_name)
		print "Jail creationg successful!"
	else:
		print "Exiting..."
		sys.exit(0)




# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
        commandline()
 
