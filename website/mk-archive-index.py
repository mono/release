#!/usr/bin/env python

import sys
import os
import distutils.dir_util
import re
import glob
import getopt

import pdb

sys.path += [ '../pyutils' ]

import packaging
import config
import utils
import build

skip_installers = False
distros = build.get_platforms()
# Command line options
try:
        opts, remaining_args = getopt.getopt(sys.argv[1:], "", [ "skip_installers", "platforms=" ])

	(bundle, output_dir, webroot_path) = remaining_args

        for option, value in opts:
                if option == "--skip_installers":
                         skip_installers = True
                if option == "--platforms":
                        distros = value.split(",")

except:
        print "Usage: ./mk-archive-index.py [ --skip_installers | --platforms=distros ] <bundle name> <output webdir> <webroot_path>"
        print " --platforms: comma separated list of platforms (distros) to include"
        print " --skip_installers: don't include installers in listing"
        sys.exit(1)

bundle_conf = packaging.bundle(bundle_name=bundle)
#print bundle_conf.info

# Create url dirs
out_file = os.path.join(output_dir, "archive", bundle_conf.info['archive_version'], 'download', 'index.html')
distro_out_file = os.path.join(output_dir, 'download-' + bundle_conf.info['bundle_urlname'], 'index.html')
distutils.dir_util.mkpath(os.path.dirname(out_file))

version = bundle_conf.info['archive_version']

bundle_short_desc = bundle_conf.info['bundle_urlname']
if bundle_conf.info.has_key('bundle_short_desc'):
        bundle_short_desc = bundle_conf.info['bundle_short_desc']

#### Sources ####
sources = "<p> <a href='../sources'>Sources</a> </p>"
distro_sources = "<p> <a href='../sources-%s'>Sources</a> </p>" % bundle_conf.info['bundle_urlname']

#### Installers ####

installer_info = [
	{ 'dir_name': 'linux-installer',   'name': 'Linux Installer',         'ext': 'bin'},
	{ 'dir_name': 'windows-installer', 'name': 'Windows Installer',       'ext': 'exe'},
	{ 'dir_name': 'macos-10-universal','name': 'Mac OSX Installer (universal)', 'ext': 'dmg'},
	{ 'dir_name': 'sunos-8-sparc',     'name': 'Solaris 8 SPARC Package', 'ext': 'pkg.gz'}
]

installers = ""
distro_installers = ""
for installer_map in installer_info:

	if skip_installers: continue

	my_dir = os.path.join(output_dir, 'archive', version, installer_map['dir_name'])

	# Skip if the installer doesn't exist for this release
	if not os.path.exists(my_dir):
		continue

	revision = utils.get_latest_ver(my_dir)
	installer_dir = my_dir + os.sep + revision
	ref_dir = "../%s/%s" % (installer_map['dir_name'], revision)
	ref_dir2 = "../archive/%s/%s/%s" % (version, installer_map['dir_name'], revision)

	filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.%s' % installer_map['ext']).pop())
	sum_filename = os.path.basename(glob.glob(installer_dir + os.sep + '*.md5').pop())

	installers += "<p>%s: <a href='%s/%s'>%s</a> [<a href='%s/%s'>MD5SUM</a>] </p>\n" % (installer_map['name'], ref_dir, filename, filename, ref_dir, sum_filename)
	distro_installers += "<p>%s: <a href='%s/%s'>%s</a> [<a href='%s/%s'>MD5SUM</a>] </p>\n" % (installer_map['name'], ref_dir2, filename, filename, ref_dir2, sum_filename)


#### Packages ####
packages = "<ul>"

# Links to distros
for distro_conf in distros:
	conf = packaging.buildconf(os.path.basename(distro_conf), exclusive=False)
	# Skip the distros that use zip packaging system
	if not conf.get_info_var('USE_ZIP_PKG'):
		if conf.get_info_var('distro_aliases'):
			alias_text = "[ " + " | ".join(conf.get_info_var('distro_aliases')) + " ]"
		else: alias_text = ""
		packages += "<li><a href='%s'>%s</a> %s</li>\n" % (conf.name, conf.name, alias_text)

packages += "</ul>"

fd = open(os.path.join(config.release_repo_root, 'website', 'archive-index'))
out_text = fd.read()
fd.close()

distro_out_text = out_text

out_text = out_text.replace('[[webroot_path]]',    webroot_path)
out_text = out_text.replace('[[version]]',    version)
out_text = out_text.replace('[[sources]]',    sources)
out_text = out_text.replace('[[installers]]', installers)
out_text = out_text.replace('[[packages]]',   packages)
out_text = out_text.replace('([[bundle_short_desc]])',   '')

distro_out_text = distro_out_text.replace('[[webroot_path]]',    webroot_path)
distro_out_text = distro_out_text.replace('[[version]]',    version)
distro_out_text = distro_out_text.replace('[[sources]]',    distro_sources)
distro_out_text = distro_out_text.replace('[[installers]]', distro_installers)
distro_out_text = distro_out_text.replace('[[packages]]',   packages)
distro_out_text = distro_out_text.replace('[[bundle_short_desc]]',  bundle_short_desc)

out = open(out_file, 'w')
out.write(out_text)
out.close()

# TODO: Make this part optional if needed later
out = open(distro_out_file, 'w')
out.write(distro_out_text)
out.close()

