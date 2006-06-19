#!/usr/bin/env python

import sys

sys.path += [ '../../pyutils' ]

import build
import datastore

platform = 'suse-93-i586'
package = 'gecko-sharp-2.0'
version = '4543'

build_info = datastore.build_info('HEAD', platform, package, version)

print build_info.get_state()


