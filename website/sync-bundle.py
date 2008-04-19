#!/usr/bin/env python

# There's a possibility that the rpms we're copying are done being copied from the build machine, and could get inconsistent
# results... we'll see how it goes

import os
import sys
import glob
import getopt

sys.path.append("../pyutils")

import pdb

import packaging
import build
import utils
import config

include_zip = False
fail_on_missing=True
skip_installers = False
config.sd_latest_build_distros = build.get_platforms()
try:

	opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "include_zip", "skip_missing", "skip_installers", "platforms=" ])
	for option, value in opts:
		if option == "--include_zip":
			 include_zip = True
		if option == "--skip_missing":
			 fail_on_missing = False
		if option == "--skip_installers":
			 skip_installers = True
		if option == "--platforms":
			config.sd_latest_build_distros = value.split(",")

	(bundle_name, dest) = remaining_args
except:
	print "Usage: ./sync-bundle.py [ --include_zip | --skip_installers | --skip_missing | --platforms=<csv distro list> ] <bundle name> <rsync dest>"
	print " --include_zip includes zip based distros"
	print " --skip_installers will not copy installers"
	print " --skip_missing will allow missing packages for a various platform"
	print " --platforms: comma separated list of platforms (distros) to sync"
	print " Ex: ./sync-bundle.py RELEASE wblinux.provo.novell.com:wa/msvn/release/packaging"
	sys.exit(1)


pack_map = {}
files = []
rpms = []
dirs = []
sources = []

execfile('repo-config/config.py')


# (for packages_in_repo)
bundle_obj = packaging.bundle(bundle_name=bundle_name)


# TODO: how to make sure we avoid the inprogress builds
#  which can be done by looking at the xml metadata for the build step...
# Gather rpms for this bundle
for plat in config.sd_latest_build_distros:
	plat_obj = packaging.buildconf(plat, exclusive=False)
	if not plat_obj.get_info_var('USE_ZIP_PKG') or include_zip:
		print plat_obj.info['distro']
		# Add external dependencies for this distro
		extern = 'external_packages' + os.sep + plat_obj.info['distro']
		if os.path.exists(extern): dirs.append(extern)

		for pack in packages_in_repo:
			pack_obj = packaging.package(plat_obj, pack, bundle_obj=bundle_obj)
			if pack_obj.valid_use_platform(plat_obj.info['distro']):
				rpms += pack_obj.get_files(fail_on_missing=fail_on_missing)

# Gather sources
for pack in packages_in_repo:
	pack_obj = packaging.package("", pack, bundle_obj=bundle_obj)
	source_file = pack_obj.get_source_file()
	# Make sure there is a valid source before adding (it will be missing if it's not in the bundle)
	if source_file:
		sources.append(pack_obj.source_basepath + os.sep + source_file)


# Collect installers (grab version defined in the bundle)
archive_version = utils.get_dict_var('archive_version', bundle_obj.info)

os.chdir('..')

installer_dirs = []
for dir in	['linux-installer/output/[[version]]/linux-installer',
		'windows-installer/Output/[[version]]/windows-installer',
		'macosx/output/[[version]]/macos-10-universal',
		'sunos/output/[[version]]/sunos-8-sparc',
		]:

	if skip_installers: continue
	try:
		candidates = glob.glob(dir.replace('[[version]]', archive_version) + os.sep + "*")
		latest = utils.version_sort(candidates).pop()
		installer_dirs.append(latest)
		cwd = os.getcwd()

		splitter = os.sep + archive_version + os.sep
		(prefix, sync_dir) = latest.split(splitter)
		os.chdir(prefix)

		status, output = utils.launch_process('rsync -avzR -e ssh %s %s/archive' % (archive_version + os.sep + sync_dir, dest))

		os.chdir(cwd)
	except:
		print "Problem syncing: " + dir
		print "Skipping..."



#print files

# Collect directory names of our packages
for file in rpms:
	dirs.append(os.path.dirname(file))

# Clean up
dirs = utils.remove_list_duplicates(dirs)
sources = utils.remove_list_duplicates(sources)

os.chdir('packaging')
cwd = os.path.abspath('.')

# Munge the paths a bit for use with rsync
#  (Removing leading path section)
for i in range(0,len(dirs)):
	dirs[i] = dirs[i].replace(cwd + os.sep, '')

for i in range(0,len(sources)):
	sources[i] = sources[i].replace(cwd + os.sep, '')


print "Gathered dirs and sources:"
print "\n".join(dirs)
print "\n".join(sources)
print ""

print "Starting rsync..."
print 'rsync -avzR -e ssh %s %s %s' % (" ".join(sources), " ".join(dirs), dest)
status, output = utils.launch_process('rsync -avzR -e ssh %s %s %s' % (" ".join(sources), " ".join(dirs), dest))

