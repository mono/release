#!/usr/bin/env python
import csv
import pdb
import os
import sys
from HtUserManagement import *


def readInCsv(filename):
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=',', quotechar='"')
    accountInfo = []

    for curLine in reader:
        accountInfo.append(curLine)

    return accountInfo


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print "Usage: " + os.path.basename(sys.argv[0]) + " <input_file.csv> <output_file.db>"
        sys.exit()

    if (not os.path.isfile(sys.argv[1])):
        print "Error: [" + sys.argv[1] + "] doesn't exist!"
        sys.exit()

    if (not os.path.isfile(sys.argv[2])):
        print "Error: [" + sys.argv[2] + "] doesn't exist!"
        sys.exit()

    if (os.path.isfile(sys.argv[2]+ ".htpasswd")):
        print "Error: [" + sys.argv[2] + "] exists!"
        sys.exit()

    user = HtUserManagement(sys.argv[2])

    accountInfo = readInCsv(sys.argv[1])
    for curAccount in accountInfo[1:]:
        if len(curAccount) == 0:
            continue  #line is a blank line

        username = curAccount[2].lower()
        fullName = curAccount[1]

        try:
            user.addUserWithRandomPassword(username, fullName)
            print ".",
        except Exception,exc:
            if (str(exc) == "Error: [" + username + "] is not a valid e-mail address."):
                print "I",
            elif (str(exc) == "Error: [" + username + "] already exists!"):
                print "E",
            else:
                print str(exc)

    user.writeOutHtpasswd(sys.argv[2] + ".htpasswd")


# vim:ts=4:expandtab:
