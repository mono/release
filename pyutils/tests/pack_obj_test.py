#!/usr/bin/env python

import sys

sys.path += [ ".." ]

import packaging
pack = packaging.package("", 'mono-1.1')

print pack.info['web_index']


