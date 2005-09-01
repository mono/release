__all__ = ["Config"]

import Mono.Build.Config
import os
import os.path
import tempfile
import commands
import sys
import string
import libxml2

def get_env_var(var_name, source):

        tmp_script = tempfile.mktemp()

	my_script = open(tmp_script, 'w')
	my_script.write(". %s\n" % source)
	my_script.write("echo ${%s[@]}\n" % var_name)
	my_script.close()

	(status, output) = commands.getstatusoutput("sh %s" % tmp_script)

	os.unlink(tmp_script)

	return output

def getPlatforms():
	platforms = []

	#opendir(DIR, $dir) or die "Can't open dir: $dir\n";

	for entry in os.listdir(Mono.Build.Config.platformDir):
		if entry != "." and entry != ".." and entry != ".svn" and entry != "hosts":
			platforms.append(entry)

	platforms.sort()
	return platforms


def getPackages():

	packages = []

	for entry in os.listdir(Mono.Build.Config.packageDir):
	
		# For some reason... .svn fails the -d perl test...???
		if not os.path.isdir(entry) and entry != ".svn":
			packages.append(entry)

	packages.sort()
	return packages

def getPackageInfo(pkg, var):

	return get_env_var( var, Mono.Build.Config.packageDir + os.sep + pkg )

def getLatestRevision(platform, package):

	revisions = []

	# If this doesn't get overwritten, a build hasn't been don for this platform/package combo
	revision = ""

	try:

		for entry in os.listdir(Mono.Build.Config.buildsDir + os.sep + platform + os.sep + package):
			# For some reason... .svn fails the -d perl test...???
			#if(!-d $dir)
			if dir != "." and dir != ".." and dir != ".svn":
				revisions.append(entry)
	

		revisions.sort()
		revision = revisions.pop()

	except OSError:
		pass

	return revision

# Get the state of a package on a platform
def getState(platform, package, revision):

	xmlFile = os.path.join(Mono.Build.Config.buildsDir, platform, package, revision, "info.xml")

	#if os.path.exists(xmlFile):
	try:
		doc = libxml2.parseFile(xmlFile)
		state = doc.xpathEval("build/state")[0].content
	except libxml2.parserError:
		state = ""

	return state;



