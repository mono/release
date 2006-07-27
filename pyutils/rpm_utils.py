#!/usr/bin/env python

import re
import commands

child_rpm_match = re.compile("is needed by \(installed\) (\S+)")

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


