#!/usr/bin/env python

import sys

sys.path += [ '../pyutils' ]

import packaging

env = packaging.buildenv('sles-9-i586')
#env = packaging.buildenv('win-4-i386')
env = packaging.buildenv('macos-10-ppc')

pack = packaging.package(env, 'mono-1.1.13')

print pack.info['POSTBUILD_STEP_NAME1']
print pack.info['POSTBUILD_STEP1']

env.ssh.print_command=1
environment = {}
environment['HEAD_or_RELEASE'] = "HEAD"

pack.info['POSTBUILD_STEP1'] = """

python -c 'print 'hey''

"""


env.ssh.execute(pack.info['POSTBUILD_STEP1'], env=environment)

