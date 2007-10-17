
import os
import os.path
import sys
import distutils.dir_util
import re

import pdb

# User packages...
import config
import packaging
import utils

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

	platforms = {}

	for entry in os.listdir(config.platform_conf_dir):
		#if not re.compile('^\.').search(entry) and entry != "hosts":
		# If it dosen't begin with '.' and isn't an alternate (-%d)
		parts = entry.split('-')
		if len(parts) == 3 and not re.compile('^\.').search(entry):
			platforms[entry] = ""

	platforms = platforms.keys()
	platforms.sort()

	return platforms

def get_platform_objs():

	platforms = get_platforms()

	plat_objs = []
	for platform in platforms:
		plat_objs.append( packaging.buildconf(platform, exclusive=False) )

	return _web_index_sort(plat_objs)

def get_packages():

	packages = []

	for entry in os.listdir(config.def_dir):
	
		#  Ignore all dot files
		if not os.path.isdir(config.def_dir + os.sep + entry) and not re.compile('^\.').search(entry):
			packages.append(entry)

	packages.sort()

	return packages


def get_package_objs(honor_disable_webview=False):
	"""Returns two lists: packages, noarch_packages."""

	packages = get_packages()

        pack_objs = []
        noarch_pack_objs = []

        for package in packages:
		# Don't try to create the dirs and links because this code is run by the web server
                pack_obj = packaging.package("", package, create_dirs_links=False)

		if honor_disable_webview and pack_obj.get_info_var("disable_webview"):
			continue

		# Handle normal package
		# Add workaround for packages that build on multiple platforms, but are noarch (currently mono-basic)
		if pack_obj.info['get_destroot'].find('noarch') == -1 or pack_obj.get_info_var('web_ignore_noarch'):
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

def _head_version_parse(x):
	rel_splitter = x.find('-')

	ver = ""
	rel = ""
	# Handle release
	if rel_splitter > 0:
		#pdb.set_trace()
		ver = x[0:rel_splitter]
		rel = x[rel_splitter+1:]
	else:
		ver = x

	# Handle svn version
	dot_splitter = ver.rfind('.')

	if dot_splitter > 0:
		ver = ver[dot_splitter+1:]

	#print "ver: %s, rel %s" % (ver, rel)
	return int(ver), rel

# Sort by last version
# still 3x slower than rpmvercmp, and WAY slower that python's sort
def _HEAD_sort(x, y):

        x_ver, x_rel = _head_version_parse(x)
        y_ver, y_rel = _head_version_parse(y)

        if x_ver < y_ver:
                return -1
        elif x_ver > y_ver:
                return 1
        elif x_rel < y_rel:
                return -1
        elif x_rel > y_rel:
                return 1
        else:
                return 0



def get_versions(HEAD_or_RELEASE, platform, package):

	versions = []

	try:

		for entry in os.listdir(os.path.join(config.build_info_dir, HEAD_or_RELEASE, platform, package)):
			if entry != ".svn":
				versions.append(entry)

		# TODO: This is going to eventually be innaccurate
		# calling rpmvercmp is too slow here, need a python version
		versions.sort()

		# This was considered as a solution, but is too slow... why not just have the svn revision in configure.in?
		## Do this for RELEASE versions (rpmvercmp doesn't seem to be too slow...)
		#if HEAD_or_RELEASE == "RELEASE":
		#	versions = utils.version_sort(versions)
		#elif HEAD_or_RELEASE == "HEAD":
		#	versions.sort(_HEAD_sort)


	except OSError:
		pass

	return versions


