#!/usr/bin/env python


import sys

sys.path.append('..')

import packaging

conf = packaging.buildconf('sunos-8-sparc')

shell_code = """
for i in `ls /tmp` ; do echo $i ; echo "manual" ; done

if [ "test" == "test2" ] ; then
	echo "no match!"
fi

if [ "test2" == "test2" ] ; then
	echo "match!"
fi


"""

python_code = """

import os

#for i in range(0, 10):
#	print i
#	print os.environ['test']
#	print os.environ['test2']

os.system('ls')
os.system('hostname')
os.system('ls')
	
"""

env = {}
env['test'] = 'tes t3'
env['test2'] = 'test4'

status, output = conf.buildenv.execute_code(shell_code, env=env, working_dir='/tmp')
status, output = conf.buildenv.execute_code(python_code, env=env, interpreter='python', working_dir='/tmp')

