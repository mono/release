#!/usr/bin/env python

import sys
import shutil
import os
import distutils.dir_util
import glob
import time
import re

import xml.xpath
import xml.dom.minidom
import gzip

import pdb

sys.path += [ '../pyutils' ]

import build
import config
import packaging
import utils

# Command line options
if len(sys.argv) != 4:
        print "Usage: ./mk-repos.py <bundle name> <package source dir> <output webdir>"
        sys.exit(1)

bundle = sys.argv[1]
package_src_dir = os.path.abspath(sys.argv[2])
output_dir = sys.argv[3]

bundle_conf = packaging.bundle(bundle_name=bundle)
url_prefix = 'download-' + bundle_conf.info['bundle_urlname']

base_dir = output_dir + os.sep + url_prefix
distutils.dir_util.mkpath(base_dir)
os.chdir(base_dir)

shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/oc/distributions.xml', ".")
shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/oc/server.conf', ".")
shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/oc/channel.conf', ".")

# OC config file substitution
utils.substitute_parameters_in_file('server.conf', { 
	'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'] 
} )

utils.substitute_parameters_in_file('channel.conf', { 
	'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'], 
	'@BUNDLE_DESC@': bundle_conf.info['bundle_desc']
} )

distro_objs = build.get_platform_objs()

# TODO: maybe we should generate the repo data for all repo types for all distros... ?  That might be just confusing...

# Create hard links to real packages to use in repo
for distro_obj in distro_objs:

	# TODO: Come up with repo system for zip system
	if distro_obj.info['USE_ZIP_PKG']:
		pass

	# Only non-zip distros and valid distros for this package
	else: 

		if not os.path.exists(distro_obj.name):
			distutils.dir_util.mkpath(distro_obj.name)
		else:
			# TODO: Better way to do this?
			# Clean up all directories
			for dir in os.listdir(distro_obj.name):
				full_dir = distro_obj.name + os.sep + dir
				if os.path.isdir(full_dir):
					shutil.rmtree(full_dir)

		rpms = []
		# Get rpms for this distro
		for pack in glob.glob(config.packaging_dir + os.sep + 'defs/*'):
			pack_obj = packaging.package(distro_obj, os.path.basename(pack), bundle_obj=bundle_conf, package_basepath=package_src_dir)

			# Only if package is valid on this distro, and it's not an 'alias' package (Ex: don't process packages whose pack/source dirs are links to others)
			if pack_obj.valid_use_platform(distro_obj.name) and not pack_obj.info.has_key('source_package_path_name'):
				rpms += pack_obj.get_files(fail_on_missing=False)

		# Get external rpms
		for rpm_file in glob.glob(os.path.join(package_src_dir, '..',  'external_packages', distro_obj.name, "*.rpm")):
			# Skip source rpms
			if not re.compile('\.src\.rpm').search(rpm_file):
				rpms.append(os.path.normpath(rpm_file))

		# Create hard links for all rpms
		for file in rpms:
			arch_dir = distro_obj.name + os.sep + utils.rpm_query('ARCH', file)
			if not os.path.exists(arch_dir):  distutils.dir_util.mkpath(arch_dir)
			
			os.link(file, os.path.join(arch_dir, os.path.basename(file)))


		# Start creating repositories

		if distro_obj.info.has_key('USE_OC') and distro_obj.info['USE_OC']:
			if distro_obj.info.has_key('distro_aliases'):
				DISTRO_STRING = ":".join([distro_obj.name] + distro_obj.info['distro_aliases'])
			else:
				DISTRO_STRING = distro_obj.name
		
			utils.append_text_to_files( {'channel.conf': 'AddDistro %s %s\n' % (DISTRO_STRING, distro_obj.name) } )

		if distro_obj.info.has_key('USE_YUM') and distro_obj.info['USE_YUM']:
			os.system("createrepo " + distro_obj.name)
			shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yum/mono.repo', distro_obj.name)

			utils.substitute_parameters_in_file(distro_obj.name + os.sep + 'mono.repo', { 
				'@DISTRO@': distro_obj.name, 
				'@URL_PREFIX@': url_prefix,
				'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'],
			} )


		# Instructions about how to create a yast repo:
		#http://en.opensuse.org/SDB%3AGenerating_YaST_Installation_Sources
			# Plain cache generated with genIS_PLAINcache in yast2-packagemanager package (also liby2util)
			# REAL yast repo created with create_package_descr in autoyast2-utils package
		if distro_obj.info.has_key('USE_YAST') and distro_obj.info['USE_YAST']:
			# The PLAINcache file is not cross platform... try a 'real' yast source
			#os.system("cd %s; /home/wberrier/yast_install/bin/genIS_PLAINcache -f -r .; gzip IS_PLAINcache ;  cd - " % i)

			# Create a 'real' yast source
			#os.system("cd %s ; mkdir media.1 ; touch media.1/media ; touch content ; ls -A1 > directory.yast ; /home/wberrier/yast_install/bin/create_package_descr -d .; cd -" % i)
			current = os.getcwd()
			os.chdir(distro_obj.name)

			os.mkdir("media.1")
			shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yast/media', 'media.1')

			utils.substitute_parameters_in_file('media.1/media', { 
				'@DATE_STRING@': time.strftime("%Y%m%d%H%M%S")
			} )

			shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yast/content', '.')

			(vendor, ver, base) = distro_obj.name.split('-')

			utils.substitute_parameters_in_file('content', { 
				'@VERSION@': bundle_conf.info['archive_version'],
				'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'],
				'@DISTRO@': distro_obj.name,
				'@BASE_ARCH@': base
			} )

			distutils.dir_util.mkpath('setup/descr')
			# The wiki page didn't say this directory.yast was needed, but newer zypp installation sources seem to require it
			os.system("cd setup/descr ; ls -A1 > directory.yast")

			# Look in the $HOME/bin and if it's not there, rely on it being in the path
			create_yast_path = os.path.join(os.environ['HOME'], 'bin', 'create_package_descr')
			if not os.path.exists(create_yast_path):
				create_yast_path = 'create_package_descr'

			os.system("ls -A1 > directory.yast; " + create_yast_path )

			os.chdir(current)
			


os.system("open-carpet")

# Create hard links for rpms to redcarpet can find them? ... nope, modify xml

# postprocess oc package xml files to change <filename> tag to contain 'arch' dir, 
#  but I'm not sure what other side effects this might have (Joe confirmed this should work)
for xmlfile in glob.glob("*/packageinfo.xml.gz"):
	fd = gzip.GzipFile(xmlfile)
	xml_text = fd.read()
	fd.close()

	xml_doc = xml.dom.minidom.parseString(xml_text)

	for package_node in xml.xpath.Evaluate('/channel/subchannel/package', xml_doc.documentElement):
		# Get arch value
		arch = xml.xpath.Evaluate('arch/text()', package_node)[0].nodeValue

		# Put arch in filename
		filename_node = xml.xpath.Evaluate('history/update/filename/text()', package_node)[0]
		filename_node.nodeValue = arch + os.sep + filename_node.nodeValue

	fd = gzip.GzipFile(xmlfile, 'wb')
	fd.write(xml_doc.toxml())
	fd.close()

