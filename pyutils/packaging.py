
import re
import sys
import tempfile
import os
import os.path
import glob
import fcntl

import pdb

# needed?
#sys.path += ['../pyutils']
import config
import utils
import sshutils
import packaging
import shell_parse

class buildenv:

	def __init__(self, conf_file_name, print_output=1, logger=""):

                self.name = conf_file_name
                self.conf_file = os.path.join(config.packaging_dir, 'conf', conf_file_name)
                self.print_output = print_output

		# Always turn this off if a logger is used
		if logger: print_output =0

		self.lock_filename = os.path.join(config.packaging_dir, 'status', self.name)

		self.load_info()

		# Construct arguments
		args = {}
		args['target_host'] = self.info['target_host']
		args['print_output'] = self.print_output
		args['logger'] = logger

		for i in "jaildir chroot_path remote_tar_path local_tar_path target_command_prefix build_location".split():
			if self.info.has_key(i):
				args[i] = self.info[i]
	
		# Set up the object	
		self.ssh = sshutils.init(**args)


	def load_info(self):
		"""This really needs to be extended...

		example, I have sunos-8-sparc and sunos-10-sparc
		and they are probably both compatible
		And win is on x86, but ARCH assumes x86 means linux
		"""

		info = {}

		info['distro'] = self.name

		# Linux distros
		redhat_distros = "fedora redhat rhel".split()
		suse_distros = "suse nld sles sled".split()

		### VERSION, ARCH ###
		try:
		# Parse out distro info
			build_os, info['version'], info['arch'] = re.compile(r'(.*)-(.*)-(.*)').search(self.name).groups()
		except AttributeError:
			print "%s is not a valid conf name, example: suse-93-i586" % self.name
			sys.exit(1)

		if re.compile(r'i[35]86').search(info['arch']): info['arch'] = 'x86'

		### OS, OS_TYPE, OS_SUBTYPE ###
		# If our os is either suse or redhat
		if (redhat_distros + suse_distros).count(build_os):
			info['os'] = 'linux'
			info['os_subtype'] = build_os
			if build_os in redhat_distros:
				info['os_type'] = 'redhat'
			elif build_os in suse_distros:
				info['os_type'] = 'suse'
		else:
			info['os'] = build_os


		# Pull out all vars in the distro conf file
		conf_file = os.path.join(config.packaging_dir, "conf", self.name)
		conf_info = shell_parse.parse_file(conf_file)
		# Copy info from conf file into structure we've been building
		for k, v in conf_info.iteritems():
			info[k] = v

		# Some required keys
		for key in ['target_host']:
			if not info.has_key(key):
				print "conf file must contain: %s" % key
				sys.exit(1)

		# Some default keys (Even if they are blank) 
		#  (Easier to do this here then multiple places later)
		for key in ['USE_ZIP_PKG']:
			if not info.has_key(key):
				info[key] = ""

		self.info = info


	# TODO: use fcntl?
	def lock_env(self):
		fd = open(self.lock_filename, 'w')
		fd.write("")
		fd.close()

	def unlock_env(self):
		if os.path.exists(self.lock_filename):
			os.unlink(self.lock_filename)
		else:
			print "Build environment already unlocked"

	def is_locked(self):
		return os.path.exists(self.lock_filename)

	def offline(self):
		old_print_output = self.ssh.print_output
		self.ssh.print_output = 0

		# Run some arbitrary command that will always return true
		(code, output) = self.ssh.execute("ls")

		self.ssh.print_output = old_print_output

		if code: return 1
		else:    return 0

class package:

	def __init__(self, package_env, name, bundle_obj="", bundle_name=""):
		"""Args: buildenv object, string name of a file in packaging/defs.
		"""

		self.package_env = package_env
		self.name = name

		# Default to use the file in the current dir, otherwise look in the defs dir
		#  (This change was for do-msvn tar)
		if os.path.exists(name) and os.path.isfile(name):
			self.def_file = name
		else:
			self.def_file = os.path.join(config.packaging_dir, "defs", name)

		if not os.path.exists(self.def_file):
			print "File not found: %s" % self.def_file
			sys.exit(1)

		self.info = shell_parse.parse_file(self.def_file)

		# Handle bundle
		if bundle_obj and bundle_name:
			print "Cannot pass bundle_obj and bundle_name to package constructor"
			sys.exit(1)
		# Prioritize bundle obj, and then bundle_name
		if bundle_obj: self.bundle_obj = bundle_obj
		# Remember, if bundle_name is empty, the BUNDLE var will be used
		#  and if BUNDLE env var is empty, as well as bundle_name, bundle_obj.exists = False
		else: self.bundle_obj = bundle(bundle_name)

		# if we have a build env
		if self.package_env:
			self.destroot = self.execute_function('get_destroot', 'DEST_ROOT')
			self.path = self.get_package_path()

		# Initialize for later... (for caching)
		self.version = ""
		self.latest_version = ""

	def execute_function(self, func_name, var_to_echo=""):

		tmp_script = tempfile.mktemp()

		# Kind of a pain to maintain... any var you want to use in get_destroot bash function must be listed here
		my_script = open(tmp_script, 'w')
		my_script.write("DISTRO=%s\n" % self.package_env.info['distro'])
		my_script.write("ARCH=%s\n" % self.package_env.info['arch'])
		my_script.write("USE_ZIP_PKG=%s\n" % self.package_env.info['USE_ZIP_PKG'])
		my_script.write(self.info[func_name])
		if var_to_echo: my_script.write("echo ${%s}\n" % var_to_echo)
		my_script.close()

		(code, output) = utils.launch_process("sh %s" % tmp_script, print_output=0)

		os.unlink(tmp_script)

		return output

	def get_package_path(self, HEAD_or_RELEASE="RELEASE"):

		# If it's a zipdir package
		#  Make an exception for noarch packages
		if self.package_env.info['USE_ZIP_PKG'] and self.destroot != 'noarch':
			packages_dir = "zip_packages"
		else:
			packages_dir = "packages"

		if HEAD_or_RELEASE == "HEAD": packages_dir = "snapshot_" + packages_dir

		package_path = os.path.join(config.packaging_dir, packages_dir, self.destroot, self.name)

		# Create symlink if the package dir is there, but not the symlink
		#  This is normally done in packaging/build, but do here just in case an installer script needs it,
		#  but the link isn't there
		if self.info.has_key('source_package_path_name') and HEAD_or_RELEASE == "RELEASE":
			print "Link path: %s" % package_path
			if not os.path.islink(package_path):
				if os.path.exists(package_path):
					print "%s is not a symbolic link (it should be)" % package_path
					sys.exit(1)
				try:
					os.symlink(self.info['source_package_path_name'], package_path)
				except:
					print "Error creating symlink: %s" % package_path
					sys.exit(1)

		return package_path


	# Used for constructing filenames
	def get_revision(self, serial):
		"""Args: serial number (equates to a release for rpms, and -5 in 1.1.13.2-5 for all else)."""

		distro = self.package_env.info['distro']
		if self.destroot == distro:
			(os, ver) = re.compile(r'(.*?)-(.*?)-.*').search(distro).groups()
			revision = "%s.%s%s.novell" % (serial, os, ver)
		else:
			revision = serial + ".novell"
		return revision

	def get_mono_deps(self):
		if self.info.has_key('MONO_DEPS'):
			return self.info['MONO_DEPS']
		else:
			return []

	def get_distro_zip_deps(self):
		name_underscored = self.package_env.name.replace("-", "_")
		name_underscored += "_ZIP_DEPS"
		if self.info.has_key(name_underscored):
			return self.info[name_underscored]
		else:
			return []

	def get_distro_zip_runtime_deps(self):
		name_underscored = self.package_env.name.replace("-", "_")
		name_underscored += "_ZIP_RUNTIME_DEPS"
		if self.info.has_key(name_underscored):
			return self.info[name_underscored]
		else:
			return []

	def get_files(self):
		version = self.get_version()
		path = self.path + os.sep + version

		files = []
	
		if version:
			files += glob.glob(path + os.sep + '*.zip')
			files += glob.glob(path + os.sep + '*.rpm')

		return files

	def get_version(self):

		if not self.version:
			if not self.latest_version:
					self.latest_version = utils.get_latest_ver(self.path)

			if self.bundle_obj.version_map_exists:
				# Cases
				# 1. version from bundle
				if self.bundle_obj.version_map.has_key(self.name):
					self.version = self.bundle_obj.version_map[self.name]
				# 2. If a package is not listed in bundle, skip it
				#  TODO: will this have to be handled elsewhere?
				else:
					return ""

				# 3. If a package is listed as package="", select the latest version
				if self.version == "": self.version = self.latest_version

				# 4. If version has a release of x-0, select x (will have to do with selecting sources as well)
				elif re.compile('([\d\.]*)-0').search(self.version):
					# Weird comma is because groups() returns tuples
					self.version, = re.compile('([\d\.]*)-0').search(self.version).groups(1)
				# 5. If version doesn't have a release (signified by a dash), get the latest release of that version
				elif not re.compile('[\d\.]*-').search(self.version):
					self.version = utils.get_latest_ver(self.path, version=self.version)

				if not os.path.exists(self.path + os.sep + self.version):
					print "Trying to use %s/%s but this path does not exist!" % (self.path, self.version)
					sys.exit(1)

			else:
				self.version = self.latest_version

		return self.version

	# Get all url deps, as well as mono_deps zip/rpms files, and their url deps
	def get_dep_files(self):
		files = []

		url_dest = config.packaging_dir + os.sep + 'external_zip_pkg'

		for dep in self.get_mono_deps():
			# Get files for mono deps
				# Woah, total cheat here, I imported packaging, and am using it!
			package = packaging.package(self.package_env, dep)
			files += package.get_files()

			# Get url files
			for url in package.get_distro_zip_deps():
				files += [ url_dest + os.sep + os.path.basename(url) ]
				utils.get_url(url, url_dest)

		# Get url files
		for url in self.get_distro_zip_deps():
			files += [ url_dest + os.sep + os.path.basename(url) ]
			utils.get_url(url, url_dest)

		return utils.remove_list_duplicates(files)

	def valid_platform(self, platform):
		return_val = 0
		if self.info['BUILD_HOSTS'].count(platform):
			return_val = 1
		return return_val


class bundle:
	def __init__(self, bundle_name=""):
		"""Args: optional: bundle_name, pointing to a file in packaging/bundles
		If this is blank, the BUNDLE environment var will be checked with the bundle name
		If this is blank, no version selection will be used."""

		self.info = {}
		self.version_map = {}
		self.bundle_name = bundle_name
		self.version_map_exists = False

		if not bundle_name and os.environ.has_key('BUNDLE'):
			self.bundle_name = os.environ['BUNDLE']
			self.info = shell_parse.parse_file(config.packaging_dir + os.sep + "bundles" + os.sep + self.bundle_name)
			if self.info.has_key('versions'):
				self.version_map = shell_parse.parse_string("\n".join(self.info['versions']))
				self.version_map_exists = True
		else:
			print "No bundle specified.  Using latest version of packages..."



