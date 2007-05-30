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

#pdb.set_trace()
include_zip = False
fail_on_missing=True
skip_installers = False
try:

	opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "include_zip", "skip_missing", "skip_installers" ])
	for option, value in opts:
		if option == "--include_zip":
			 include_zip = True
		if option == "--skip_missing":
			 fail_on_missing = False
		if option == "--skip_installers":
			 skip_installers = True

	(bundle_name, dest) = remaining_args
except:
	print "Usage: ./sync-bundle.py [ --include_zip | --skip_installers | --skip_missing ] <bundle name> <rsync dest>"
	print " --include_zip includes zip based distros"
	print " --skip_installers will not copy installers"
	print " --skip_missing will allow missing packages for a various platform"
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

# Testing
#config.sd_latest_build_distros = ['redhat-9-i386', 'suse-101-i586']
#config.sd_latest_build_distros = ['suse-101-i586']
config.sd_latest_build_distros = build.get_platforms()

# Gather rpms for this bundle
for plat in config.sd_latest_build_distros:
	plat_obj = packaging.buildconf(plat)
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
		'macosx/new/output/[[version]]/macos-10-universal',
		'sunos/output/[[version]]/sunos-8-sparc',
		]:

	try:
		candidates = glob.glob(dir.replace('[[version]]', archive_version) + os.sep + "*")
		latest = utils.version_sort(candidates).pop()
		installer_dirs.append(latest)
		cwd = os.getcwd()

		splitter = os.sep + archive_version + os.sep
		(prefix, sync_dir) = latest.split(splitter)
		os.chdir(prefix)

		if not skip_installers:
			status, output = utils.launch_process('rsync -avzR -e ssh %s %s/archive' % (archive_version + os.sep + sync_dir, dest))

		os.chdir(cwd)
	except:
		print "Problem syncing: " + dir
		print "Skipping..."



#print files

# Collect directory names of our packages
for file in rpms:
	dirs.append(os.path.dirname(file))

# For the dirs, if any is a symlink, add the real path as well
#  For aliased packages
new_dirs = []
for dir in dirs:
	package_path = os.path.dirname(dir)
	version = os.path.basename(dir)
	if os.path.islink(package_path):
		new_dirs += [ os.path.dirname(package_path) + os.sep + os.readlink(package_path) + os.sep + version ]
dirs += new_dirs

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


print "\n".join(dirs)
print "\n".join(sources)

status, output = utils.launch_process('rsync -avzR -e ssh %s %s %s' % (" ".join(sources), " ".join(dirs), dest))

