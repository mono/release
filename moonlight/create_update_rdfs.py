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

profile = '1.0'
new_version = '1.0.1'
old_versions = ['0.6','0.7','0.8','1.0b1','1.0b2','1.0']    # older versions that will upgrade to new_version
archs = ['i586','x86_64']
versions = old_versions + [new_version] # Note to self: this is intentional. Leave it alone :)

update_link = 'http://go-mono.com/archive/moonlight-plugins'
rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
em_ns = "http://www.mozilla.org/2004/em-rdf#"
max_firefox_version = "3.5.*"

update_info_url = 'http://go-mono.com/archive/moonlight-plugins/latest/update.xhtml'


def get_sha1sum(filename):
	sha = hashlib.sha1()
	f = open(filename,'rb')
	data = f.read()
	sha.update(data)
	return sha.hexdigest()

def create_text_node(doc,name,text):
	node = doc.createElementNS(em_ns,name)
	t_node = doc.createTextNode(text)
	node.appendChild(t_node)
	return node

def create_target_application(doc,xpi):
	sha1sum = get_sha1sum(xpi)
	target = doc.createElementNS(em_ns,"em:targetApplication")
	rdf_desc = doc.createElementNS(None,"Description")
	target.appendChild(rdf_desc)

	rdf_desc.appendChild(create_text_node(doc,"em:id","{ec8030f7-c20a-464f-9b0e-13a3a9e97384}")) # Firefox application GUID
	rdf_desc.appendChild(create_text_node(doc,"em:minVersion","1.5"))
	rdf_desc.appendChild(create_text_node(doc,"em:maxVersion",max_firefox_version))
	rdf_desc.appendChild(create_text_node(doc,"em:updateLink","%s/%s/%s" % (update_link,new_version,xpi)))
	rdf_desc.appendChild(create_text_node(doc,"em:updateHash","sha1:%s" % sha1sum))
	rdf_desc.appendChild(create_text_node(doc,"em:updateInfoURL",update_info_url))
	return target

def create_resource(doc,version,xpi):
	rdf_desc = doc.createElementNS(None,"RDF:Description")
	rdf_desc.setAttributeNS(None,"about","urn:mozilla:extension:moonlight@novell.com:%s" % version)
	em_version = doc.createElementNS(em_ns,"em:version")
	em_version_txt = doc.createTextNode(version)
	em_version.appendChild(em_version_txt)
	rdf_desc.appendChild(em_version)
	rdf_desc.appendChild(create_target_application(doc,xpi))
	return rdf_desc

def create_seq_li(doc,version):
	#rdf_li = doc.createElementNS(rdf_ns,"RDF:li")
	rdf_li = doc.createElementNS(None,"RDF:li")
	rdf_li.setAttributeNS(rdf_ns,"resource","urn:mozilla:extension:moonlight@novell.com:%s" % version)
	return rdf_li

def create_rdf_for_arch(arch):
	xpi = 'novell-moonlight-%s-%s.xpi' % (new_version,arch)
	if not os.path.isfile(xpi):
		print "Missing new xpi file %s" % xpi
		return

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

if __name__ == '__main__':

	for arch in archs:
		create_rdf_for_arch(arch)

