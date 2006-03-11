
#

import os.path
import commands

# Local modules
import config

# TODO: add some error checking to die gracefully  (use Exceptions?)

#  svn source repo utils
class svn:

	def __init__(self, root):

		self.root = root

	def latest_tree_revision(self):
		"""Get the last commit version.
		"""

		output = commands.getoutput('svn ls %s -v' % ( self.root ) )

		versions = []
		for line in output.split('\n'):
			list = line.split()
			versions.append(int(list[0]))

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

			output = commands.getoutput('svn ls %s/%s %s -v' % ( self.root , dirname, rev_arg) )

			for line in output.split('\n'):
				list = line.split()
				version = int(list[0])
				tmp_module = os.path.dirname(list.pop())

				if tmp_module == module:
					versions += [ version ]

		versions.sort()
		return versions.pop()


