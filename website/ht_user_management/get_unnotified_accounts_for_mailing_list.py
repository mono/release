#!/usr/bin/env python
import pdb
import os
import sys
from HtUserManagement import *


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print "Usage: " + os.path.basename(sys.argv[0]) + " <input.db>"
        sys.exit()

    if (not os.path.isfile(sys.argv[1])):
        print "Error: [" + sys.argv[1] + "] doesn't exist!"
        sys.exit()

    user = HtUserManagement(sys.argv[1])
    allusers = {}

    user.printAllUnnotifiedUsers()

# vim:ts=4:expandtab:
