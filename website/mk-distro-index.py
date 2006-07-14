#!/usr/bin/env python

import sys
import os
import os.path
import glob
import distutils.dir_util
import re

import pdb

sys.path += [ '../pyutils' ]

import packaging
import config
import utils


def get_rpm_install(env_obj, archive=False):
	return_text = ""

	# Don't display repository information for archive pages
	if archive:
		return return_text

	# For rhel systems...
	#  If there are distro aliases, use those
	if env_obj.info.has_key('distro_aliases'):
		distro_name = env_obj.info['distro_aliases'][0]
	else:
		distro_name = env_obj.name

	# Grab OC stuff from conf file
	vars = {}
	vars['OC_DOWNLOAD_URL'] = "ftp://ftp.ximian.com/pub/redcarpet2/%s" % distro_name
	vars['OC_NOTES'] = ""
	for i in "OC_NOTES OC_DOWNLOAD_URL".split():
		if env_obj.info.has_key(i):
			vars[i] = env_obj.info[i]

	# Generate OC text
	if env_obj.info.has_key('USE_OC') and env_obj.info['USE_OC']:
		return_text += """
		<p>
		This distro supports installing Mono using Novell's Red Carpet.
		If you do not already have Red Carpet, you can <a href='%s'>download</a> it.
		%s
		</p>

		<p>To use Red Carpet, execute these commands:</p>

		<xmp class='shell'>
	rug sa http://go-mono.com/%s
	rug sub mono-%s
	rug in mono-complete gtk-sharp-complete
		</xmp>

		<p>Note: some versions of Red Carpet frequently have IOError timeouts.  This is a bug in Red Carpet.  If Red Carpet for your distro frequently has this problem, please use another installation method.</p>
		<p>""" % (vars['OC_DOWNLOAD_URL'], vars['OC_NOTES'], url_prefix, bundle_conf.info['bundle_urlname'])


	# Generate Yum Text
	if env_obj.info.has_key('USE_YUM') and env_obj.info['USE_YUM']:
		return_text += """
		<p>
		This distro supports installing packages via <tt>yum</tt>. Putting the
		<a href="mono.repo">mono.repo</a> file in <tt>/etc/yum.repos.d</tt> will allow you to
		install mono and related packages.
		</p>
		"""

	# Generate yast text
	if env_obj.info.has_key('USE_YAST') and env_obj.info['USE_YAST']:
		return_text += """
		<p>
		This distro supports installing packages via <tt>YaST</tt>.  Add the following installation
		source to <tt>YaST</tt>:
		<ul>
		<li><tt>http://go-mono.com/%s/%s</tt></li>
		</ul>
		</p>
		<p>For assistance with using repositories and installing packages with YaST, visit this link: 
		<a href="http://en.opensuse.org/Add_Package_Repositories_to_YaST">[1]</a>
                </p>""" % (url_prefix, env_obj.name)


	# TODO: Generate zmd text
	# Hmm... zmd can use all of the above sources...
	if env_obj.info.has_key('USE_ZMD') and env_obj.info['USE_ZMD']:
		pass

		#Only select one category, since they're all valid.
		#if OC
		#elif yum,
		#elif yast

	return return_text

def get_external_deps(env_obj, archive=False):

	if archive:	external_url_path = "../../../../external_packages"
	else:		external_url_path = "../../external_packages"

	return_text = ""

	external_rpms = glob.glob("../external_packages/%s/*.rpm" % env_obj.name)
	external_src_rpms = glob.glob("../external_packages/%s/*.src.rpm" % env_obj.name)
	
	# For the RPMS
	if external_rpms:
		return_text += "<h3>External Dependencies</h3>"
		return_text += "<ul>"
		for i in external_rpms:

			i = os.path.basename(i)

			if re.compile("\.src\.rpm").search(i):
				continue

			(NAME, DESC) = utils.rpm_query(['NAME', 'SUMMARY'], '../external_packages/%s/%s' % (env_obj.name, i) )
			return_text += "<li><a href='%s/%s/%s'>%s</a> -- %s</li>" % (external_url_path, env_obj.name, i, NAME, DESC)
		return_text += "</ul>"

	# For the source RPMS
	if external_src_rpms:
		return_text += "<p>Source RPMS: "
		for i in external_src_rpms:

			i = os.path.basename(i)

			NAME = utils.rpm_query('NAME', '../external_packages/%s/%s' % (env_obj.name, i) )
			return_text += "<a href='%s/%s/%s'>%s</a> " % (external_url_path, env_obj.name, i, NAME)

		return_text += "</p>"

	return return_text


# Command line options
if len(sys.argv) != 4:
        print "Usage: ./mk-distro-index.py <bundle name> <package source dir> <output webdir>"
        sys.exit(1)

bundle = sys.argv[1]
package_src_dir = os.path.abspath(sys.argv[2])
output_dir = sys.argv[3]

bundle_conf = packaging.bundle(bundle_name=bundle)
url_prefix = 'download-' + bundle_conf.info['bundle_urlname']

fd = open(os.path.join(config.release_repo_root, 'website', 'distro-index'))
template = fd.readlines()
fd.close()

version = bundle_conf.info['archive_version']

# Go here so the rpm file globbings look right
os.chdir(package_src_dir)
distros = glob.glob(config.packaging_dir + "/conf/*-*-*")
distros.sort()
for distro_conf in distros:

	env = packaging.buildenv(os.path.basename(distro_conf))
	print "*** Generating pages for: %s" % env.name

	# Skip the distros that use zip packaging system
	if utils.get_dict_var('USE_ZIP_PKG', env.info): continue

	distro_out_dir = os.path.join(output_dir, url_prefix, env.name)
	out_file = distro_out_dir + os.sep + 'index.html'
	arc_out_file = os.path.join(output_dir, 'archive',  version, 'download', env.name, 'index.html')

	distutils.dir_util.mkpath(os.path.dirname(out_file))
	distutils.dir_util.mkpath(os.path.dirname(arc_out_file))

	out = open(out_file, 'w')
	arc_out = open(arc_out_file, 'w')

	for line in template:	
		line_segs = line.split()
		if line_segs and line_segs[0] == "#":
			ARGS = line_segs[2:]
			RPMS = []
			SPECS = []
			for package in ARGS:
				pack_obj = packaging.package(env, package, bundle_obj=bundle_conf, package_basepath=package_src_dir)

				#if pack_obj.name == "gtk-sharp": pdb.set_trace()
				if not pack_obj.valid_use_platform(env.name):
					continue

				# probably won't ever want to post zip files ... ?
				RPMS += pack_obj.get_files_relpath(ext=["rpm"], fail_on_missing=False)

				# Remove src.rpms in case we saved them (which we usually don't)
				for i in RPMS:
					if re.compile(".*\.src\.rpm").search(i):
						RPMS.remove(i)

				SPECS += pack_obj.get_files_relpath(ext="spec", fail_on_missing=False)

			if len(RPMS) == 0:
				out.write("<p>Not available for this platform</p>")
				arc_out.write("<p>Not available for this platform</p>")
				print " * Skipping " + pack_obj.name
				continue
		
			zipname = line_segs[1]
			zip_filename = distro_out_dir + os.sep + zipname + ".zip"
			if os.path.exists(zip_filename):
				os.unlink(zip_filename)

			# If there are more than one rpms to be in the zip file
			if len(RPMS) > 1:
				print "Creating zip: " + zipname
				# rpms are compressed anyways -- doing any compression is a waste of time
				os.system("zip -j -0 %s %s" % (zip_filename, " ".join(RPMS)) )
				
				out.write("<p><a href='%s.zip'><img src='/zip-icon.png' />All of these RPMs in a ZIP file</a></p>" % (zipname))


			out.write("<ul>")
			arc_out.write("<ul>")

			for i in RPMS:
				(NAME, DESC) = utils.rpm_query(['NAME', 'SUMMARY'], i)
				out.write("<li><a href='../../download/%s'>%s</a> -- %s</li>" % (i, NAME, DESC) )
				arc_out.write("<li><a href='../../../../download/%s'>%s</a> -- %s</li>" % (i, NAME, DESC) )
			
			out.write("</ul>")
			arc_out.write("</ul>")

			# Print links to spec files
			if len(SPECS) == 0:
				continue

			out.write("<p>RPM Spec files: ")
			arc_out.write("<p>RPM Spec files: ")
			for i in SPECS:
				NAME = os.path.basename(i)
				out.write("<a href='../../download/%s'>%s</a> " % (i, NAME) )
				arc_out.write("<a href='../../../../download/%s'>%s</a> " % (i, NAME) )

			out.write("</p>")
			arc_out.write("</p>")

			
		elif line_segs and line_segs[0] == "!":
			command = line_segs[1]

			# Strange... but useful way of calling a python function based on a string name
			#  always pass the buildenv object and archive bool
			out.write( eval(command)(env, archive=False) )
			arc_out.write( eval(command)(env, archive=True) )

		else:
			line = line.replace('[[arch]]', env.name)
			line = line.replace('[[version]]', version)

			out.write(line)
			arc_out.write(line)


