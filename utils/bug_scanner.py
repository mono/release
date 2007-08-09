#!/usr/bin/env python

import re
import sys

try:
	fd = open(sys.argv[1])
except:
	print "Usage: bug_scanner.py <file>"
	print "  File can be a diff, changelog, etc..."
	sys.exit(1)

bugs = {}

for line in fd.readlines():
	bug = re.search('(\d{5})', line) # 5 digits
	rev = re.search('(revision \d{5}|r\d{5})', line)

	if bug and not rev:
		bugs[bug.group(1)] = ""
		print line,

bugs = bugs.keys()
bugs.sort()
print ",".join(bugs)

