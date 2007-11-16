
#

import os.path
import time

# Local modules
import config
import utils

# TODO: add some error checking to die gracefully  (use Exceptions?)

# Exceptions would be nice...

output_timeout=600

# Wait at least x seconds between commands
default_min_wait = 5

#  svn source repo utils
class svn:

	def __init__(self, root, key_file="", min_wait=default_min_wait):

		self.root = root

		self.ssh_options = config.ssh_options
		if key_file:
			self.ssh_options += " -i %s" % key_file

		# Even this won't be used when using svn:// protocol, it won't hurt
		self.svn_env = "SVN_SSH='ssh %s'" % self.ssh_options

		self.last_access = 0
		self.min_wait = min_wait

	def regulator(self):
		"""Make sure we don't pound the svn server too hard"""
		#print "DEBUG: Calling regulator"

		time_since_last = utils.time_duration_asc(self.last_access, utils.get_time() ) * 60
		if time_since_last < self.min_wait:
			wait_time = self.min_wait - time_since_last
			#print "DEBUG: Sleeping: %d" % wait_time
			time.sleep(wait_time)
		#else:
		#	print "DEBUG: min_wait (%d) satisfied, not waiting" % self.min_wait

		self.last_access = utils.get_time()
		

	def latest_tree_revision(self):
		"""Get the last commit version.
		"""

		self.regulator()
		code, output = utils.launch_process('%s svn ls %s -v' % ( self.svn_env, self.root ), print_output=0, output_timeout=output_timeout )

		versions = []
		for line in output.split('\n'):
			list = line.split()
			# Catch network/ssh errors
			try:
				versions.append(int(list[0]))
			except:
				return 0

		versions.sort()

		return versions.pop()

	def latest_path_revision(self, path, revision=0):
		"""given a svn dir path, what's the latest revision for that url at a given revision.

		path can either be a string or sequence of strings
		"""

		# Convert to list
		if path.__class__ == str:
			path = [ path ]

		versions = []

		rev_arg = ""
		if revision: rev_arg = "-r " + str(revision)

		for item in path:
			dirname = os.path.dirname(item)
			module = os.path.basename(item)

			self.regulator()
			code, output = utils.launch_process('%s svn ls %s/%s %s -v' % ( self.svn_env, self.root , dirname, rev_arg), print_output=0, output_timeout=output_timeout )

			for line in output.split('\n'):
				list = line.split()

				# Catch network/ssh errors
				try: 
					version = int(list[0])
				except:
					return 0

				tmp_module = os.path.dirname(list.pop())

				if tmp_module == module:
					versions += [ version ]

		versions.sort()
		return versions.pop()


