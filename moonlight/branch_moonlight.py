#!/usr/bin/env python

# Get these revision numbers from #moonlight

import os
import sys
import subprocess

import MoonlightReleases

def executeCmd(command, stderr=open(os.devnull)):
    print command
    ret = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=stderr)
    output = ret.communicate()[0]
    lines = output.split('\n')
    return lines

def branch(preview,mono_rev,moonlight_rev):

    host='svn+ssh://rhowell@mono-cvs.ximian.com/source'
    mono='%s/branches/mono-2.6/mono' % host
    mcs='%s/branches/mono-2-6/mcs' % host
    moonlight='%s/trunk/moon' % host
    mono_basic='%s/branches/mono-2-6/mono-basic' % host
    branch='%s/branches/moon/%s' % (host,preview)

    print host
    print branch


    # Create the branch
    cmd = 'svn mkdir -m " * Creating branch for Moonlight %s" %s' % (preview,branch)
    executeCmd(cmd)

    print " * Branching mono r%s for Moonlight %s" % (mono_rev,preview)
    cmd = 'svn cp -m " * Branching mono r%s for Moonlight %s" -r%s %s %s' % (mono_rev,preview,mono_rev,mono,branch)
    executeCmd(cmd)

    print " * Branching mcs r%s for Moonlight %s" % (mono_rev,preview)
    cmd = 'svn cp -m " * Branching mcs r%s for Moonlight %s" -r%s %s %s' % (mono_rev,preview,mono_rev,mcs,branch)
    executeCmd(cmd)

    print " * Branching moon r%s for Moonlight %s" % (moonlight_rev,preview)
    cmd = 'svn cp -m " * Branching moon r%s for Moonlight %s" -r%s %s %s' % (moonlight_rev,preview,moonlight_rev,moonlight,branch)
    executeCmd(cmd)

    print " * Branching mono-basic r%s for Moonlight %s" % (mono_rev,preview)
    cmd = 'svn cp -m " * Branching mono-basic r%s for Moonlight %s" -r%s %s %s' % (mono_rev,preview,mono_rev,mono_basic,branch)
    executeCmd(cmd)

    cmd = 'svn co -N %s/moon moon-%s' % (branch,preview)
    executeCmd(cmd)

def main():

    preview = MoonlightReleases.latest['release']
    mono_rev = MoonlightReleases.latest['monorev']
    moonlight_rev = MoonlightReleases.latest['moonrev']

    print "\n      preview = %s" % preview
    print "     Mono Rev = %s" % mono_rev
    print "Moonlight Rev = %s\n" % moonlight_rev

    CHAR = raw_input("Continue branching for Moonlight %s? (yes,NO): " % preview)

    if CHAR != 'yes':
        print "Aborting branch"
        sys.exit(1)

    print "Branching Moonlight %s" % preview
    branch(preview,mono_rev,moonlight_rev)

    print "\nUpdate the version numbers in moon-%s/configure.ac\n" % preview

if __name__ == '__main__':
    main()


# vim:ts=4:noexpandtab:

