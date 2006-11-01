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

# try some execute options
host = sshutils.init('builder@hardhat.boston.ximian.com', print_output=1)
host.execute('find /', max_output_size=10000)
host.execute('ls /tmp/sdfl')
host.execute('ls /tmp/sdfl; sleep 15', output_timeout=10)
host.execute('find /', terminate_reg="h.me")
host.execute('find /', terminate_reg="h.me", output_timeout=10, max_output_size=10000)

