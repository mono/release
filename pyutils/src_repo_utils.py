
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
default_min_wait = 10

#  svn source repo utils
class svn:

	def __init__(self, root, key_file="", min_wait=default_min_wait, debug=0):

		self.root = root

		self.ssh_options = config.ssh_options
		if key_file:
			self.ssh_options += " -i %s" % key_file

		# Even this won't be used when using svn:// protocol, it won't hurt
		self.svn_env = "SVN_SSH='ssh %s'" % self.ssh_options

		self.svn_options = config.svn_options

		self.last_access = 0
		self.min_wait = min_wait
		self.debug = debug

		# Cache vars
		self.latest_path_revision_cache = {}
		self.cache_max_size = 150
		self.cache_lru = []

	def debug_print(self, text):
		if self.debug:
			print text

	def regulator(self):
		"""Make sure we don't pound the svn server too hard"""
		self.debug_print("DEBUG: Calling regulator")

		time_since_last = int(time.time()) - self.last_access
		self.debug_print("time_since_last: %d" % time_since_last)
		if time_since_last < self.min_wait:
			wait_time = self.min_wait - time_since_last
			self.debug_print("DEBUG: Sleeping: %d" % wait_time)
			time.sleep(wait_time)
		else:
			self.debug_print("DEBUG: min_wait (%d) satisfied, not waiting" % self.min_wait)

		self.last_access = int(time.time())
		

	def latest_tree_revision(self):
		"""Get the last commit version.
		"""

		self.regulator()
		code, output = utils.launch_process('%s svn %s ls %s -v' % ( self.svn_env, self.svn_options, self.root ), print_output=0, output_timeout=output_timeout )

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

			command = '%s svn %s ls %s/%s %s -v' % ( self.svn_env, self.svn_options, self.root , dirname, rev_arg)
			self.debug_print("Command: " + command)

			# Cache output for this command, should lessen load from svn server
			#  Only check if we have a revision
			if revision and self.latest_path_revision_cache.has_key(command):
				self.debug_print("CACHE:hit!")
				(code, output) = self.latest_path_revision_cache[command]

				# find hit and put it at the end of the list
				self.cache_lru.append(self.cache_lru.pop(self.cache_lru.index(command)))
			else:
				self.debug_print("CACHE:miss...")
				self.regulator()

				code, output = utils.launch_process(command, print_output=0, output_timeout=output_timeout)

				self.latest_path_revision_cache[command] = (code, output)
				self.cache_lru.append(command)

				# Cache cleanup, so we don't use up all memory since this is a long running process
				if len(self.cache_lru) > self.cache_max_size:
					self.debug_print("Removing old item from cache")
					self.latest_path_revision_cache.pop(self.cache_lru.pop(0))

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


