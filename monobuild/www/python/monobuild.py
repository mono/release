#!/usr/bin/env python

import pdb
import random
import os

import sys
import libxml2
import pickle

import Mono.Build
import Mono.Build.Config

# Some global vars...
rootUrl = Mono.Build.Config.rootUrl

def randomRev():
	return random.randint(1,3)


def randomState(index):

	states = [
			'notused',
			'success', 
			'failure', 
			'inprogress' 
		 ]
 
	return states[index]

def index(req, **vars):


	scriptname = os.path.basename(req.canonical_filename)

	# Pull this in from the release repo
	linux_platforms = Mono.Build.getPlatforms()
	linux_packages = Mono.Build.getPackages()

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

	""" % (rootUrl, rootUrl, scriptname))

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

	for platform in linux_platforms:
		req.write("<td>%s</td>\n" % platform)

	req.write("</thead><tbody>")


	for package in linux_packages:

		req.write("<tr><td>%s</td>\n" % package)
		buildhosts = Mono.Build.getPackageInfo(package, "BUILD_HOSTS")

		rev = ""
		state = ""

		for platform in linux_platforms:
		
		
			# If this is a valid package for this platform...	
			if buildhosts.count(platform):
				# Then start reading the xml...
					# Currently this reads a ton of xml files... might need to aggregate these later...
						# But, that means it's more difficult to remove builds...  issue? 
				rev = Mono.Build.getLatestRevision(platform, package) # in r<num> format
				state = Mono.Build.getState(platform, package, rev)

				# if it's a valid package, but hasn't been built yet...
				if rev == "" and state == "":
					state = "new"
			
			else:
			
				state = "notused"
			


			req.write("<td class=%s>" % state)

			# Print a link if there has been a build, and we're not in schedule mode
			if state != 'notused' and state != 'new' and not schedule_flag:
				req.write("<a href=%s/packagestatus?platform=%s&package=%s&revision=%s>%s</a>" % ( scriptname, platform, package, rev, rev))
			

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
		req.write("""<p><a href="%s?schedule=true">Schedule Builds</a></p>""" % scriptname)


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
		revision = vars['revision']
	except KeyError:
		return "Invalid arguments"

	meta_files_path = os.path.join("..", "..", Mono.Build.Config.buildsUrl, platform, package, revision)

	# Just for testing...
	#platform = "suse-93-i586"
	#package = "gecko-sharp-2.0"
	#revision = "r4543"

	html = ""
	req.content_type = "text/html"

	# Figure out where the xml file is at
	xmlFile = os.path.join(Mono.Build.Config.buildsDir, vars['platform'], vars['package'], vars['revision'], "info.xml")

	# Try to open and get data out of the xml document
	try:

		xmldoc = libxml2.parseFile(xmlFile)

		buildhost = xmldoc.xpathEval("build/buildhost")[0].content
		start = xmldoc.xpathEval("build/start")[0].content
		finish = xmldoc.xpathEval("build/finish")[0].content
	
		html += """

			<h1>%s  -- %s -- %s</h1>

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
			<tbody>""" % (package, platform, revision, start, finish, buildhost)

		count = 0
		# Start through the build steps...	

		for step in xmldoc.xpathEval("build/steps/step"):

			#html += "<br>".join(dir(step))
			#html += "<br>" + step.type
			
			name = step.xpathEval("name")[0].content
			state = step.xpathEval("state")[0].content

			log = os.path.join(meta_files_path, 'logs', step.xpathEval("log")[0].content)

			html += """
					<tr>
					<th>%s</th>
					<td><a href="%s">%s</a></td>
				 """ % (name, log, state)

			# If there's download info, add it to the html
			try:
				download = step.xpathEval("download")[0].content

				download_file = os.path.join(meta_files_path, "files", download)

				html += """
						<td><a href="%s">%s</a></td>
						</tr>
					""" % (download_file, download)
			except IndexError:
				pass

			
		html += "</tbody></table></p>"


		xmldoc.freeDoc()

	# Couldn't find the xml file...
	except libxml2.parserError:
		html += "<h1>Mono Build Status</h1>"
		html += "<p>No information found: %s -- %s -- %s</p>" % (package, platform, revision) 


	req.write("""
	<html><head>

	<title>Mono Build Status</title><link rel="stylesheet" href="%s/build.css" type="text/css"></head>

	<body>

	%s

	</body>
	</html>""" % (rootUrl, html))



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

		<p>""" % rootUrl

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

