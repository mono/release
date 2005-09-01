#!/usr/bin/env python


import commands
import tempfile
import os

import Mono.Build

data = Mono.Build.get_env_var("USE_HOSTS", "/home/wade/wa/msvn/release/packaging/defs/boo")
print data.split()


data = Mono.Build.get_env_var("TEST", "/home/wade/wa/msvn/release/packaging/defs/boo")

print data

if not data:
	print "I didn't find any data!"

