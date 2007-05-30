#!/usr/bin/env python


import sys

sys.path.append('..')

import packaging

conf = packaging.buildconf('suse-102-x86_64')

code = """
for i in `ls /tmp` ; do echo $i ; echo "manual" ; done
"""

code = """

import os

#for i in range(0, 10):
#	print i
#	print os.environ['test']
#	print os.environ['test2']

os.system('ls')
os.system('hostname')
	
"""

#code = 'test.sh'

env = {}
env['test'] = 'tes t3'
env['test2'] = 'test4'

status, output = conf.buildenv.execute_code(code, env=env, interpreter="python", working_dir='/home')

