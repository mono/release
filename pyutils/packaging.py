
import re
import sys
import tempfile
import os
import os.path
import glob
import distutils.dir_util

import pdb

import config
import utils
import buildenv
import packaging
import shell_parse

class buildconf:

	def __init__(self, conf_file_name, my_logger="", skip_alternates=False):
		"""skip_alternates is for times like jail-do, where I don't care if the jail is locked or not"""

		# Parse out name and counter (alternate)
		parts = conf_file_name.split('-')
		if len(parts) > 3:
			self.name = "-".join(parts[:3])
			counter = int(parts[3])
		else:
			self.name = conf_file_name
			counter = 0

		# Look in the current dir and then in conf dir
		#  (This is so that these classes can be used in /tmp on remote machines)
		if os.path.exists(conf_file_name) and os.path.isfile(conf_file_name):
			conf_dir = ""
			check_alternates = False
		else:
			conf_dir = os.path.join(config.packaging_dir, 'conf')
			check_alternates = True

		lock_dir = os.path.join(config.packaging_dir, 'status')

		# Construct arguments
		buildenv_args = {}
		buildenv_args['my_logger'] = my_logger

		# Find a buildenv that isn't locked
		while True:

			self.conf_lock_filename = self.name
			if counter > 0:
				self.conf_lock_filename += "-%d" % counter

			self.conf_file = os.path.join(conf_dir, self.conf_lock_filename)
			buildenv_args['lock_filename'] = lock_dir + os.sep +  self.conf_lock_filename

			# If no alternates were found
			if not os.path.exists(self.conf_file) and counter > 0:
				break

			self.info = {}
			self.load_computed_info()
			self.load_configured_info()

			for i in "username hostname root_dir target_command_prefix".split():
				if self.info.has_key(i):
					buildenv_args[i] = self.info[i]
				# Remove the stale arg from buildenv_args
				elif buildenv_args.has_key(i):
					buildenv_args.pop(i)

			buildenv_args['env'] = self.env_vars

			# Set up the object
			self.buildenv = buildenv.buildenv(**buildenv_args)

			# Don't check for redundance buildenvs when inside the buildenv
			if not check_alternates:
				break

			if skip_alternates or self.buildenv.offline() or not self.buildenv.is_locked():
				# we're done, use that buildenv
				break

			counter += 1

			print "Checking alternate %d" % counter


	def load_configured_info(self):

		# Default environment
		self.env_vars = {}
		# Make a copy
		for k, v in config.env_vars.iteritems():
			self.env_vars[k] = v

		# Pull out all vars in the distro conf file
		conf_info = shell_parse.parse_file(self.conf_file)
		# Copy info from conf file into structure we've been building
		for k, v in conf_info.iteritems():
			self.info[k] = v

		# Keys that are required
		for key in []:
			if not self.info.has_key(key):
				print "conf file must contain: %s" % key
				sys.exit(1)

		# Allow override from the conf file
		for key in self.env_vars.keys():
			if self.info.has_key(key):
				self.env_vars[key] = self.info[key]

		# allow override or config from self.env
		if self.info.has_key('env'):
			for i in self.info['env'].split(','):
				k, v = i.split('=')
				self.env_vars[k] = v
			# remove it from info now that it's been added to env_vars
			self.info.pop('env')


	def load_computed_info(self):
		"""Load some info based on the buildconf name, that remains the same for redundant jails

		This really needs to be extended...

		example, I have sunos-8-sparc and sunos-10-sparc
		and they are probably both compatible
		And win is on x86, but ARCH assumes x86 means linux
		"""

		self.info['distro'] = self.name

		# Linux distros
		redhat_distros = "fedora redhat rhel".split()
		suse_distros = "suse nld sles sled".split()

		### VERSION, ARCH ###
		try:
		# Parse out distro info
			build_os, self.info['version'], self.info['arch'] = re.compile(r'(.*)-(.*)-(.*)').search(self.name).groups()
		except AttributeError:
			print "%s is not a valid conf name, example: suse-93-i586" % self.name
			sys.exit(1)

		if re.compile(r'i[35]86').search(self.info['arch']): self.info['arch'] = 'x86'

		### OS, OS_TYPE, OS_SUBTYPE ###
		# If our os is either suse or redhat
		if (redhat_distros + suse_distros).count(build_os):
			self.info['os'] = 'linux'
			self.info['os_subtype'] = build_os
			if build_os in redhat_distros:
				self.info['os_type'] = 'redhat'
			elif build_os in suse_distros:
				self.info['os_type'] = 'suse'
		else:
			self.info['os'] = build_os



	def get_info_var(self, key):
		return utils.get_dict_var(key, self.info)



class package:

	def __init__(self, package_env, name, bundle_obj="", bundle_name="", source_basepath="", package_basepath="", inside_jail=False, HEAD_or_RELEASE="", create_dirs_links=True, has_parent_pack=False):
		"""Args: buildconf object, string name of a file in packaging/defs.
		source/package_basepath: full path to where packages are.  Can be overridden (used for web publishing)
		inside_jail: this packaging module is used in release/pyutils and /tmp.  If it's in /tmp, that means we're inside the jail
		   and there are certain things we shouldn't do.

		has_parent_pack: used internally.  Set this flag when creating new package objects within the package constructor.  This
		lets us know to create the dir structure, even if our buildconf isn't valid for this pack (used by def_alias packages).
		"""

		self.package_env = package_env
		self.name = name
		self.source_basepath = source_basepath
		self.package_basepath = package_basepath
		self.inside_jail = inside_jail
		self.create_dirs_links = create_dirs_links

		self.has_parent_pack = has_parent_pack

		# Default to use the file in the current dir, otherwise look in the defs dir
		#  (This change was for do-msvn tar)
		if os.path.exists(name) and os.path.isfile(name):
			self.def_file = name
		else:
			self.def_file = os.path.join(config.packaging_dir, "defs", name)

		if not os.path.exists(self.def_file):
			print "package.__init__(): File not found: %s" % self.def_file
			sys.exit(1)

		self.info = shell_parse.parse_file(self.def_file)

		# Shell config hack to properly populate USE_HOSTS 
		if self.info['USE_HOSTS'] == ['${BUILD_HOSTS[@]}']:
			self.info['USE_HOSTS'] = self.info['BUILD_HOSTS']

		# keys (regs) to grab from the def_alias if they are not in this def file
		valid_alias_key_regs = []
		for reg in ['make_dist', 'HEAD_PATH', 'RELEASE_PATH', 'get_destroot', '_ZIP_', 'get_source']:
			valid_alias_key_regs.append(re.compile(reg))

		# Check alias package so we include any information from it that we don't include in this package (reduces maintenance redundancy)
		self.alias_pack_obj = ""
		if self.get_info_var('def_alias'):
			# TODO: pass all contructor vars to this new object?
			# has_parent_pack must always be true so that def_aliased packages create their dir structure
			self.alias_pack_obj = packaging.package(self.package_env, self.get_info_var('def_alias'), source_basepath=source_basepath, package_basepath=package_basepath, inside_jail=inside_jail, create_dirs_links=create_dirs_links, has_parent_pack=True)
			for k, v in self.alias_pack_obj.info.iteritems():
				# There's some type of data we don't want to copy: def_alias to avoid recursive loops...
				#   Ignore POSTBUILD stuff.... sort of a hack, but ignoring reduces the amount of redundancy
				valid_key = False
				for reg in valid_alias_key_regs:
					if reg.search(k):
						valid_key = True

				# If we don't have the key, grab info from alias def
				if valid_key and not self.info.has_key(k):
					self.info[k] = v

		# Handle bundle
		if bundle_obj and bundle_name:
			print "Cannot pass bundle_obj and bundle_name to package constructor"
			sys.exit(1)
		# Prioritize bundle obj, and then bundle_name, the 'bundle' from def file, and then resort to an empty bundl
		if bundle_obj:
			self.bundle_obj = bundle_obj
		# Remember, if bundle_name is empty, the BUNDLE var will be used
		#  and if BUNDLE env var is empty, as well as bundle_name, bundle_obj.version_map_exists = False
		elif bundle_name:
			self.bundle_obj = bundle(bundle_name=bundle_name)
		# Check to see if the bundle file exists... (if it doesn't, we may be in a jail, or the config file info is wrong)
		elif self.info.has_key('bundle') and os.path.exists(os.path.join(config.packaging_dir, 'bundles', self.info['bundle'])):
			self.bundle_obj = bundle(bundle_name=self.info['bundle'])
		else:
			self.bundle_obj = bundle(bundle_name="")

		# What's passed in overrides the bundle conf
		if HEAD_or_RELEASE:
			self.HEAD_or_RELEASE = HEAD_or_RELEASE
		elif self.bundle_obj.info.has_key('HEAD_or_RELEASE'):
			self.HEAD_or_RELEASE = self.bundle_obj.info['HEAD_or_RELEASE']
		else:
			self.HEAD_or_RELEASE = "RELEASE"

		# if we have a build env
		if self.package_env:
			self.destroot = self.execute_function('get_destroot', 'DEST_ROOT')

		self.setup_paths()
		self.setup_symlinks()

		# Initialize for later... (for caching)
		self.version = ""
		self.latest_version = ""
		self.source_filename = ""

	def execute_function(self, func_name, var_to_echo=""):

		tmp_script = tempfile.mktemp()

		# Kind of a pain to maintain... any var you want to use in get_destroot bash function must be listed here
		my_script = open(tmp_script, 'w')
		my_script.write("DISTRO=%s\n" % self.package_env.info['distro'])
		my_script.write("ARCH=%s\n" % self.package_env.info['arch'])
		my_script.write("USE_ZIP_PKG=%s\n" % self.package_env.get_info_var('USE_ZIP_PKG') )
		my_script.write("HEAD_or_RELEASE=%s\n" % self.HEAD_or_RELEASE )
		my_script.write(self.info[func_name])
		if var_to_echo: my_script.write("echo ${%s}\n" % var_to_echo)
		my_script.close()

		(code, output) = utils.launch_process("sh %s" % tmp_script, print_output=0)

		os.unlink(tmp_script)

		return output

	def setup_paths(self):
		"""Construct basepaths and relative paths for sources and packages."""

		# Set up full basepaths
		if self.package_env and not self.package_basepath:
			# If it's a zipdir package
			#  Make an exception for noarch packages
			if self.package_env.get_info_var('USE_ZIP_PKG') and self.destroot != 'noarch':
				packages_dir = "zip_packages"
			else:
				packages_dir = "packages"

			# Point to snapshot packages if this is HEAD and if we build out of Mono's svn repo
			if self.HEAD_or_RELEASE == "HEAD" and not self.get_info_var('EXTERNAL_SOURCE'): packages_dir = "snapshot_" + packages_dir

			self.package_basepath = os.path.join(config.packaging_dir, packages_dir)
			self.package_base_relpath = packages_dir

		if not self.source_basepath:
			# Point to snapshot sources if this is HEAD and if we build out of Mono's svn repo
			if self.HEAD_or_RELEASE == "HEAD" and not self.get_info_var('EXTERNAL_SOURCE'):
				sources_dir = "snapshot_sources"
			else:
				sources_dir = "sources"
			self.source_basepath = config.packaging_dir + os.sep + sources_dir
			self.source_base_relpath = sources_dir

		# Set up relative and full paths
		if self.package_env:
			self.package_relpath = self.destroot + os.sep + self.name
			self.package_fullpath = self.package_basepath + os.sep + self.package_relpath

		self.source_relpath = self.name
		self.source_fullpath = self.source_basepath + os.sep + self.source_relpath
		

	def setup_symlinks(self):
		"""Setup alias symlinks for sources and packages."""

		if self.package_env and (self.valid_build_platform(self.package_env.name) or self.has_parent_pack):
			dirs = [ self.package_fullpath, self.source_fullpath ]
		else:	dirs = [ self.source_fullpath ]

		# Create the paths if it doesn't exist (and if this isn't an alias pack)
		#  But create the dirs anyway if we're building a HEAD tarball, even if this is a def_alias package
		if not self.inside_jail and self.create_dirs_links and (not self.get_info_var('def_alias') or self.HEAD_or_RELEASE == "HEAD"):
			for path in (dirs):
				if not os.path.exists(path): distutils.dir_util.mkpath(path)

		# Create source and package symlinks if the dirs are there, but not the symlink
		if self.info.has_key('def_alias') and self.HEAD_or_RELEASE == "RELEASE" and self.create_dirs_links:
			#print "Link alias: %s" % self.info['def_alias']
			for dir in (dirs):
				if not os.path.islink(dir) and not self.inside_jail:
					if os.path.exists(dir):
						print "%s is not a symbolic link (it should be)" % dir
						sys.exit(1)
					try:
						os.symlink(self.info['def_alias'], dir)
					except:
						print "Error creating symlink: %s" % dir
						sys.exit(1)


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

	def get_mono_recommend_deps(self):
		if self.info.has_key('MONO_RECOMMEND_DEPS'):
			return self.info['MONO_RECOMMEND_DEPS']
		else:
			return []

	def get_mono_source_deps(self):
		if self.info.has_key('MONO_SOURCE_DEPS'):
			return self.info['MONO_SOURCE_DEPS']
		# If there are no source_deps, use mono_deps instead
		else:
			return self.get_mono_deps()

	def get_packs_to_remove(self):
		if self.info.has_key('PACKS_TO_REMOVE'):
			return self.info['PACKS_TO_REMOVE']
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

	def get_files(self, ext=['rpm', 'zip'], fail_on_missing=True):
		"""call get_files_relpath, then append basepath to the front."""

		files = self.get_files_relpath(ext=ext, fail_on_missing=fail_on_missing)
		new_files = []

		for file in files:
			new_files.append(self.package_basepath + os.sep + file)
	
		return new_files

	def get_files_relpath(self, ext=['rpm', 'zip'], fail_on_missing=True):
		"""Get the list of files for this package, relative to the package_basepath."""

		version = self.get_version(fail_on_missing=fail_on_missing)
		path = self.package_fullpath + os.sep + version

		files = []
	
		if version:
			current_dir = os.getcwd()
			os.chdir(self.package_basepath)

			if ext.__class__ == str:
				ext = [ext]

			for e in ext:
				files += glob.glob(self.package_relpath + os.sep + version + os.sep + '*.%s' % e)

			os.chdir(current_dir)

		# Sort the files (for consistency on the web pages)
		files.sort()

		return files

	def get_version(self, fail_on_missing=True):

		if not self.version:
			if not self.latest_version:
				# Only use the version_selection_reg on RELEASE, since 'version' is replaced with the subversion revision
				#  with HEAD
				version_selection_reg = ""
				if self.HEAD_or_RELEASE == "RELEASE":
					version_selection_reg = self.get_info_var('version_selection_reg')
				self.latest_version = utils.get_latest_ver(self.package_fullpath, fail_on_missing=fail_on_missing, version_reg=version_selection_reg )

			if self.bundle_obj.version_map_exists:
				# Cases
				# 1. version from bundle
				name = self.name

				# Why was this done?  I don't think def_alias should apply to bundle versioning
				#  (Ex: 1.1.13 bundle: gtk-sharp-2.0 picks 1.0.10 stuff even though bundle says 2.4.2)
				#if self.info.has_key('def_alias') and self.HEAD_or_RELEASE == "RELEASE":
				#	name = self.info['def_alias']

				if self.bundle_obj.version_map.has_key(name):
					self.version = self.bundle_obj.version_map[name]
				# 2. If a package is not listed in bundle, print warning and skip
				else:
					print "* Package %s not available in bundle (%s) ... skipping" % (self.name, self.bundle_obj.bundle_name)
					return ""
					#sys.exit(1)

				# 3. If a package is listed as package="", select the latest version
				if self.version == "": self.version = self.latest_version

				# 4. If version has a release of x-0, select x
				elif re.compile('([\d\.]*)-0').search(self.version):
					# Weird comma is because groups() returns tuples
					self.version, = re.compile('([\d\.]*)-0').search(self.version).groups(1)
				# 5. If version doesn't have a release (signified by a dash), get the latest release of that version
				elif not re.compile('[\d\.]*-').search(self.version):
					self.version = utils.get_latest_ver(self.package_fullpath, version=self.version, fail_on_missing=fail_on_missing)

				if not os.path.exists(self.package_fullpath + os.sep + self.version):
					print "Trying to use %s/%s but this path does not exist!" % (self.package_fullpath, self.version)
					sys.exit(1)

			else:
				self.version = self.latest_version

		return self.version

	def get_source_file(self):
		if not self.source_filename:
			if self.bundle_obj.version_map_exists and self.bundle_obj.version_map.has_key(self.name):
				# Strip release version if it exists (so that a bundle conf may have a release attached, 
				#   but that it won't apply to the source)
				ver_wo_rel, = re.compile("(.*)-?").search(self.bundle_obj.version_map[self.name]).groups(1)
				# Can't include self.name as part of reg because of cases like gtk-sharp-2.x

				# Account for empty string versions, ex:  gtk-sharp=""
				if ver_wo_rel == "":
					ver_wo_rel = ".*?"

				reg = re.compile(".*?-%s%s" % (ver_wo_rel, config.sources_ext_re_string) )

			# There's a version map, but this component isn't listed, return nothing
			elif self.bundle_obj.version_map_exists:
				return ""
			# There's no version map, get the latest
			else:
				reg = re.compile(".*")

			candidates = []
			for file in os.listdir(self.source_fullpath):
				# Also match against the version selection reg for this pack def
				if reg.search(file) and re.compile(self.get_info_var('version_selection_reg')).search(file):
					candidates.append(file)

			# TODO: need to use rpm sorting on this?
			self.source_filename = self.name + os.sep + utils.version_sort(candidates).pop()

		return self.source_filename


	# Get all url deps, as well as mono_deps zip/rpms files, and their url deps
	def get_dep_files(self, build_deps=False, recommend_deps=False, source_deps=False):
		files = []

		url_dest = config.packaging_dir + os.sep + 'external_zip_pkg'

		deps = []
		if build_deps:
			deps += self.get_mono_deps()
		if recommend_deps:
			deps += self.get_mono_recommend_deps()
		if source_deps:
			deps += self.get_mono_source_deps()

		for dep in deps:
			# Get files for mono deps
				# Woah, total cheat here, I imported packaging, and am using it!
			package = packaging.package(self.package_env, dep, HEAD_or_RELEASE=self.HEAD_or_RELEASE)

			# If this is a recommended package, don't fail if missing
			if self.get_mono_recommend_deps().count(package.name):
				fail_flag = False
			else:
				fail_flag = True

			files += package.get_files(fail_on_missing=fail_flag)

			# Get url files
			for url in package.get_distro_zip_deps():
				files += [ url_dest + os.sep + os.path.basename(url) ]
				utils.get_url(url, url_dest)

		# Get url files
		for url in self.get_distro_zip_deps():
			files += [ url_dest + os.sep + os.path.basename(url) ]
			utils.get_url(url, url_dest)

		return utils.remove_list_duplicates(files)

	def valid_build_platform(self, platform):
		return_val = 0
		if self.info['BUILD_HOSTS'].count(platform):
			return_val = 1
		return return_val

	def valid_use_platform(self, platform):
		return_val = 0
		if self.info['USE_HOSTS'].count(platform) or self.info['USE_HOSTS'].count("ALL"):
			return_val = 1
		return return_val

	def get_zip_build_commands(self):
		"""Get build code.  Go from more to less specific: distro-ver-arch, distro-ver, distro, then generic."""

		my_os = self.package_env.info['os']
		my_os_version = my_os + "-" + self.package_env.info['version']
		my_distro = self.package_env.info['distro']

		shell_code = ""
		for key in [my_distro, my_os_version, my_os]:
			new_key = key.replace("-", "_") + "_ZIP_BUILD"
			shell_code = self.get_info_var(new_key)
			if shell_code: break

		if not shell_code:
			shell_code = self.get_info_var("ZIP_BUILD")

		if not shell_code:
			print "Warning... could not find shell code..."

		return shell_code

	def get_info_var(self, key):
		return utils.get_dict_var(key, self.info)
		
	def get_aliases(self):
		"""Return all names of alises, recursively.

		This was being done in the packaging scripts to copy stuff over.  Was put here for consolidation.
		"""
		if self.alias_pack_obj:
			return [ self.get_info_var('def_alias') ] + self.alias_pack_obj.get_aliases()
		else:
			return []
		

class bundle:
	def __init__(self, bundle_name=""):
		"""Args: optional: bundle_name, pointing to a file in packaging/bundles
		If this is blank, the BUNDLE environment var will be checked with the bundle name
		If this is blank, no version selection will be used."""

		self.info = {}
		self.version_map = {}
		self.bundle_name = bundle_name
		self.version_map_exists = False

		if self.bundle_name == "" and os.environ.has_key('BUNDLE'):
			self.bundle_name = os.environ['BUNDLE']

		if self.bundle_name != "":
			self.info = shell_parse.parse_file(config.packaging_dir + os.sep + "bundles" + os.sep + self.bundle_name)
			if self.info.has_key('versions'):
				# Can't do this because shell string vars can't have the '-' char...
				#self.version_map = shell_parse.parse_string("\n".join(self.info['versions']))
				self.version_map = {}

				# Note: this ingores single and double quotes around the value
				#  This was copied from shell_parse, but changed so that a var is .* instead of \w*
				for match in re.compile('^\s*(.*?)=["\']?([^\(].*?)["\']?$', re.S | re.M).finditer("\n".join(self.info['versions'])):
					# Weird hack... (easier than fixing the reg...)
					if match.group(2) == '"':
						value = ""
					else:   value = match.group(2)
					self.version_map[match.group(1)] = value

				self.version_map_exists = True

			# Make sure bundle contains minimum data
			for key in "bundle_urlname archive_version".split():
				if not self.info.has_key(key):
					print "Required key (%s) not found in bundle config file" % key
					sys.exit(1)
		else:
			#print "No bundle specified.  Using latest version of packages..."
			pass

