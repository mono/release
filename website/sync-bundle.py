#!/usr/bin/env python

# There's a possibility that the rpms we're copying are done being copied from the build machine, and could get inconsistent
# results... we'll see how it goes

import os
import sys
import glob
import getopt

sys.path.append("../pyutils")

import packaging
import build
import utils
import config
import datastore

include_zip = False
fail_on_missing=True
skip_installers = False
validated = False
config.sd_latest_build_distros = build.get_platforms()
try:

	opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "include_zip", "skip_missing", "skip_installers", "platforms=", "validated" ])
	for option, value in opts:
		if option == "--include_zip":
			 include_zip = True
		if option == "--skip_missing":
			 fail_on_missing = False
		if option == "--skip_installers":
			 skip_installers = True
		if option == "--platforms":
			config.sd_latest_build_distros = value.split(",")
		if option == "--validated":
			validated = True

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

def find_base_distro(pack_name, distro_name):
	"""Look at all the build hosts to see which gives the same distro_root"""

	plat_obj = packaging.buildconf(distro_name, exclusive=False)
	pack_obj = packaging.package(plat_obj, pack_name, bundle_obj=bundle_obj)

	target_base_path = pack_obj.package_relpath

	base_distro = ""
	for p in pack_obj.get_info_var("BUILD_HOSTS"):
		plat2 = packaging.buildconf(p, exclusive=False)
		pack2 = packaging.package(plat2, pack_name, bundle_obj=bundle_obj)

		if pack2.package_relpath == target_base_path:
			base_distro = p
			#print "Found base distro for %s,%s: %s" % ( pack_name, distro_name, p)
			break

	return base_distro


# TODO: how to make sure we avoid the inprogress builds
#  which can be done by looking at the xml metadata for the build step...
# Gather rpms for this bundle
for plat in config.sd_latest_build_distros:

	# Start with a fresh bundle so one distro doesn't affect another
	bundle_obj2 = packaging.bundle(bundle_name=bundle_name)
	if validated:
		bundle_obj2.force_version_map()

	plat_obj = packaging.buildconf(plat, exclusive=False)

	# Don't gather RPMs from distros published via OBS
	if plat_obj.get_info_var('OBS_REPO'):
		continue

	if not plat_obj.get_info_var('USE_ZIP_PKG') or include_zip:
		print plat_obj.info['distro']
		# Add external dependencies for this distro
		extern = 'external_packages' + os.sep + plat_obj.info['distro']
		if os.path.exists(extern): dirs.append(extern)

		for pack in packages_in_repo:

			#  if we're doing validated builds
			# figure out which version this platform/package should have in the bundle
			if validated:

				#  find the distro that builds for the current pack for the current distro
				base_distro = find_base_distro(pack, plat)
				if not base_distro:
					print "WARNING: unable to find base distro for: %s %s (skipping)" % (plat, pack)
					continue

				versions = build.get_versions(bundle_obj2.HEAD_or_RELEASE(), base_distro, pack)
				versions.reverse()

				target_ver = ""
				for ver in versions:

					build_info = datastore.build_info(bundle_obj2.HEAD_or_RELEASE(), base_distro, pack, ver)

					# check for a build that passed all tests
					if build_info.get_state() == "success":
						target_ver = ver
						print "Found validated build for %s: %s" % (pack, target_ver)
						break

				if target_ver:
					bundle_obj2.add_version(pack, target_ver)

			pack_obj = packaging.package(plat_obj, pack, bundle_obj=bundle_obj2)

			# Ignore versioning from external sources (which we don't build svn versions of)
			if pack_obj.get_info_var("EXTERNAL_SOURCE"):
				pack_obj.bundle_obj.ignore_version_map()

			if pack_obj.valid_use_platform(plat_obj.info['distro']):
				rpms += pack_obj.get_files(fail_on_missing=fail_on_missing)

# Gather sources
for pack in build.get_packages():
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

