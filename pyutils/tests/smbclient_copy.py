#!/usr/bin/env python

import sys
import string
import os

sys.path.append('..')

import remote_shell

host = remote_shell.smbclient(username='builder', hostname='cygwin-mono.boston.ximian.com', env={'SMB_SHARE': 'msys'})

if not os.path.exists('tmp'): os.mkdir('tmp')

host.copy_to(['*.py'], '/tmp')
host.copy_to(['../../packaging/sources/libgdiplus/*'], '/tmp')

host.copy_to(['../../packaging/sources/libgdiplus/*'], '/tmp')
host.copy_to(['../../packaging/sources/libgdiplus/*'], '/')

host.copy_from(['/tmp/libgdiplus*'], 'tmp')

