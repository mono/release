#!/usr/bin/env python

import os
import sys
import random

import xml.xpath
import xml.dom.minidom

import pdb

# How to import these so they are reimported on change?
import build
import config
import packaging
import datastore


def index(req, **vars):

	# Default to HEAD if it's not specified
	if vars.has_key('HEAD_or_RELEASE'):
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	else:
		HEAD_or_RELEASE = 'HEAD'

	scriptname = os.path.basename(req.canonical_filename)

	# Pull this in from the release repo
	platforms = build.get_platforms()
	packages = build.get_packages()

	schedule_flag = ""
	if vars.has_key("schedule"): schedule_flag = vars["schedule"]

	req.content_type = "text/html"

	req.write( """
	<HTML>
	<HEAD>
	<TITLE>Mono Build Status</TITLE>
	<link rel="stylesheet" href="%s/build.css" type="text/css">
	<script language="javascript" src="%s/build.js"></script>
	</HEAD>
	<BODY>

	<H1>Mono Build Status</H1>

	<FORM name=buildform action="%s/schedulebuild" method=get enctype="multipart/form-data">

	""" % (config.web_root_url, config.web_root_url, scriptname))

	if schedule_flag:
		req.write("""<p><INPUT type=submit Value="Build Selected Packages"></p>""")


	checkbox_html = ""

	if schedule_flag:
		checkbox_html = """Select All <INPUT type=checkbox name=linux onClick=toggleCheckBoxes(document.buildform.build)>"""

	 
	req.write("""
	<h3>Build Matrix</h3>

	<p>
	<table class="buildstatus">
		<thead><td>%s</td>
	""" % checkbox_html)

	for platform in platforms:
		req.write("<td>%s</td>\n" % platform)

	req.write("</thead><tbody>")


	for package in packages:

		req.write("<tr><td>%s</td>\n" % package)
		pack_obj = packaging.package("", package)
		buildhosts = pack_obj.info['BUILD_HOSTS']

		version = ""
		state = ""

		for platform in platforms:
		
			# If this is a valid package for this platform...	
			if buildhosts.count(platform):
				# Then start reading the xml...
					# Currently this reads a ton of xml files... might need to aggregate these later...
						# But, that means it's more difficult to remove builds...  issue? 
				version = build.get_latest_version(HEAD_or_RELEASE, platform, package) # in <num> format

				build_info = datastore.build_info(HEAD_or_RELEASE, platform, package, version)

				state = build_info.get_state()

				# if it's a valid package, but hasn't been built yet...
				if version == "" and state == "":
					state = "new"
			
			else:
			
				state = "notused"


			req.write("<td class=%s>" % state)

			# Print a link if there has been a build, and we're not in schedule mode
			if state != 'notused' and state != 'new' and not schedule_flag:
				req.write("<a href=%s/packagestatus?platform=%s&package=%s&version=%s&HEAD_or_RELEASE=%s>%s</a>" % ( scriptname, platform, package, version, HEAD_or_RELEASE, version))
			

			# Print a checkbox if we're in schedule mode and it's a valid BUILD_HOSTS
			if schedule_flag and state != "notused":
				req.write("<input type=checkbox name=build value=\"%s:%s\"" % (platform, package))
			
			
			req.write("</td>\n")

		
		req.write("</tr>")
		



	req.write("""</tbody>
	</table>
	</p>""")


	# Legend
	req.write("""

	<h3>Legend</h3>
	<p>
	<table class=legend>

	<tbody>
	<tr><th>In Progress</th><td class=inprogress></td></tr>
	<tr><th>Success</td><td class=success></td></tr>
	<tr><th>Failed</td><td class=failure></td></tr>
	<tr><th>Queued</td><td class=queued></td></tr>
	<tr><th>New</td><td class=new></td></tr>

	</tbody>
	</table>
	</p>

	""")

	if schedule_flag:
		req.write("""<p><a href="%s">Build Status</a></p>""" % scriptname)
	else:
		#req.write("""<p><a href="%s?schedule=true">Schedule Builds</a></p>""" % scriptname)
		pass

	# Link to toggle between HEAD and RELEASE
	if HEAD_or_RELEASE == "RELEASE":
		toggle_link = "HEAD"
	else:   toggle_link = "RELEASE"
	req.write("""<p><a href="%s?HEAD_or_RELEASE=%s">%s Status</a></p>""" % (scriptname, toggle_link, toggle_link) )


	# Footer
	req.write("""
	</FORM>

	</BODY>
	</HTML>
	""")

def packagestatus(req, **vars):


	try:
		platform = vars['platform']
		package = vars['package']
		version = vars['version']
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	except KeyError:
		return "Invalid arguments"


	build_info = datastore.build_info(HEAD_or_RELEASE, platform, package, version)

	# Just for testing...
	#platform = "suse-93-i586"
	#package = "gecko-sharp-2.0"
	#revision = "r4543"

	html = ""
	req.content_type = "text/html"


	# Try to open and get data out of the xml document
	if build_info.exists:

		xmldoc = build_info.doc

		values = {}
		for key in ['buildhost', 'start', 'finish' ]:
			node = xml.xpath.Evaluate('/build/%s/text()' % key, build_info.doc.documentElement)[0]
			if node:
				values[key] = node.nodeValue
			else: values[key] = ""
	
		html += """

			<h1>%s -- %s -- %s</h1>

			<h3>Build status</h3>

			<p>
			<table>
			<tbody>
			<tr>
			<th>Build started:</th>

			<td>%s</td>

			<th>Build completed:</th>
			<td>%s</td>

			</tr>

			<tr>
			<th>Build host</th>
			<td>%s</td>

			</tr>
			</tbody></table>

			<h3>Build Steps</h3>
			<p>
			<table>
			<tbody>""" % (package, platform, version, values['start'], values['finish'], values['buildhost'])

		count = 0
		# Start through the build steps...	

		for step in xml.xpath.Evaluate('/build/steps/step', build_info.doc.documentElement):

			name = xml.xpath.Evaluate('name/text()', step)[0].nodeValue
			state = xml.xpath.Evaluate('state/text()', step)[0].nodeValue
			log = os.path.join(config.build_info_url, build_info.rel_files_dir, 'logs', xml.xpath.Evaluate('log/text()', step)[0].nodeValue)

			html += """
					<tr>
					<th>%s</th>
					<td><a href="%s">%s</a></td>
				 """ % (name, log, state)

			# If there's download info, add it to the html
			try:
				download = xml.xpath.Evaluate('download/text()', step)[0].nodeValue

				download_file = os.path.join(config.build_info_url, build_info.rel_files_dir, "files", download)

				html += """
						<td><a href="%s">%s</a></td>
						</tr>
					""" % (download_file, download)
			except IndexError:
				pass

			
		html += "</tbody></table></p>"


	# Couldn't find the xml file...
	else:
		html += "<h1>Mono Build Status</h1>"
		html += "<p>No information found: %s -- %s -- %s</p>" % (package, platform, version) 


	req.write("""
	<html><head>

	<title>Mono Build Status</title><link rel="stylesheet" href="%s/build.css" type="text/css"></head>

	<body>

	%s

	</body>
	</html>""" % (config.web_root_url, html))



def schedulebuild(req, **vars):

	builds = ""
	scriptname = os.path.basename(req.canonical_filename)

	# Only select keys if they exist, and make sure the args are always treated as lists
	if vars.has_key('build'):
		builds = vars['build']
		if builds.__class__ != list:
			builds = [ builds ]
		

	html = """
		<HTML>
		<HEAD>
			<TITLE>Mono Build Control</TITLE>
			<link rel="stylesheet" href="%s/build.css" type="text/css">
		</HEAD>
		<BODY>

		<H1>Mono Build Control</H1>

		<H3>Scheduled the following builds</H3>

		<p>""" % config.web_root_url

	#latest_rev = Mono.Build.getLatestTreeRevision()
	latest_rev = "r57777"
	latest_rev = "r57635"

	#if latest_rev:
	#	html += "Error scheduling build<br>"

	html += "Tree revision: %s<br>" % latest_rev

	for build in builds:
		#html += "Build: " + build + "<br>"

		(platform, package) = build.split(":")
		html += "Platform: %s, package: %s<br>" % (platform, package)
		Mono.Build.scheduleBuild(platform, package, latest_rev)

	html += """

		<a href=../%s>Back</a>

		</p>

		</BODY>
		</HTML>""" % scriptname

	req.content_type = "text/html"
	req.write(html)

