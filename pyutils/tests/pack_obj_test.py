#!/usr/bin/env python

import sys

import pdb

sys.path += [ ".." ]

import packaging
pack = packaging.package("", 'mono-1.1.7')

pdb.set_trace()

print pack.info['web_index']


