#!/usr/bin/env python

import sys
import shutil
import os
import distutils.dir_util
import glob
import time
import re
import getopt
import string

import pdb

sys.path += [ '../pyutils' ]

import build
import config
import packaging
import utils
import rpm_utils

distros = build.get_platforms()
# Command line options
try:
	opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "platforms=" ])
	for option, value in opts:
		if option == "--platforms":
			distros = value.split(",")

	(bundle, output_dir, webroot_path, package_src_dir, hostname_url) = remaining_args

	package_src_dir = os.path.abspath(package_src_dir)
except:
        print "Usage: ./mk-repos.py [ --platforms=<distros> ] <bundle name> <output webdir> <webroot_path> <package source dir> <hostname_url>"
	print " --platforms: comma separated list of platforms (distros) to create distros for"
        sys.exit(1)

bundle_conf = packaging.bundle(bundle_name=bundle)
url_prefix = 'download-' + bundle_conf.info['bundle_urlname']

base_dir = output_dir + os.sep + url_prefix
distutils.dir_util.mkpath(base_dir)
os.chdir(base_dir)

# Load up packages to include in repository (packages_in_repo)
execfile(os.path.join(config.release_repo_root, 'website', 'repo-config', 'config.py') )

# TODO: maybe we should generate the repo data for all repo types for all distros... ?  That might be just confusing...

# Keep track of OBS repos because they are multi-arch
obs_repos = set([])

# Create hard links to real packages to use in repo
for distro in distros:

        distro_obj = packaging.buildconf(distro, exclusive=False)

	# TODO: Come up with repo system for zip system
	if utils.get_dict_var('USE_ZIP_PKG', distro_obj.info):
		pass

	elif utils.get_dict_var('OBS_REPO', distro_obj.info):
		repo_url = utils.get_dict_var('OBS_REPO_URL', distro_obj.info)
		distro_name = string.split(repo_url, "/")[-2]
		# OBS is multi-distro, so we will hit this more than once
		if distro_name in obs_repos:
			continue
		if os.system("lftp -c mirror " + repo_url):
			print "Error. (Is lftp installed?)"
		else:
			obs_repos.add(distro_name)

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
			arch_dir = distro_obj.name + os.sep + rpm_utils.rpm_query('ARCH', file)
			if not os.path.exists(arch_dir):  distutils.dir_util.mkpath(arch_dir)

			# Hrm... seems the shutil.rmtree didn't work... ?
			link = arch_dir + os.sep + os.path.basename(file)
			if not os.path.exists(link):
				os.link(file, link)


		# Start creating repositories
		if utils.get_dict_var('RPM_MD_REPO', distro_obj.info):
			if os.system("createrepo " + distro_obj.name):
				print "Error. (Is createrepo installed?)"
				sys.exit(1)

			if utils.get_dict_var('YUM_INSTALL', distro_obj.info):
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
			gpg_opts = "--no-random-seed-file --no-default-keyring --secret-keyring %s --keyring %s --trustdb-name %s" % (config.release_repo_root + os.sep + "website/secring.gpg", config.release_repo_root + os.sep + "website/pubring.gpg", config.release_repo_root + os.sep + "website/trustdb.gpg")
			ret = os.system("gpg %s -a --detach-sign %s/repodata/repomd.xml" % (gpg_opts, distro_obj.name) )
			ret2 = os.system("gpg %s -a --export E1C55E73 > %s/repodata/repomd.xml.key" % (gpg_opts, distro_obj.name) )
			if ret or ret2:
				print "Error signing repositories..."
				sys.exit(1)


		# Instructions about how to create a yast repo:
		#http://en.opensuse.org/SDB%3AGenerating_YaST_Installation_Sources
			# Plain cache generated with genIS_PLAINcache in yast2-packagemanager package (also liby2util)
			# REAL yast repo created with create_package_descr in autoyast2-utils package
		if utils.get_dict_var('YAST_REPO', distro_obj.info):
			# The PLAINcache file is not cross platform... try a 'real' yast source
			#os.system("cd %s; /home/wberrier/yast_install/bin/genIS_PLAINcache -f -r .; gzip IS_PLAINcache ;  cd - " % i)

			# TODO: Create a signed yast repo (http://en.opensuse.org/Secure_Installation_Sources)
			# Create a 'real' yast source
			#os.system("cd %s ; mkdir media.1 ; touch media.1/media ; touch content ; ls -A1 > directory.yast ; /home/wberrier/yast_install/bin/create_package_descr -d .; cd -" % i)
			current = os.getcwd()
			os.chdir(distro_obj.name)

			os.mkdir("media.1")
			shutil.copy(config.release_repo_root + os.sep + 'website/repo-config/yast/media', 'media.1')
			# zypp in 10.2 requires this directory.yast (as well as 10.1)
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

			# Use the one we checked in
			create_yast_path = os.path.join(config.release_repo_root, 'website', 'create_package_descr')

			if os.system("ls -A1 > directory.yast; " + create_yast_path ):
				print "Error running create_package_descr"
				sys.exit(1)

			os.chdir(current)
			

