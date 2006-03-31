#!/usr/bin/env python

import os
import sys


# How to import these so they are reimported on change?
import build
import config
import packaging
import datastore
import utils

def index(req, **vars):

	# Debug to see what's available in req
	#return("\n".join(dir(req)))

	# Default to HEAD if it's not specified
	if vars.has_key('HEAD_or_RELEASE'):
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	else:
		HEAD_or_RELEASE = 'HEAD'

	if HEAD_or_RELEASE != "HEAD" and HEAD_or_RELEASE != "RELEASE":
		return("Invalid parameters")

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
	<TITLE>Mono Build Status - %s</TITLE>
	<link rel="stylesheet" href="%s/build.css" type="text/css">
	<script language="javascript" src="%s/build.js"></script>
	</HEAD>
	<BODY>

	<H1>Mono Build Status - %s</H1>

	<FORM name=buildform action="%s/schedulebuild" method=get enctype="multipart/form-data">

	""" % (HEAD_or_RELEASE, config.web_root_url, config.web_root_url, HEAD_or_RELEASE, scriptname))

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
				req.write("<a href=%s/packagestatus?platform=%s&package=%s&HEAD_or_RELEASE=%s>%s</a>" % ( scriptname, platform, package, HEAD_or_RELEASE, version))
			

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

# TODO: Should probably show all builds on this page
def packagestatus(req, **vars):


	try:
		platform = vars['platform']
		package = vars['package']
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	except KeyError:
		return "Invalid arguments"

	versions = build.get_versions(HEAD_or_RELEASE, platform, package)

	versions = utils.version_sort(versions)

	versions.reverse()

	html = ""
	req.content_type = "text/html"

	if versions:
		html += "<h1>%s -- %s -- %s</h1>" % (package, platform, HEAD_or_RELEASE)

		counter = 0

		for version in versions:

			build_info = datastore.build_info(HEAD_or_RELEASE, platform, package, version)
			values = build_info.get_build_info()

			if values['start'] and values['finish']:
				duration = utils.time_duration_asc(values['start'], values['finish'])
			elif values['start'] and counter == 0:
				duration = "Running for %s" % utils.time_duration_asc(values['start'], utils.get_time())
			else:
				duration = "?"
		
			html += """

				<h3>Build status - %s</h3>

				<p>
				<table>
				<tbody>
				<tr>
				<th>Build started:</th>

				<td>%s</td>

				<th>Build completed:</th>
				<td>%s</td>

				<th>Duration:</th>
				<td>%s min(s)</td>

				</tr>

				<tr>
				<th>Build host:</th>
				<td>%s</td>

				</tr>
				</tbody></table>

				<h4>Build Steps</h4>
				<p>
				<table>
				<tbody>""" % (version, values['start'], values['finish'], duration, values['buildhost'])

			# Start through the build steps...	
			for step in build_info.get_steps_info(read_info=0):

				log = os.path.join(config.build_info_url, build_info.rel_files_dir, 'logs', step['log'])

				html += """
						<tr>
						<th>%s</th>
						<td><a href="%s">%s</a></td>
					 """ % (step['name'], log, step['state'])

				# If there's download info, add it to the html
				if step['download']:

					download_file = os.path.join(config.build_info_url, build_info.rel_files_dir, "files", step['download'])

					html += """
							<td><a href="%s">%s</a></td>
						""" % (download_file, step['download'])
				else:
					html += "<td></td>"

				if step['start'] and step['finish']:
					html += "<td>[ %s min(s) ] </td>" % utils.time_duration_asc(step['start'], step['finish'])
				elif step['start'] and counter == 0:
					html += "<td>[ Running for %s min(s) ] </td>" % utils.time_duration_asc(step['start'], utils.get_time())
				html += "</tr>"

				
			html += "</tbody></table></p><br>"

			# Update version counter
			counter += 1


	else:
		html += "<h1>Mono Build Status</h1>"
		html += "<p>No information found: %s -- %s -- %s</p>" % (package, platform, HEAD_or_RELEASE) 


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
	latest_rev = "57777"
	latest_rev = "57635"

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

