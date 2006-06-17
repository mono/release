#!/usr/bin/env python

import sys

sys.path += [".."]

import packaging
import shell_parse

#env = packaging.buildenv('sles-9-x86_64')
env = packaging.buildenv('win-4-i386')
print env.info

#pack = packaging.package(env, 'gecko-sharp-2.0')
pack = packaging.package(env, 'mono')
print pack.info

print "---------------------------------------------------------------------"

pack_def = shell_parse.parse_file('../../packaging/defs/libgdiplus')

print pack_def['macos_10_ppc_ZIP_BUILD']

print "---------------------------------------------------------------------"
