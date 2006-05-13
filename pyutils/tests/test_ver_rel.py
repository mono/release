#!/usr/bin/env python

import sys

sys.path += [".."]

import utils

print utils.get_latest_ver('../../packaging/packages/noarch/gtksourceview-sharp-2.0', version='0.10')
print utils.get_latest_ver('../../packaging/packages/noarch/gtksourceview-sharp-2.0')


print utils.get_latest_ver('../../packaging/packages/noarch/gtksourceview-sharp-2.0', version='0.9')


