
#

import os.path
import commands

# Local modules
import config

# TODO: add some error checking to die gracefully  (use Exceptions?)

#  svn source repo utils
class svn:

	def __init__(self, root, key_file=""):

		self.root = root

		self.auth_env = ""
		if key_file:
			self.auth_env = "SVN_SSH='ssh -i %s'" % key_file

	def latest_tree_revision(self):
		"""Get the last commit version.
		"""

		output = commands.getoutput('%s svn ls %s -v' % ( self.auth_env, self.root ) )

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

			output = commands.getoutput('%s svn ls %s/%s %s -v' % ( self.auth_env, self.root , dirname, rev_arg) )

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


