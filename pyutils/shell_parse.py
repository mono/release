import re
import sys

def parse_file(filename):
	"""Args: shell file.  Returns a dictionary with keys as named elements.
	
	Currently supports variables, arrays, and functions."""


	# Read in string while removing comments from the file string
	try: fd = open(filename, 'r')
	except IOError:
		print "Could not open " + filename
		sys.exit(1)

	shell_string = fd.read()
	
	fd.close()

	return parse_string(shell_string)

def parse_string(shell_string):
	"""Args: string of shell code.  Returns a dictionary with keys as named elements.
	
	Currently supports variables, arrays, and functions."""

	info = {}
	string_no_comments = ""


	# Remove comments from string
	#line_end_reg = re.compile('[(\r\n)\n(\r)]')
	#for line in line_end_reg.split(shell_string):
	#	if not re.compile('^\s*#').search(line):
	#		string_no_comments += line + "\n"
	comment_reg = re.compile('#.*')
	string_no_comments = comment_reg.sub("", shell_string)

	# get vars (var="value")
	# Note: this ingores single and double quotes around the value
	for match in re.compile('^(\w*?)=["\']?([^\(].*?)["\']?$', re.S | re.M).finditer(string_no_comments):
		info[match.group(1)] = match.group(2)

	# get arrays ( var=(value list) )
	for match in re.compile('^(\w*?)=\((.*?)\)', re.S | re.M).finditer(string_no_comments):
		items = match.group(2).split()
		info[match.group(1)] = items

	# get Functions ( func () { } )
	# Note: because of libgdiplus generating the .pc file which includes { and }, the ^} had to be
	# 	added, so just remember that } on a newline always means the end of the function
	for match in re.compile('^(\w*?) \(\) {(.*?)^}', re.S | re.M).finditer(string_no_comments):
		info[match.group(1)] = match.group(2)

	return info

