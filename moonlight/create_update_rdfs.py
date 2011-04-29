#!/usr/bin/python

# This file should print a valid update.rdf file for Moonlight
# It should include <RDF:Seq> and <RDF:li> tags for all Moonlight versions
# that should be updated by this file.

# this script should follow the format on this site:
# http://www.mozilla.org/projects/cck/firefox/update_site.html
# It works for 1.9.0.1

import xml.dom.minidom
import xml.dom.ext
import subprocess
import sys
import os
import hashlib
import getopt

# GLOBALS

profile = '3.0'
new_version = None
old_versions = None # older versions that will upgrade to new_version
archs = ['i586','x86_64']
versions = []
debug = False

base_link = 'http://go-mono.com/archive/moonlight-plugins'
rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
em_ns = "http://www.mozilla.org/2004/em-rdf#"

min_firefox_version = "1.5"
max_firefox_version = "3.6.*"
firefox_guid = '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}'

min_seamonkey_version = "2.0b1"
max_seamonkey_version = "2.0.*"
seamonkey_guid = '{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a}'


############################################################################################
#
# Helper functions
# 

value_args = {'profile=':'Silverlight Profile of the plugin',
		'new_version=':'New version of the plugin',
		'old_versions=':'Comma separated list of older versions that will upgrade',
		'archs=':'Comma separated list of computer archs for the plugin (Defaults to i586,x86_64)',
		'debug':'Prints the current values',
		'help':'Prints this help message'}


def get_args(cli_args):
	global profile,archs
	global new_version,old_versions,versions
	global debug

	debug = False
	shortopts = "hp:n:a:o:d"
	longopts = value_args.keys()
	opts,args = getopt.getopt(cli_args,shortopts,longopts)
	
	for o,a in opts:
		if o in ('-h','--help'):
			usage()
			sys.exit(1)
		elif o in ('-p','--profile'):
			profile = a
		elif o in ('-n','--new_version'):
			new_version = a
		elif o in ('-a','--archs'):
			archs = a.split(',')
		elif o in ('-o','--old_versions'):
			old_versions = a.split(',')
		elif o in ('-d','--debug'):
			debug = True
		else:
			print "ERROR: unhandled option %s" % o

	if old_versions != None and new_version != None:
		versions = old_versions + [new_version] # Note to self: this is intentional. Leave it alone :)
	else:
		versions = []

	if debug:
		print "archs = %s" % str(archs)
		print "profile = %s" % profile
		print "new_version = %s" % new_version
		print "old_versions = %s" % str(old_versions)

#-------------------------------------------------------------------------------------

def usage():
	print "\nUsage: %s [OPTIONS]\n" % sys.argv[0]

	options = value_args.items()
	options.sort()

	for (k,v) in options:
		print '     ',
		print ('--'+ k).ljust(25),v.ljust(50)
	print ''

	print 'Example: ./create_update_rdfs.py --profile=2.0 --archs=i586,x86_64 --new_version=1.9.3 --old_versions=1.9.0,1.9.1,1.9.2'
	print ''

#-------------------------------------------------------------------------------------

def checkValues():
	isValid = True
	if profile == None or profile == '':
		print "Error: profile is not set"
		isValid = False
	if archs == None or archs == []:
		print "Error: archs is not set"
		isValid = False
	if new_version == None or new_version == "":
		print "Error: new_version is not set"
		isValid = False
	if old_versions == None or old_versions == []:
		print "Error: old_versions is not set"
		isValid = False

	if not isValid:
		sys.exit(1)
		

############################################################################################
#
# Functions to create the RDF file
#

def get_updateInfoUrl():
	url = "%s/%s/%s" % (base_link,new_version,get_updateInfoFile())
	return url

def get_updateInfoFile():
	name = "info-%s.xhtml" % new_version
	return name

def get_sha1sum(filename):
	sha = hashlib.sha1()
	try:
		f = open(filename,'rb')
		data = f.read()
		sha.update(data)
		return sha.hexdigest()
	except:
		pass

#-------------------------------------------------------------------------------------
def create_text_node(doc,name,text):
	node = doc.createElementNS(em_ns,name)
	t_node = doc.createTextNode(text)
	node.appendChild(t_node)
	return node

#-------------------------------------------------------------------------------------
def create_SeaMonkey_target_application(doc,xpi):
	return __create_target_application(doc,xpi,seamonkey_guid,min_seamonkey_version,max_seamonkey_version);

#-------------------------------------------------------------------------------------
def create_Firefox_target_application(doc,xpi):
	return __create_target_application(doc,xpi,firefox_guid,min_firefox_version,max_firefox_version);

#-------------------------------------------------------------------------------------
def __create_target_application(doc,xpi,guid,min,max):
	sha1sum = get_sha1sum(xpi)
	target = doc.createElementNS(em_ns,"em:targetApplication")
	rdf_desc = doc.createElementNS(None,"Description")
	target.appendChild(rdf_desc)

	rdf_desc.appendChild(create_text_node(doc,"em:id",guid))
	rdf_desc.appendChild(create_text_node(doc,"em:minVersion",min))
	rdf_desc.appendChild(create_text_node(doc,"em:maxVersion",max))
	rdf_desc.appendChild(create_text_node(doc,"em:updateLink","%s/%s/%s" % (base_link,new_version,xpi)))
	rdf_desc.appendChild(create_text_node(doc,"em:updateHash","sha1:%s" % sha1sum))
	rdf_desc.appendChild(create_text_node(doc,"em:updateInfoURL",get_updateInfoUrl()))
	return target

#-------------------------------------------------------------------------------------
def create_resource(doc,version,xpi):
	rdf_desc = doc.createElementNS(None,"RDF:Description")
	rdf_desc.setAttributeNS(None,"about","urn:mozilla:extension:moonlight@novell.com:%s" % version)
	em_version = doc.createElementNS(em_ns,"em:version")
	em_version_txt = doc.createTextNode(version)
	em_version.appendChild(em_version_txt)
	rdf_desc.appendChild(em_version)
	rdf_desc.appendChild(create_Firefox_target_application(doc,xpi))
	rdf_desc.appendChild(create_SeaMonkey_target_application(doc,xpi))
	return rdf_desc

#-------------------------------------------------------------------------------------
def create_seq_li(doc,version):
	#rdf_li = doc.createElementNS(rdf_ns,"RDF:li")
	rdf_li = doc.createElementNS(None,"RDF:li")
	rdf_li.setAttributeNS(rdf_ns,"resource","urn:mozilla:extension:moonlight@novell.com:%s" % version)
	return rdf_li

#-------------------------------------------------------------------------------------
def create_rdf_for_arch(arch):
	xpi = 'novell-moonlight-%s-%s.xpi' % (new_version,arch)
	update_rdf = 'update-%s-%s.rdf' % (profile,arch)
	print "Creating %s" % update_rdf

	doc = xml.dom.minidom.Document()

	rdf_rdf = doc.createElementNS(rdf_ns,"RDF:RDF")
	doc.appendChild(rdf_rdf)
	rdf_desc = doc.createElementNS(None,"RDF:Description")
	rdf_desc.setAttributeNS(rdf_ns,"about","urn:mozilla:extension:moonlight@novell.com")
	rdf_rdf.appendChild(rdf_desc)
	em_updates = doc.createElementNS(em_ns,"em:updates")
	rdf_desc.appendChild(em_updates)

	rdf_seq = doc.createElementNS(None,"RDF:Seq")
	em_updates.appendChild(rdf_seq)

	#Create the top RDF:Seq
	for version in versions:
		rdf_li = create_seq_li(doc,version)
		rdf_seq.appendChild(rdf_li)

	# Create the descriptions for each resource
	for version in versions:
		rdf_resource = create_resource(doc,version,xpi)
		rdf_rdf.appendChild(rdf_resource)

	f = open(update_rdf,'w')
	xml.dom.ext.PrettyPrint(doc,f)
	f.close()

	return True


#####################################################################################
#
# Functions to create info.xhmlt
#

def create_template_xhtml():
	xhtml = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
   <title>Update Information for Moonlight</title>
</head>
<body>
   <h1>Update Information for Moonlight %s</h1>

   <ul>
       <li>Item #1</li>
   </ul>
</body>
</html>
''' % (new_version)



	updatefile = 'info-%s.xhtml' % new_version
	print "Creating %s" % updatefile

	f = open(updatefile,'w')
	f.write(xhtml)
	f.close()

#####################################################################################
#
# MAIN
#

def create_rdfs(m_new_version,m_old_versions,m_profile=None,m_archs=None):
	global profile
	global new_version
	global old_versions
	global archs
	global versions

	new_version = m_new_version
	old_versions = m_old_versions

	if m_profile != None:
		profile = m_profile

	if m_archs != None:
		archs = m_archs

	if old_versions != None and new_version != None:
		versions = old_versions + [new_version] # Note to self: this is intentional. Leave it alone :)
	else:
		versions = []

	checkValues()
	main()

def main():
	for arch in archs:
		xpi = 'novell-moonlight-%s-%s.xpi' % (new_version,arch)
		if not os.path.isfile(xpi):
			print "Missing new xpi file %s" % xpi
			if not debug:
				continue

		create_rdf_for_arch(arch)
	create_template_xhtml()

if __name__ == '__main__':
	get_args(sys.argv[1:])
	checkValues()
	main()


# vim:ts=4:noexpandtab:
