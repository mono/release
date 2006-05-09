#!/usr/bin/env python

import sys

sys.path += [".."]

import packaging

#env = packaging.buildenv('sles-9-x86_64')
env = packaging.buildenv('win-4-i386')
print env.info

#pack = packaging.package(env, 'gecko-sharp-2.0')
pack = packaging.package(env, 'mono')
print pack.info
