import re

def parse(filename):
	"""Args: shell file.  Returns a dictionary with keys as named elements.
	
	Currently supports variables, arrays, and functions."""

	file_string = ""
	info = {}

	# Read in string while removing comments from the file string
	try: fd = open(filename, 'r')
	except IOError:
		print "Could not open " + filename
		sys.exit(1)
	
	for line in fd:
		if not re.compile('^\s*#').search(line):
			file_string += line
	fd.close()

	# get vars (var="value")
	# Note: this ingores single and double quotes around the value
	for match in re.compile('^(\w*?)=["\']?([^\(].*?)["\']?$', re.S | re.M).finditer(file_string):
		info[match.group(1)] = match.group(2)

	# get arrays ( var=(value list) )
	for match in re.compile('^(\w*?)=\((.*?)\)', re.S | re.M).finditer(file_string):
		items = match.group(2).split()
		info[match.group(1)] = items

	# get Functions ( func () { } )
	for match in re.compile('^(\w*?) \(\) {(.*?)}', re.S | re.M).finditer(file_string):
		info[match.group(1)] = match.group(2)

	return info

