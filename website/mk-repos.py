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
try:
	(script_name, bundle, output_dir, webroot_path, package_src_dir, hostname_url) = sys.argv
	package_src_dir = os.path.abspath(package_src_dir)
except:
        print "Usage: ./mk-repos.py <bundle name> <package source dir> <output webdir> <hostname_url> <webroot_path>"
        sys.exit(1)

bundle_conf = packaging.bundle(bundle_name=bundle)
url_prefix = 'download-' + bundle_conf.info['bundle_urlname']

base_dir = output_dir + os.sep + url_prefix
distutils.dir_util.mkpath(base_dir)
os.chdir(base_dir)

# Load up packages to include in repository (packages_in_repo)
execfile(os.path.join(config.release_repo_root, 'website', 'repo-config', 'config.py') )

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
	if utils.get_dict_var('USE_ZIP_PKG', distro_obj.info):
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
		for pack in packages_in_repo:
			pack_obj = packaging.package(distro_obj, os.path.basename(pack), bundle_obj=bundle_conf, package_basepath=package_src_dir)

			# Only if package is valid on this distro
			if pack_obj.valid_use_platform(distro_obj.name):
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

		if utils.get_dict_var('USE_OC', distro_obj.info):
			if distro_obj.info.has_key('distro_aliases'):
				DISTRO_STRING = ":".join([distro_obj.name] + distro_obj.info['distro_aliases'])
			else:
				DISTRO_STRING = distro_obj.name
		
			utils.append_text_to_files( {'channel.conf': 'AddDistro %s %s\n' % (DISTRO_STRING, distro_obj.name) } )

		if utils.get_dict_var('USE_YUM', distro_obj.info) or utils.get_dict_var('USE_ZMD', distro_obj.info):
			os.system("createrepo " + distro_obj.name)

			if utils.get_dict_var('USE_YUM', distro_obj.info):
				shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yum/mono.repo', distro_obj.name)

				utils.substitute_parameters_in_file(distro_obj.name + os.sep + 'mono.repo', { 
					'@DISTRO@': distro_obj.name, 
					'@URL_PREFIX@': url_prefix,
					'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'],
					'@BUNDLE_NAME@': bundle_conf.info['bundle_urlname'],
					'@HOSTNAME_URL@': hostname_url,
					'@WEBROOT_PATH@': webroot_path,
				} )

			# Sign repo
			os.system("gpg -a --detach-sign %s/repodata/repomd.xml" % distro_obj.name)
			os.system("gpg -a --export E1C55E73 > %s/repodata/repomd.xml.key" % distro_obj.name)


		# Instructions about how to create a yast repo:
		#http://en.opensuse.org/SDB%3AGenerating_YaST_Installation_Sources
			# Plain cache generated with genIS_PLAINcache in yast2-packagemanager package (also liby2util)
			# REAL yast repo created with create_package_descr in autoyast2-utils package
		if utils.get_dict_var('USE_YAST', distro_obj.info):# or utils.get_dict_var('USE_ZMD', distro_obj.info):
			# The PLAINcache file is not cross platform... try a 'real' yast source
			#os.system("cd %s; /home/wberrier/yast_install/bin/genIS_PLAINcache -f -r .; gzip IS_PLAINcache ;  cd - " % i)

			# TODO: Create a signed yast repo (http://en.opensuse.org/Secure_Installation_Sources)
			# Create a 'real' yast source
			#os.system("cd %s ; mkdir media.1 ; touch media.1/media ; touch content ; ls -A1 > directory.yast ; /home/wberrier/yast_install/bin/create_package_descr -d .; cd -" % i)
			current = os.getcwd()
			os.chdir(distro_obj.name)

			os.mkdir("media.1")
			shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yast/media', 'media.1')
			# zypp in 10.2 requires this directory.yast
			os.system("cd media.1 ; ls -A1 > directory.yast")

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

