
#

import os.path

# Local modules
import config
import utils

# TODO: add some error checking to die gracefully  (use Exceptions?)

output_timeout=600

#  svn source repo utils
class svn:

	def __init__(self, root, key_file=""):

		self.root = root

		self.ssh_options = config.ssh_options
		if key_file:
			self.ssh_options += " -i %s" % key_file

		# Even this won't be used when using svn:// protocol, it won't hurt
		self.svn_env = "SVN_SSH='ssh %s'" % self.ssh_options

	def latest_tree_revision(self):
		"""Get the last commit version.
		"""

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


