#!/usr/bin/python

# This file should print a valid update.rdf file for Moonlight
# It should include <RDF:Seq> and <RDF:li> tags for all Moonlight versions
# that should be updated by this file.

import xml.dom.minidom
import xml.dom.ext


doc = None
rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
em_ns = "http://www.mozilla.org/2004/em-rdf#"

def get_sha1sum():
	pass

def prettyprint(doc):
	xml.dom.ext.PrettyPrint(doc)

def create_text_node(name,text):

	node = doc.createElementNS(em_ns,name)
	t_node = doc.createTextNode(text)
	node.appendChild(t_node)
	return node

def create_target_application():
	target = doc.createElementNS(em_ns,"em:targetApplication")
	rdf_desc = doc.createElementNS(rdf_ns,"RDF:Description")
	target.appendChild(rdf_desc)

	rdf_desc.appendChild(create_text_node("em:id","{ec8030f7-c20a-464f-9b0e-13a3a9e97384}"))
	rdf_desc.appendChild(create_text_node("em:minVersion","1.5"))
	rdf_desc.appendChild(create_text_node("em:maxVersion","3.1.*"))
	rdf_desc.appendChild(create_text_node("em:updateLink","http://go-mono.com/archive/moonlight-plugins/latest/novell-moonlight-1.0.1-i586.xpi"))
	rdf_desc.appendChild(create_text_node("em:updateHash","sha1:85e01afad312a6af7028703049b6eb329ac82327"))
	rdf_desc.appendChild(create_text_node("em:updateInfoURL","http://go-mono.com/archive/moonlight-plugins/latest/update.xhtml"))

	return target


def create_seq_li(version):

	rdf_li = doc.createElementNS(rdf_ns,"RDF:li")
	rdf_desc = doc.createElementNS(rdf_ns,"RDF:Description")
	rdf_li.appendChild(rdf_desc)
	em_version = doc.createElementNS(em_ns,"em:version")
	em_version_txt = doc.createTextNode(version)
	em_version.appendChild(em_version_txt)
	rdf_desc.appendChild(em_version)
	rdf_desc.appendChild(create_target_application())
	return rdf_li

def main():
	global doc
	doc = xml.dom.minidom.Document()

	rdf_rdf = doc.createElementNS(rdf_ns,"RDF:RDF")
	doc.appendChild(rdf_rdf)
	rdf_desc = doc.createElementNS(rdf_ns,"RDF:Description")
	rdf_desc.setAttributeNS(rdf_ns,"about","urn:mozilla:extension:moonlight@novell.com")
	rdf_rdf.appendChild(rdf_desc)
	em_updates = doc.createElementNS(em_ns,"em:updates")
	rdf_desc.appendChild(em_updates)

	rdf_seq = doc.createElementNS(em_ns,"RDF:Seq")
	em_updates.appendChild(rdf_seq)

	for version in ["0.8","1.0b1","1.0"]:
		rdf_li = create_seq_li(version)
		rdf_seq.appendChild(rdf_li)
	



	prettyprint(doc)

if __name__ == '__main__':
	main()
