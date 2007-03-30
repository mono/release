#!/usr/bin/env python

import os
import sys


# How to import these so they are reimported on change?
import build
import config
import datastore
import utils
import www_utils

doc_type = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">"""

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
	pack_objs, noarch_pack_objs = build.get_package_objs()

        req.content_type = "text/html"

	req.write( """
	%s
	<HTML>
	<HEAD>
	<TITLE>Mono Build Status - %s</TITLE>
	<link rel="stylesheet" href="%s/build.css" type="text/css">
	<script language="javascript" src="%s/build.js" type="text/javascript"></script>
	<meta http-equiv="refresh" content="60">
	</HEAD>
	<BODY>

	<H1>Mono Build Status - %s</H1>

	""" % (doc_type, HEAD_or_RELEASE, config.web_root_url, config.web_root_url, HEAD_or_RELEASE))

	legend_html = """
	
	<h3>Legend</h3>
	<div>
	<table class=legend>

	<tbody>
	<tr>
	<th class=inprogress>In Progress</th>
	<th class=success>Success</th>
	<th class=failure>Failed</th>
	<th class=testfailure>Tests Failed</th>
	<th class=timeout>Timed Out</th>
	<th class=queued>Queued</th>
	<th class=new>New</th>
	</tr>

	</tbody>
	</table>
	</div>"""

	req.write(legend_html)
	 
	req.write("""
	<h3>Build Matrix</h3>

	<div>
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
	
	count = 0

	# Only read once here
	src = datastore.source_file_repo()
	src.load_info()

	# Iterate through arch packages, and then noarch packages
	for (platforms, packs) in  [ (plat_objs, pack_objs), (['noarch'], noarch_pack_objs) ]:
		
		req.write("<tr><td></td>\n")

		for obj in packs:
			req.write("<th>%s</th>\n" % obj.name)

		req.write("</tr>\n")

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

				link = "<a href='%s/tarball_logs/%s/%s/%s.log'>%s</a>" % (config.web_root_url, HEAD_or_RELEASE, package.name, revision, revision)

				if len(info['revisions']) > 1:
					revision2 = info['revisions'][1]
					state2 = info['state'][revision2]

				if revision2:
					req.write("<td class=%s>" % state2)
					req.write("<center><table class=%s><tr><td>" % (state))
					req.write(link)
					req.write("</td></tr></table></center>")
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
						link = "<a href='%s/packagestatus?platform=%s&amp;package=%s&amp;HEAD_or_RELEASE=%s'>%s</a>" % ( scriptname, platform_name, package.name, HEAD_or_RELEASE, version)

					# if there's a previous version, print a container table
					if version2:
						req.write("<td class=%s>" % state2)
						req.write("<center><table class=%s><tr><td>" % (state))
						req.write(link)
						req.write("</td></tr></table></center>")
						req.write("</td>\n")
					else:
						req.write("<td class=%s>" % state)
						req.write(link)
						req.write("</td>\n")
				
				else:
					req.write("<td class=notused>")
					req.write("</td>\n")

			req.write("</tr>\n")

		# Separator section ( # Don't write this on the last one )
		if count == 0:
			req.write("<tr><td></td></tr>\n")

		count+= 1
	

	req.write("</table>\n</div>")

        # Legend
	req.write(legend_html)

	# Link to toggle between HEAD and RELEASE
	if HEAD_or_RELEASE == "RELEASE":
		toggle_link = "HEAD"
	else:   toggle_link = "RELEASE"
	req.write("""<p><a href="%s?HEAD_or_RELEASE=%s">%s Status</a></p>""" % (scriptname, toggle_link, toggle_link) )


	# Footer
	req.write("""

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

	timezone_offset = www_utils.get_tz_cookie(req.headers_in)

	versions = build.get_versions(HEAD_or_RELEASE, platform, package)
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

	refresh_html = ""
	if not showall:
		refresh_html = """<meta http-equiv="refresh" content="60">"""

	req.content_type = "text/html"

	req.write("""
	%s
	<html>
	<head>
	%s
	<title>Mono Build Status</title>
	<link rel="stylesheet" href="%s/build.css" type="text/css">
	</head>

	<body>""" % (doc_type, refresh_html, config.web_root_url) )

	if versions:
		req.write("<h1>%s -- %s -- %s</h1>" % (package, platform, HEAD_or_RELEASE))

		# Print out links...
		if show_links:
			if showall:
				req.write("<p><a href='packagestatus?platform=%s&amp;package=%s&amp;HEAD_or_RELEASE=%s'>Show Latest 10 Builds</a></p>" % (platform, package, HEAD_or_RELEASE) )
			else:
				req.write("<p><a href='packagestatus?platform=%s&amp;package=%s&amp;HEAD_or_RELEASE=%s&amp;showall=1'>Show Full Build History</a></p>" % (platform, package, HEAD_or_RELEASE) )

		for version in versions:

			build_info = datastore.build_info(HEAD_or_RELEASE, platform, package, version)
			values = build_info.get_build_info()

			if values['start'] and values['finish']:
				duration = utils.time_duration_asc(values['start'], values['finish'])
			# Sometimes the latest build isn't the one running (usually a bug), but still show the running time
			elif values['start']:
				duration = "Running for %s" % utils.time_duration_asc(values['start'], utils.get_time())
			else:
				duration = "?"

			# New times based on clients timezone (accurrate?)
			try:
				tz_start = utils.adjust_for_timezone(timezone_offset, values['start'])
				tz_finish = utils.adjust_for_timezone(timezone_offset, values['finish'])
			except:
				raise `version`

			req.write("""

			<h3>Build status - %s</h3>

			<div>
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
			</div>

			<h4>Build Steps</h4>
			<div>
			<table>
			<tbody>""" % (version, tz_start, tz_finish, duration, values['buildhost']) )

			# Start through the build steps...	
			for step in build_info.get_steps_info(read_info=0):

				log = os.path.join(config.build_info_url, build_info.rel_files_dir, 'logs', step['log'])

				req.write("""
				<tr>
				<th>%s</th>
				<td><a href="%s">%s</a></td>
				""" % (step['name'], log, step['state']) )

				# If there's download info, and it exists, add it to the html
				#  (It won't exist on the mirrored public site)
				if step.has_key('download'):
					temp_rel_path =  os.path.join(build_info.rel_files_dir, "files", step['download'])
				else:   temp_rel_path = ""

				if temp_rel_path and os.path.exists(os.path.join(config.web_root_dir, 'builds', temp_rel_path)):

					download_file = os.path.join(config.build_info_url, temp_rel_path)

					req.write("""
					<td><a href="%s">%s</a></td>
					""" % (download_file, step['download']) )
				else:
					req.write("<td></td>")

				if step['start'] and step['finish']:
					req.write("<td>[ %s min(s) ] </td>" % utils.time_duration_asc(step['start'], step['finish']) )
				# Sometimes the latest build isn't the one running (usually a bug), but still show the running time
				elif step['start']:
					req.write("<td>[ Running for %s min(s) ] </td>" % utils.time_duration_asc(step['start'], utils.get_time()) )
				req.write("</tr>")

				
			req.write("</tbody></table></div><br>")


	else:
		req.write("<h1>Mono Build Status</h1>")
		req.write("<p>No information found: %s -- %s -- %s</p>" % (package, platform, HEAD_or_RELEASE) )


	req.write("""
	</body>
	</html>""")

