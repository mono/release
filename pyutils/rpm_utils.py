#!/usr/bin/env python

import re
import commands
import os

child_rpm_match = re.compile("is needed by \(installed\) (\S+)")

rpm_query_cache = {}

def rpm_is_installed(rpm_name):

	(status, output) = commands.getstatusoutput("rpm -q " + rpm_name)

	if status:
		return 0
	else:
		return 1

# Parse rpm -e output to see what other rpms depend on the ones we're trying to remove
def get_dependent_rpms(command_output):

	rpms = []

	for line in command_output.split('\n'):
		if child_rpm_match.search(line):
			rpm = child_rpm_match.search(line).group(1)

			rpms.append(rpm)

	#print "*Dependent rpms: " + " ".join(rpms)

	return rpms

def remove_rpms(rpms, test=False):

	installed_rpms = []

	for rpm in rpms:
		if rpm_is_installed(rpm):
			installed_rpms.append(rpm)
	status = 1

	if test:
		rpm_flags = "--test"
	else:
		rpm_flags = ""

	while status and installed_rpms:
		command = "rpm %s -e %s" % (rpm_flags, ' '.join(installed_rpms) )
		(status, output) = commands.getstatusoutput(command)

		if not status:
			installed_rpms.sort()
			break
		else:
			new_rpms = get_dependent_rpms(output)

			# Only add duplicates
			for rpm in new_rpms:
				if not installed_rpms.count(rpm):
					installed_rpms.append(rpm)

	return installed_rpms

def rpm_query(query_format, file, installed=False):
        """Args: query_format, file.
        query_format can be a list or a string.
        Returns: results of query, which can also be a list (if > 1), or a string (if < 2).

        Ex:  name = rpm_utils.rpm_query('NAME', 'myrpm.rpm')
        Ex:  (name, sum) = rpm_utils.rpm_query(['NAME', 'SUMMARY'], 'myrpm.rpm')

        This function also utilizes a hash cache to speed up the script generation by a couple of minutes."""

        marker = "__MONO__"

        if installed:
                installed = ""
        else:
                installed = "p"

        # Find if query is a string or list
        if query_format.__class__ == str:
                query_format = [ query_format ]

        # Build up query string
        for i in range(0, len(query_format)):
                query_format[i] = "%{" + query_format[i] + "}"

        query_string = marker.join(query_format)

        #print "query: " + query_string
        #print "querying %s for %s" % (file, query_string)

        key = os.path.basename(file) + ":" + query_string

        if rpm_query_cache.has_key(key):
                #print "Cache hit!"
                output = rpm_query_cache[key]
        else:   
		# Must use "nosignature", otherwise that output from stderr gets interpreted as part of the query results
                (code, output) = commands.getstatusoutput("rpm -q%s --nosignature --queryformat \"%s\" %s" % (installed, query_string, file))
                rpm_query_cache[key] = output

        results = output.split(marker)
        if len(results) <= 1:
                results = output

        return results

