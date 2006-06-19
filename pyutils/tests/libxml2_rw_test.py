#!/usr/bin/env python

import sys
import os
import libxml2

xmlfile = open('../../monobuild/info.xml_new', 'r')

text = xmlfile.read()

xmlfile.close()

doc = ""
#doc = libxml2.parseFile("../info.xml_new")
doc = libxml2.parseMemory(text, len(text) )

#print "\n".join(dir(doc.xpathEval("build")[0]))
#print "\n".join(dir(doc))

# Modify some stuff
doc.xpathEval("build/distro")[0].setContent("redhat-9-i386")

# Write out a new xml doc
file = open('test.xml', 'w')
doc.dump(file)
file.close()

# Cleanup
doc.freeDoc()

