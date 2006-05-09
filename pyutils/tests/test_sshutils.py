#!/usr/bin/env python

import sys
import string

sys.path += [ ".." ]

import sshutils

# Normal host
host = sshutils.init('builder@mono-sparc.boston.ximian.com', print_output=1)
host.execute('ls'),
host.execute('ls /tmp/sdfl'),

host.copy_from('/tmp/scratch', 'junk')
host.copy_from(['/tmp/do-build', '/tmp/rem*' ], '.')

host.copy_to('*.py', '/tmp')
host.copy_to(['test_sshutils.pyc', 'rem*' ], '/tmp')


# Test a chroot
host = sshutils.init('builder@monobuild1.boston.ximian.com', jaildir='/jails/redhat-9-i386-duncan-1', print_output=1)
host.execute('ls'),
host.execute('ls /tmp/sdfl'),

host.copy_from('/tmp/scratch', 'junk')
host.copy_from(['/tmp/do-build', '/tmp/rem*' ], '.')

host.copy_to('*.py', '/tmp')
host.copy_to(['test_sshutils.pyc', 'rem*' ], '/tmp')


