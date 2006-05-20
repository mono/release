#!/usr/bin/env python

import sys
import shutil
import os
import distutils.dir_util
import glob

import pdb

sys.path += [ '../pyutils' ]

import build
import config
import packaging


# Command line options
if len(sys.argv) != 4:
        print "Usage: ./mk-repos.py <bundle name> <package source dir> <output webdir>"
        sys.exit(1)

bundle = sys.argv[1]
package_src_dir = sys.argv[2]
output_dir = sys.argv[3]

bundle_conf = packaging.bundle(bundle_name=bundle)
url_prefix = 'download-' + bundle_conf.info['bundle_urlname']

serverconf = "official"


base_dir = output_dir + os.sep + url_prefix
distutils.dir_util.mkpath(base_dir)
os.chdir(base_dir)

shutil.copy(config.release_repo_root + os.sep + 'website/oc-config/distributions.xml', ".")

fd = open(os.path.join(config.release_repo_root, 'website', 'oc-config', "%s.conf" % serverconf))
template = fd.readlines()
fd.close()

distro_objs = build.get_platform_objs()

server_file = open('server.conf', 'w')

# TODO: maybe we should generate the repo data for all repo types for all distros... ?  That might be just confusing...
# TODO: Flow needs some major reorganizing...  

for line in template:
	line_segs = line.split()
	if not line_segs or line_segs[0] != "!":
		server_file.write(line)
		continue

	chan = line_segs[1]
	server_file.write("AddChannel %s\n" % chan)

	# Yikes, this makes me nervous for now
	# TODO
	if os.path.exists(chan): shutil.rmtree(chan)
	os.mkdir(chan)

	chan_conf = open(chan + os.sep + 'channel.conf', 'w')

	fd = open(os.path.join(config.release_repo_root, 'website', 'oc-config', '%s.chan' % chan))
	chan_template = fd.readlines()
	fd.close()
	
	for line2 in chan_template:

		line_segs2 = line2.split()

		# If line starts with '+'
		#  Create hard links for external_packages for the mono-deps channel
		if line_segs2 and line_segs2[0] == "+":
		
			external_dir = line_segs[1]

			for distro_conf in distro_objs:

				# Only do this for non-zip package type distros
				if distro_conf.info['USE_ZIP_PKG']:
					continue

				distutils.dir_util.mkpath(chan + os.sep + distro_conf.name)

				for rpm_file in glob.glob(os.path.join(external_dir, distro_conf.name, "*.rpm")):
					# Skip source rpms
					if re.compile('\.src\.rpm').search(rpmfile):
						continue

					# Add rpm to the channel for this distro
					os.link(rpm_file, chan + os.sep + distro_conf.name)

			# Ok, ... what's this here for?  this script needs some love...
			continue


		# If line doesn't start with '!' (Normal text)
		if not line_segs2 or line_segs2[0] != "!":
			line2 = line2.replace('[[name]]', serverconf)
			chan_conf.write(line2)
			continue
		
		package = line_segs2[1]


		# Create hard links to real packages to use in repo
		for distro_conf in distro_objs:

			# Skip the distros that use zip packaging system
			if distro_conf.info['USE_ZIP_PKG']:
				continue

			pack_obj = packaging.package(distro_conf, package, bundle_obj=bundle_conf)
			if not pack_obj.valid_use_platform(distro_conf.name):
				continue

			distutils.dir_util.mkpath(chan + os.sep + distro_conf.name)
			for file in pack_obj.get_files_relpath(fail_on_missing=False):
				os.link(package_src_dir + os.sep + file, os.path.join(chan, distro_conf.name, os.path.basename(file)))
	
	# Set up each channel
	for i in glob.glob(chan + os.sep + "*-*-*"):
		distro_obj = packaging.buildenv(os.path.basename(i))

		# Not needed here, since the glob will take a distro list which already made it through this test
		#if distro_obj.info['USE_ZIP_PKG']:
		#	continue

		if distro_obj.info.has_key('distro_aliases'):
			DISTRO_STRING = ":".join([distro_obj.name] + distro_obj.info['distro_aliases'])
		else:
			DISTRO_STRING = distro_obj.name

		
		if distro_obj.info.has_key('USE_OC') and distro_obj.info['USE_OC']:
			chan_conf.write("AddDistro %s %s\n" % (DISTRO_STRING, distro_obj.name) )

		if distro_obj.info.has_key('USE_YUM') and distro_obj.info['USE_YUM']:
			os.system("createrepo " + i)

	chan_conf.close()

server_file.close()

os.system("open-carpet")

