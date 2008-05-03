#!/usr/bin/env python

import sys
import os

sys.path.append('../pyutils')

import config

os.system('curl http://localhost%s/python/monobuild.py | sed  "s/monobuild.py/python\/monobuild.py/g" > www/index.html.new; mv www/index.html.new www/index.html' % config.web_root_url)

