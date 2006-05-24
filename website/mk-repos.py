#!/usr/bin/env python

import sys
import shutil
import os
import distutils.dir_util
import glob
import time

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

	if line_segs and line_segs[0] == "!":
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
					if not distro_conf.info['USE_ZIP_PKG']:
						distutils.dir_util.mkpath(chan + os.sep + distro_conf.name)

						for rpm_file in glob.glob(os.path.join(external_dir, distro_conf.name, "*.rpm")):
							# Skip source rpms
							if not re.compile('\.src\.rpm').search(rpmfile):
								# Add rpm to the channel for this distro
								os.link(rpm_file, chan + os.sep + distro_conf.name)


			elif line_segs2 and line_segs2[0] == "!":

				package = line_segs2[1]

				# Create hard links to real packages to use in repo
				for distro_conf in distro_objs:

					pack_obj = packaging.package(distro_conf, package, bundle_obj=bundle_conf)
					# Only non-zip distros and valid distros for this package
					if not distro_conf.info['USE_ZIP_PKG'] and pack_obj.valid_use_platform(distro_conf.name):

						distutils.dir_util.mkpath(chan + os.sep + distro_conf.name)
						for file in pack_obj.get_files_relpath(fail_on_missing=False):
							os.link(package_src_dir + os.sep + file, os.path.join(chan, distro_conf.name, os.path.basename(file)))

			# (Normal text)
			else:
				line2 = line2.replace('[[name]]', serverconf)
				chan_conf.write(line2)


		# Set up each channel for each distro
		for i in glob.glob(chan + os.sep + "*-*-*"):
			distro_obj = packaging.buildenv(os.path.basename(i))

			if distro_obj.info.has_key('distro_aliases'):
				DISTRO_STRING = ":".join([distro_obj.name] + distro_obj.info['distro_aliases'])
			else:
				DISTRO_STRING = distro_obj.name

			
			if distro_obj.info.has_key('USE_OC') and distro_obj.info['USE_OC']:
				chan_conf.write("AddDistro %s %s\n" % (DISTRO_STRING, distro_obj.name) )

			if distro_obj.info.has_key('USE_YUM') and distro_obj.info['USE_YUM']:
				os.system("createrepo " + i)
	
			# Instructions about how to create a yast repo:
			#http://en.opensuse.org/SDB%3AGenerating_YaST_Installation_Sources
				# Plain cache generated with genIS_PLAINcache in yast2-packagemanager package (also liby2util)
				# REAL yast repo created with create_package_descr in autoyast2-utils package
			if distro_obj.info.has_key('USE_YAST') and distro_obj.info['USE_YAST']:
				# The PLAINcache file is not cross platform... try a 'real' yast source
				#os.system("cd %s; /home/wberrier/yast_install/bin/genIS_PLAINcache -f -r .; gzip IS_PLAINcache ;  cd - " % i)

				#pdb.set_trace()
				# Create a 'real' yast source
				#os.system("cd %s ; mkdir media.1 ; touch media.1/media ; touch content ; ls -A1 > directory.yast ; /home/wberrier/yast_install/bin/create_package_descr -d .; cd -" % i)
				current = os.getcwd()
				os.chdir(i)
				os.mkdir("media.1")
				fd = open('media.1/media', 'w')
				fd.write('Novell\n')
				fd.write(time.strftime("%Y%m%d%H%M%S") + "\n")
				fd.write('1\n')
				fd.close()

				fd = open('content', 'w')
				fd.write("PRODUCT Mono\n")
				fd.write("VERSION %s\n" % bundle_conf.info['archive_version'])
				fd.write("LABEL Novell Mono - %s\n" % distro_obj.name)
				fd.write("VENDOR Novell, Inc.\n")

				# Doesn't hurt to have all the arch types here...
				fd.write("ARCH.i386 i386 noarch\n")
				fd.write("ARCH.i486 i486 i386 noarch\n")
				fd.write("ARCH.i586 i586 i486 i386 noarch\n")
				fd.write("ARCH.i686 i686 i586 i486 i386 noarch\n")
				fd.write("ARCH.x86_64 x86_64 i686 i586 i486 i386 noarch\n")
				fd.write("ARCH.s390 s390 noarch\n")
				fd.write("ARCH.s390x s390x s390 noarch\n")
				fd.write("ARCH.ia64 ia64 noarch\n")
				fd.write("ARCH.ppc ppc noarch\n")

				fd.write("DEFAULTBASE %s\n" % distro_obj.info['arch'])

				fd.write("DESCRDIR setup/descr\n")
				fd.write("DATADIR .\n")
				fd.close()

				# It appears that 'arch' must be in the filename... ugh...
				# Create rpm dir structure for yast repo (hardlinks)
				for rpm in glob.glob("*.rpm"):
					arch = utils.rpm_query("ARCH", rpm)
					if not os.path.exists(arch): distutils.dir_util.mkpath(arch)
					os.link(rpm, arch + os.sep + rpm)

				distutils.dir_util.mkpath('setup/descr')
				# The wiki page didn't say this directory.yast was needed, but newer zypp installation sources seem to require it
				os.system("cd setup/descr ; ls -A1 > directory.yast")

				os.system("ls -A1 > directory.yast; create_package_descr")

				os.chdir(current)
				

		chan_conf.close()

	# Else, write oc conf out to file
	else:
		server_file.write(line)

server_file.close()

os.system("open-carpet")

