
import sys

import os
import os.path
import distutils.dir_util

import re

line_reg = re.compile('%s$' % os.linesep, re.M)

class Logger:

	def __init__(self, filename="log.log", print_screen=1):
		self.print_screen = print_screen


		self.full_path = os.path.abspath(filename)

		log_dir = os.path.dirname(self.full_path)
		if not os.path.exists(log_dir):
			distutils.dir_util.mkpath(log_dir)

		self.fd = open(self.full_path, 'a')
		

	def __del__(self):
		self.fd.close()

	def log(self, msg):

		# If string doesn't have a line ending, add one (so I don't have to constantly pass in '\n')
		if not line_reg.search(msg): 
			msg += os.linesep

		self.fd.write(msg)
		self.fd.flush()
		if self.print_screen:
			print msg,
			sys.stdout.flush()



