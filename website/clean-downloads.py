#!/usr/bin/env python

# Script used to removed stale downloads

# Motivation was so that we wouldn't fill up the webserver disk when publishing daily/hourly rpms and repos

# gtk-sharp stuff will get deleted wrong, but that's ok...

import os
import sys
import re
import shutil
import getopt
import glob

sys.path.append("../pyutils")

import utils
import packaging
import build

source_basepath = ""
package_basepath = ""
archive_basepath = ""
platforms = build.get_platforms()

try:
        opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "source_basepath=", "package_basepath=", "archive_basepath=", "platforms=", ])
        for option, value in opts:
                if option == "--source_basepath":
                         source_basepath = value
                if option == "--package_basepath":
                         package_basepath = value
                if option == "--archive_basepath":
                        archive_basepath = value
                if option == "--platforms":
                        platforms = value.split(",")

        (HEAD_or_RELEASE, num_builds) = remaining_args

except:
	print "Usage: ./clean-downloads.py [ --source_basepath=source_basepath ] [ --package_basepath=<package basepath> ] [ --archive_basepath=<archive basepath> ] [ --platforms=<csv distro lst> ] <HEAD_or_RELEASE> <num_builds_to_keep>"
	print "  source_basepath defaults to packaging/sources"
	print "  packaging_basepath defaults to packaging/packages"
	print "  archive_basepath defaults to their build output locations in 'release/'"
	print "  if HEAD_or_RELEASE is HEAD, it will use automatically use the default snapshot_ prefix to the paths"
	print "  distro_list defaults to all distros"
	print "  where num_builds_to_keep >= 1"
	sys.exit(1)

remove_noarch = True

packages = build.get_packages()

num_builds = int(num_builds)

def clean_distro_builds(distro_name):

	# Reference global var instead of defining in our own scope
	global remove_noarch

	print "Removing packages for: " + distro_name
	conf_obj = packaging.buildconf(distro_name, exclusive=False)
	for p in packages:
		# fake out symlink errors by using 'inside_jail'
		pobj = packaging.package(conf_obj, p, HEAD_or_RELEASE=HEAD_or_RELEASE, source_basepath=source_basepath, package_basepath=package_basepath)

		if pobj.destroot == 'noarch' and not remove_noarch:
			continue

		for i in pobj.get_versions(fail_on_missing=False)[:-num_builds]:
			path = os.path.join(package_basepath, pobj.destroot, pobj.name, i)
			print "Removing: " + path
			shutil.rmtree(path)

	# Only remove these once
	remove_noarch = False

def clean_sources():

	for p in packages:
		pobj = packaging.package("", p, HEAD_or_RELEASE=HEAD_or_RELEASE, source_basepath=source_basepath, package_basepath=package_basepath)
		for i in pobj.get_source_files()[:-num_builds]:
			path = os.path.join(source_basepath,  pobj.name, i)
			print "Removing: " + path
			os.unlink(path)

def clean_installers(installer, path):

	cwd = os.getcwd()
	global archive_basepath

	try:
		if archive_basepath:
			os.chdir(archive_basepath)
		else:
			os.chdir(config.release_repo_root)
	except OSError:
		return

	installers = utils.version_sort( glob.glob("*/%s/*" % installer) )
	if installers:
		#print "Found installers (sorted): " + " ".join(installers)
		for i in installers[:-num_builds]:
			print "Removing: " + i
			shutil.rmtree(i)
	else:
		print "No installers found for " + installer

	os.chdir(cwd)
	

clean_sources()

for d in platforms:
	clean_distro_builds(d)

# clean installers
# These are the respective output dirs for the installers.  If archive_basepath isn't specified, installers
#  will be removed from these dirs (release to 'release/')
installer_dirs = {
	'macos-*':		'macosx/output',
	'windows-installer':	'windows-installer/Output',
	'sunos-*':		'sunos/output',

}

for k,v in installer_dirs.iteritems():
	clean_installers(k,v)

