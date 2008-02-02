
import sys
import os
import os.path
import distutils.dir_util
import gzip
import re

class MaxLogOverflowException(Exception):
	def __init__(self, msg, max):
		print "Trying to log '%s': but max_logsize reached: %s MB" % (msg, str(max/1024/1024))

class Logger:

	def __init__(self, filename="log.log", print_screen=1, max_size=0, compressed=1, print_file=1):
		"""Simple logging class.
		filename:	custom filename, otherwise will be log.log
		print_screen:	whether or not to do screen printout
		max_size:	throw exception if log is over this size in MB (0 for no limit, which is the default)
		compressed:	compress while writing log.  Append .gz to filename
		print_file:	output to file
		"""

		self.print_screen = print_screen
		self.full_path = os.path.abspath(filename)

		log_dir = os.path.dirname(self.full_path)
		if not os.path.exists(log_dir):
			distutils.dir_util.mkpath(log_dir)

		self.print_file = print_file

		self.size = 0

		if compressed:
			# NOTE: to get this working in the browser, you must configure apache so:

			# First, and text/plain for .log files: (in mime.types)
			#  text/plain txt asc log

			#  Add encoding so browsers will uncompress on the fly:
			#  AddEncoding x-gzip .gz .tgz
			#
			#  Comment out: application/x-gzip gz
			#  (Can this be done for only certain dirs? or added where necessary?)
			#
			#  Must also add 'MultiViews' to options (because links with .log will automaticall point to .log.gz if the file exists)
			#   (all links on page will point to .log)

			# Append extension
			self.full_path = self.full_path + ".gz"
			if self.print_file:
				# Truncate instead of append, because apache doesn't send anything that has been appended
				#  (maybe apache stops at EOF?, even though there could be more data?)
				self.fd = gzip.open(self.full_path, 'w')
		else:
			if self.print_file:
				self.fd = open(self.full_path, 'a')

		if not max_size:
			self.max_size = 0
		else:
			self.max_size = max_size * (1024 * 1024)

	def __del__(self):
		if self.print_file:
			self.fd.close()

	def log(self, msg):

		if self.print_file:
			self.fd.write(msg)
			self.fd.flush()
		if self.print_screen:
			sys.stdout.write(msg)
			sys.stdout.flush()

		self.size += len(msg)

		# throw exception if there is a size limit and we exceed it
		if self.max_size and self.size > self.max_size:
			raise MaxLogOverflowException(msg, self.max_size)


