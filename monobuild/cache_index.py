#!/usr/bin/env python

import sys
import os

sys.path.append('../pyutils')

import config

os.system('curl %s | sed  "s/monobuild.py/python\/monobuild.py/g" | sed "s/\.\.\///g" > www/index.html.new; mv www/index.html.new www/index.html' % sys.argv[1])

