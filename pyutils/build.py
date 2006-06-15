
import os
import os.path
import sys
import distutils.dir_util
import re

import pdb

# User packages...
import config
import packaging

debug = 1

def get_platforms():
	"""Return buildenv objects sorted by web_index.  If some platforms don't have a web_index, sort
        the remaining alphabetically."""

	platforms = []

	for entry in os.listdir(config.platform_conf_dir):
		if entry != ".svn" and entry != "hosts":
			platforms.append(entry)

	platforms.sort()

	return platforms

def get_platform_objs():

	platforms = get_platforms()

	plat_objs = []
	plat_map = {}
	for platform in platforms:
		plat_obj = packaging.buildenv(platform)
		if plat_obj.info.has_key('web_index'):
			index = plat_obj.info['web_index']
			plat_map[index] = plat_obj
		else:
			plat_objs.append(plat_obj)

	# Insert ordered platforms to the beginning of the list
	for i in range(0, len(plat_map.keys())):
		plat_objs.insert(i, plat_map[str(i)])

	return plat_objs


def get_packages():

	packages = []

	for entry in os.listdir(config.def_dir):
	
		#  Ignore all dot files
		if not os.path.isdir(config.def_dir + os.sep + entry) and not re.compile('^\.').search(entry):
			packages.append(entry)

	packages.sort()

	return packages


def get_package_objs():

	packages = get_packages()

        pack_objs = []
        pack_map = {}
        for package in packages:
		# Don't try to create the dirs and links because this code is run by the web server
                pack_obj = packaging.package("", package, create_dirs_links=False)
                if pack_obj.info.has_key('web_index'):
                        index = pack_obj.info['web_index']
			print "Index: " + index
                        pack_map[index] = pack_obj
                else:
                        pack_objs.append(pack_obj)

        # Insert ordered packages to the beginning of the list
        for i in range(0, len(pack_map.keys())):
                pack_objs.insert(i, pack_map[str(i)])

        return pack_objs


def get_latest_version(HEAD_or_RELEASE, platform, package):

	version = ""
	versions = get_versions(HEAD_or_RELEASE, platform, package)

	if versions:
		version = versions.pop()

	return version

def get_versions(HEAD_or_RELEASE, platform, package):

	versions = []

	try:

		for entry in os.listdir(os.path.join(config.build_info_dir, HEAD_or_RELEASE, platform, package)):
			if entry != ".svn":
				versions.append(entry)

		# TODO: This is going to eventually be innaccurate
		# calling rpmvercmp is too slow here, need a python version
		versions.sort()

	except OSError:
		pass

	return versions


