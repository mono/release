#!/usr/bin/env python

import sys
import os
import distutils.dir_util
import re
import glob

import pdb

sys.path += [ '../pyutils' ]

import packaging
import config
import utils

# Command line options
if len(sys.argv) != 3:
        print "Usage: ./mk-archive-index.py <bundle name> <output webdir>"
        sys.exit(1)

bundle = sys.argv[1]
output_dir = sys.argv[2]

bundle_conf = packaging.bundle(bundle_name=bundle)
#print bundle_conf.info

# Create url dirs
out_file = os.path.join(output_dir, "archive", bundle_conf.info['archive_version'], 'download', 'index.html')
distutils.dir_util.mkpath(os.path.dirname(out_file))

version = bundle_conf.info['archive_version']

#### Sources ####
sources = "<p> <a href='../sources'>Sources</a> </p>"


#### Installers ####

installer_info = [
	{ 'dir_name': 'linux-installer',   'name': 'Linux Installer',         'ext': 'bin'},
	{ 'dir_name': 'windows-installer', 'name': 'Windows Installer',       'ext': 'exe'},
	{ 'dir_name': 'macos-10-ppc',      'name': 'Mac OSX Installer',       'ext': 'dmg'},
	{ 'dir_name': 'sunos-8-sparc',     'name': 'Solaris 8 SPARC Package', 'ext': 'pkg.gz'}
]

installers = ""
for installer_map in installer_info:
		
	revision = utils.get_latest_ver(os.path.join(output_dir, 'archive', version, installer_map['dir_name']))
	installer_dir = os.path.join(output_dir, 'archive', version, installer_map['dir_name'], revision)
	ref_dir = "../%s/%s" % (installer_map['dir_name'], revision)

	filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.%s' % installer_map['ext']).pop())
	sum_filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.md5').pop())

	installers += "<p>%s: <a href='%s/%s'>%s</a> [<a href='%s/%s'>MD5SUM</a>] </p>" % (installer_map['name'], ref_dir, filename, filename, ref_dir, sum_filename)


#### Packages ####
packages = "<ul>"

# Links to distros
for distro_conf in glob.glob(config.packaging_dir + os.sep + 'conf/*-*-*'):

	env = packaging.buildenv(os.path.basename(distro_conf))
	# Skip the distros that use zip packaging system
	if not env.info['USE_ZIP_PKG']:
		packages += "<li><a href='%s'>%s</a></li>" % (env.name, env.name)

packages += "</ul>"

fd = open(os.path.join(config.release_repo_root, 'website', 'archive-index'))
out_text = fd.read()
fd.close()

out_text = out_text.replace('[[version]]',    version)
out_text = out_text.replace('[[sources]]',    sources)
out_text = out_text.replace('[[installers]]', installers)
out_text = out_text.replace('[[packages]]',   packages)

out = open(out_file, 'w')
out.write(out_text)
out.close()

