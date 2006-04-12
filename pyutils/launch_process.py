#!/usr/bin/env python

import sys
import getopt

import utils

def usage():
	print "Usage: ./launch_process.py [--terminate_reg=<reg>] [--output_timeout=<secs>] [--kill_process_group] <command>"

def commandline():

        if len(sys.argv) < 2:
                usage()
                sys.exit(1)

	# Options for launch process
	try:
		#opts, command = getopt.gnu_getopt(sys.argv[1:], "", [ "terminate_reg=", "output_timeout=" ])
		opts, command = getopt.getopt(sys.argv[1:], "", [ "terminate_reg=", "output_timeout=", "kill_process_group" ])
	except getopt.GetoptError:
                usage()
		sys.exit(1)
	print "Command '%s'" % command

	# Get args to pass to function
	args = {}
	for option, value in opts:
		if option == "--terminate_reg":
			args['terminate_reg'] = value
		if option == "--output_timeout":
			args['output_timeout'] = int(value)
		if option == "--kill_process_group":
			args['kill_process_group'] = 1

	command = " ".join(command)
	code, output = utils.launch_process(command, **args)
	sys.exit(code)

# If called from the command line, run main, otherwise, functions are callable through imports
if __name__ == "__main__":
        commandline()


