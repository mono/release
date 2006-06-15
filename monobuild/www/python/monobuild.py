#!/usr/bin/env python

import os
import sys


# How to import these so they are reimported on change?
import build
import config
import datastore
import utils
import www_utils


def index(req, **vars):

	# Debug to see what's available in req
	#return("\n".join(dir(req)))

	# Validate/sanitize args to catch some common security errors
	vars = www_utils.sanitize_args(vars)

	# Default to HEAD if it's not specified
	if vars.has_key('HEAD_or_RELEASE'):
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	else:
		HEAD_or_RELEASE = 'HEAD'

	if HEAD_or_RELEASE != "HEAD" and HEAD_or_RELEASE != "RELEASE":
		return("Invalid parameters")

	scriptname = os.path.basename(req.canonical_filename)

	# Pull this in from the release repo
	plat_objs = build.get_platform_objs()
	pack_objs = build.get_package_objs()

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

	""" % (HEAD_or_RELEASE, config.web_root_url, config.web_root_url, HEAD_or_RELEASE))

	 
	req.write("""
	<h3>Build Matrix</h3>

	<p>
	<table class="buildstatus">
	""")

	# Get unique list of used platforms
	platforms = {}
	for obj in pack_objs:
		for host in obj.info['BUILD_HOSTS']:
			platforms[host] = ""

	# Remove unused plat_objs
	num_removed = 0
	for i in range(0, len(plat_objs)):
		if not platforms.has_key(plat_objs[i - num_removed].name):
			plat_objs.pop(i - num_removed)
			num_removed += 1
	

	# Separate noarch packages
	noarch_pack_objs = []
	num_removed = 0
	for i in range(0, len(pack_objs)):
		# If it's a noarch package
		# get_destroot': '\n\tDEST_ROOT=noarch\n'
		if pack_objs[i - num_removed].info['get_destroot'].find('noarch') != -1:
			#req.write(pack_objs[i - num_removed].info['get_destroot'])
			noarch_pack_objs.append(pack_objs[i - num_removed])
			pack_objs.pop(i - num_removed)
			num_removed += 1
	

	count = 0

	# Only read once here
	src = datastore.source_file_repo()
	src.load_info()

	# Iterate through arch packages, and then noarch packages
	for (platforms, packs) in  [ (plat_objs, pack_objs), (['noarch'], noarch_pack_objs) ]:
		
		req.write("<thead><tr><td></td>\n")

		for obj in packs:
			req.write("<th>%s</th>\n" % obj.name)

		req.write("</tr></thead>\n<tbody>\n")

		# Add row for mktarball status
		req.write("<tr><th>mktarball</th>\n")
		for package in packs:
			info = src.get_tarball_state_info(HEAD_or_RELEASE, package.name, read_info=False)

			revision = ""
			revision2 = ""
			state = ""
			state2 = ""
			if len(info['revisions']) > 0:
				revision = info['revisions'][0]
				state = info['state'][revision]

				link = "<a href=%s/tarball_logs/%s/%s/%s.log>%s</a>" % (config.web_root_url, HEAD_or_RELEASE, package.name, revision, revision)

				if len(info['revisions']) > 1:
					revision2 = info['revisions'][1]
					state2 = info['state'][revision2]

				if revision2:
					req.write("<td class=%s>" % state2)
					req.write("<center><table class=%s><td>" % (state))
					req.write(link)
					req.write("</td></table></center>")
					req.write("</td>\n")
				else:
					req.write("<td class=%s>" % state)
					req.write(link)
					req.write("</td>\n")

			else:
				req.write("<td class=new>")
				req.write("</td>\n")

		req.write("</tr>\n")
		# End of mktarball row

		# list out non-noarch packages
		for platform in platforms:
			if platform == 'noarch':
				platform_name = "noarch"
			else: platform_name = platform.name

			req.write("<tr><th>%s</th>\n" % platform_name)

			for package in packs:
				#req.write("<br>".join(package.info.keys()))
				if platform == "noarch": platform_name = package.info['BUILD_HOSTS'][0]	
			
				# if this is a valid package for this platform...	
				if package.info['BUILD_HOSTS'].count(platform_name):
					# show the last two builds (otherwise, it's going to mostly be showing yellow)
					versions = build.get_versions(HEAD_or_RELEASE, platform_name, package.name) # in <num> format

					version = ""
					version2 = ""
					state = ""

					# pop and get first version
					if len(versions) > 0:
						version = versions.pop()
						build_info = datastore.build_info(HEAD_or_RELEASE, platform_name, package.name, version)
						state = build_info.get_state()

					# pop and get second version
					if len(versions) > 0:
						version2 = versions.pop()
						build_info2 = datastore.build_info(HEAD_or_RELEASE, platform_name, package.name, version2)
						state2 = build_info2.get_state()

					# if it's a valid package, but hasn't been built yet...
					if state == "":
						state = "new"
						link = ""
					else:
						link = "<a href=%s/packagestatus?platform=%s&package=%s&HEAD_or_RELEASE=%s>%s</a>" % ( scriptname, platform_name, package.name, HEAD_or_RELEASE, version)

					# if there's a previous version, print a container table
					if version2:
						req.write("<td class=%s>" % state2)
						req.write("<center><table class=%s><td>" % (state))
						req.write(link)
						req.write("</td></table></center>")
						req.write("</td>\n")
					else:
						req.write("<td class=%s>" % state)
						req.write(link)
						req.write("</td>\n")
				
				else:
					req.write("<td class=notused>")
					req.write("</td>\n")

			req.write("</tr>\n")

		req.write("</tbody>\n")

		# Separator section ( # Don't write this on the last one )
		if count == 0:
			req.write("<tr><td></td></tr>\n")

		count+= 1
	

	req.write("</table>\n</p>")

        # Legend
	req.write("""

	<h3>Legend</h3>
	<p>
	<table class=legend>

	<tbody>
	<tr>
	<th>In Progress</th>
	<th>Success</th>
	<th>Failed</th>
	<th>Tests Failed</th>
	<th>Timed Out</td>
	<th>Queued</th>
	<th>New</th>
	</tr>

	<td class=inprogress></td>
	<td class=success></td>
	<td class=failure></td>
	<td class=testfailure></td>
	<td class=timeout></td>
	<td class=queued></td>
	<td class=new></td>

	</tbody>
	</table>
	</p>

	""")

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

# List all builds for a platform/package combination
def packagestatus(req, **vars):

	# Validate/sanitize args to catch some common security errors
        vars = www_utils.sanitize_args(vars)


	try:
		platform = vars['platform']
		package = vars['package']
		HEAD_or_RELEASE = vars['HEAD_or_RELEASE']
	except KeyError:
		return "Invalid arguments"

	versions = build.get_versions(HEAD_or_RELEASE, platform, package)
	versions = utils.version_sort(versions)
	versions.reverse()

	if len(versions) <= 10:
		show_links = False
	else:   show_links = True

	# Flag to show all builds or not
	if vars.has_key('showall'):
		showall = True
	else:   showall = False


	# Only show the first 10 versions unless showall link is pushed
	if not showall and len(versions) > 10:
		versions = versions[:10]

	html = ""
	req.content_type = "text/html"

	if versions:
		html += "<h1>%s -- %s -- %s</h1>" % (package, platform, HEAD_or_RELEASE)

		# Print out links...
		if show_links:
			if showall:
				html += "<p><a href='packagestatus?platform=%s&package=%s&HEAD_or_RELEASE=%s'>Show Latest 10 Builds</a></p>" % (platform, package, HEAD_or_RELEASE) 
			else:
				html += "<p><a href='packagestatus?platform=%s&package=%s&HEAD_or_RELEASE=%s&showall=1'>Show Full Build History</a></p>" % (platform, package, HEAD_or_RELEASE) 

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

				# If there's download info, and it exists, add it to the html
				#  (It won't exist on the mirrored public site)
				if step.has_key('download'):
					temp_rel_path =  os.path.join(build_info.rel_files_dir, "files", step['download'])
				else:   temp_rel_path = ""

				if temp_rel_path and os.path.exists(os.path.join(config.web_root_dir, 'builds', temp_rel_path)):

					download_file = os.path.join(config.build_info_url, temp_rel_path)

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


