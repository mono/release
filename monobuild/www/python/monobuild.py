#!/usr/bin/env python

import pdb
import random
import os

import Mono.Build
import Mono.Build.Config


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

	rootUrl = Mono.Build.Config.rootUrl

	# Pull this in from the release repo
	linux_platforms = Mono.Build.getPlatforms()
	linux_packages = Mono.Build.getPackages()

	# Come up with common way to build things not in this framework...
	other_platforms = [
			'sparc',
			'windows',
			'mac'
			]
	other_platforms.sort()
	other_packages = ['mono-1.1']

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

	<FORM name=buildform action="schedulebuild.pl" method=post enctype="multipart/form-data">

	""" % (rootUrl, rootUrl))

	if schedule_flag:
		req.write("""<p><INPUT type=submit Value="Build Selected Packages"></p>""")


	checkbox_html = ""

	if schedule_flag:
		checkbox_html = """Select All <INPUT type=checkbox name=linux onClick=toggleCheckBoxes(document.buildform.build)>"""

	 
	req.write("""
	<h3>Linux Platforms</h3>

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
				req.write("<a href=monobuild.py/packagestatus?platform=%s&package=%s&revision=%s>%s</a>" % ( platform, package, rev, rev))
			

			# Print a checkbox if we're in schedule mode and it's a valid BUILD_HOSTS
			if schedule_flag and state != "notused":
				req.write("""<input type=checkbox name=build value="%s:%s""" % (platform, package))
			
			
			req.write("</td>\n")

		
		req.write("</tr>")
		



	req.write("""</tbody>
	</table>
	</p>""")

	if schedule_flag:
		checkbox_html = """Select All <INPUT type=checkbox name=other onClick=toggleCheckBoxes(document.buildform.build_other)>"""
	else:
		checkbox_html = ""



# Other Systems
	req.write("""
	<h3>Other Platforms</h3>

	<p>
	<table class="buildstatus">
		<thead><td>%s</td>
	""" % checkbox_html)

	for other_platform in other_platforms:

		req.write("<td>%s</td>\n" % other_platform)


	req.write("</thead><tbody>")

	for other_package in other_packages:

		req.write("<tr><td>%s</td>\n" % other_package)

		for other_platform in other_platforms:
		
			# Make sure you don't get unused
			while 1:
			
				rand = randomRev()
				state = randomState(rand)
				if not state == 'notused': break

			req.write("<td class=%s>" % state)

			rev = "r454"

			#req.write("<a href=logs/$package-$platform-$rev$rand.log>$rev$rand</a>";)

			if schedule_flag:
				req.write("""<input type=checkbox name=build_other value=\"%s:%s\"""" % (other_platform, other_package))
			else:
				req.write("<a href=%s/package_status_example.html>%s%s</a>" % ( rootUrl, rev, rand))

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
		req.write("""<p><a href="$ENV{SCRIPT_NAME}">Build Status</a></p>""")
	else:
		req.write("""<p><a href="$ENV{SCRIPT_NAME}?schedule=true">Schedule Builds</a></p>""")


# Footer
	req.write("""
	</FORM>

	</BODY>
	</HTML>
	""")


