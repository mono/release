
import sys

import os
import os.path
import distutils.dir_util

import re

#line_reg = re.compile('%s$' % os.linesep, re.M)

class MaxLogOverflowException(Exception):
	def __init__(self, msg, max):
		print "Trying to log '%s': but max_logsize reached: %s MB" % (msg, str(max/1024/1024))

class Logger:

	def __init__(self, filename="log.log", print_screen=1, max_size=0):
		"""Simple logging class.
		filename:	custom filename, otherwise will be log.log
		print_screen:	whether or not to do screen printout
		max_size:	throw exception if log is over this size in MB (0 for no limit, which is the default)
		"""

		self.print_screen = print_screen
		self.full_path = os.path.abspath(filename)

		log_dir = os.path.dirname(self.full_path)
		if not os.path.exists(log_dir):
			distutils.dir_util.mkpath(log_dir)

		self.fd = open(self.full_path, 'a')

		if not max_size:
			self.max_size = 0
		else:
			self.max_size = max_size * (1024 * 1024)

	def __del__(self):
		self.fd.close()

	def log(self, msg):

		# If string doesn't have a line ending, add one (so I don't have to constantly pass in '\n')
		# Can't do this, because we're not logging by line anymore (logging chunks)
		#if not line_reg.search(msg): 
		#	msg += os.linesep

		# throw exception if there is a size limit and we exceed it
		if self.max_size and self.fd.tell() + len(msg) > self.max_size:
			raise MaxLogOverflowException(msg, self.max_size)

		self.fd.write(msg)
		self.fd.flush()
		if self.print_screen:
			sys.stdout.write(msg)
			sys.stdout.flush()



