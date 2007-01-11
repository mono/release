
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

# Private method
def _web_index_sort(web_index_objs):
	"""Args: dictionary objects with an optional 'web_index' key in the 'info' member
	returns: sorted objects, according to web_index.
	Items without web_index are at the end of resulting array, sorted in original
	order, (which in this case is alphabetically)."""

	obj_map = {}
	# Create a map with key as index num, and value as an array of plat objs
	for obj in web_index_objs:

		index = obj.get_info_var('web_index')
		if index == "": index = "999"

		index = int(index)

		if obj_map.has_key(index):
			obj_map[index].append(obj)
		else:
			obj_map[index] = [obj]

	sorted_web_index_objs = []

	indexes = obj_map.keys()
	indexes.sort()

	# get objs out of map into sorted array
	for index in indexes:
		for i in obj_map[index]:
			sorted_web_index_objs.append(i)

	return sorted_web_index_objs

def get_platforms():
	"""Return platform names, sorted alphabetically."""

	platforms = []

	for entry in os.listdir(config.platform_conf_dir):
		if not re.compile('^\.').search(entry) and entry != "hosts":
			platforms.append(entry)

	platforms.sort()

	return platforms

def get_platform_objs():

	platforms = get_platforms()

	plat_objs = []
	for platform in platforms:
		plat_objs.append(packaging.buildenv(platform))

	return _web_index_sort(plat_objs)

def get_packages():

	packages = []

	for entry in os.listdir(config.def_dir):
	
		#  Ignore all dot files
		if not os.path.isdir(config.def_dir + os.sep + entry) and not re.compile('^\.').search(entry):
			packages.append(entry)

	packages.sort()

	return packages


def get_package_objs():
	"""Returns two lists: packages, noarch_packages."""

	packages = get_packages()

        pack_objs = []
        noarch_pack_objs = []

        for package in packages:
		# Don't try to create the dirs and links because this code is run by the web server
                pack_obj = packaging.package("", package, create_dirs_links=False)

		# Handle normal package
		if pack_obj.info['get_destroot'].find('noarch') == -1:
			pack_objs.append(pack_obj)
		# It's noarch
		else:
			noarch_pack_objs.append(pack_obj)

        return _web_index_sort(pack_objs), _web_index_sort(noarch_pack_objs)


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


