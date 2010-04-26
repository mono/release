#!/usr/bin/env python

# This script is to take the signed.zip file from the signing lab and perform 
#  the necessary steps to prepare the update.rdf and fix the zip file

import os
import sys
import glob
import zipfile
import shutil
import subprocess
import hashlib
import pdb
import tempfile

import MoonlightReleases
import create_update_rdfs

MCCOY_EXE="/home/rhowell/code/moonlight-ms/moz_ext_update/mccoy/mccoy"

#------------------------------------------------------------------------------
def executeCmd(command, stderr=open(os.devnull)):
    ret = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=stderr)
    output = ret.communicate()[0]
    lines = output.split('\n')
    return lines


#------------------------------------------------------------------------------
def clean():
    # Delete any old generated files
    #pdb.set_trace()

    return

    files = glob.glob("novell*xpi")
    files.extend(glob.glob("update*rdf"))
    files.extend(glob.glob("info*xhtml"))
    files.extend(glob.glob("sha1sums-*"))
    for f in files:
        os.remove(f)
    print "cleaned"


#------------------------------------------------------------------------------
def get_sha1sum(filename):
    sha = hashlib.sha1()
    try:
        f = open(filename,'rb')
        data = f.read()
        sha.update(data)
        return sha.hexdigest()
    except:
        pass


#------------------------------------------------------------------------------
def fail(msg):
    print "Failed: %s" % msg
    sys.exit(1)

#------------------------------------------------------------------------------
# The purpose of this is the recreate the zip with zigbert.rsa as
#  the first file in the zip. Firefox 3 requires this.
# https://developer.mozilla.org/en/Signing_a_XPI#Prepare_XPI_file_for_signing

def callback(filelist,dirname,files):
    for f in files:
        filelist.append(os.path.join(dirname,f))

def getfiles(dir):
    filelist = []
    os.path.walk(dir,callback,filelist)
    return filelist

#------------------------------------------------------------------------------
# Check to make sure there are two xpis in the zip file
def check_zip(z):
    xpis_list = z.namelist()
    if len(xpis_list) != 2:
        fail("There are %d files in the zip file" % len(xpis_list))

#------------------------------------------------------------------------------
# Pass in the rdf file to be signed
def sign_update_rdfs(rdf):

    if not os.path.isfile(MCCOY_EXE):
        print "ERROR: Could not sign %s " % rdf
        print "     McCoy path is invalid: %s" % MCCOY_EXE
        return

    print "Signing %s..." % rdf
    # Passing -xpi just generates and adds the sha1 hash to the file
    # The hash is is already generated in create_update_rdfs.py
    #cmd = "%s -command update -updateRDF $SCRIPTDIR/$1 -key moonlight" % mccoy_exe
    curdir = os.path.dirname(os.path.realpath(__file__))
    fullRdfPath = os.path.join(curdir,rdf)  # mccoy cli requires full path to rdf file
    cmd = "%s -command update -key moonlight -updateRDF %s" % (MCCOY_EXE,fullRdfPath)

    executeCmd(cmd)


#------------------------------------------------------------------------------
# MAIN function

def prepare_xpi(xpifilename):

    new_version = MoonlightReleases.new_version

    if xpifilename == 'clean':
        clean()
        return

    if not os.path.exists(xpifilename):
        fail("Cannot find file %s" % xpifilename)

    # copy xpi to tmp dir, create update.rdf
    tmpdir = tempfile.mkdtemp(dir='.')
    shutil.copy(xpifilename,tmpdir)
    os.chdir(tmpdir)

    arch = None
    if xpifilename.find('x86_64') >= 0:
        arch = 'x86_64'
    else:
        arch = 'i586'

    #./create_update_rdfs.py -p 2.0 -a i586,x86_64 -n $NEW_VERSION -o $OLD_VERSIONS
    create_update_rdfs.create_rdfs(new_version,MoonlightReleases.old_versions,'2.0',[arch])
    create_update_rdfs.create_rdfs(new_version,MoonlightReleases.old_1_0_versions,'1.0',[arch])

    for rdf in glob.glob("update*.rdf"):
        sign_update_rdfs(rdf)



    #mkdir $NEW_VERSION
    new_dir = os.path.join('..',new_version)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    #mv update*.rdf novell-moonlight*.xpi sha1sums-* info*xhtml $NEW_VERSION
    filelist = glob.glob('update*rdf')
    filelist.extend(glob.glob('novell-moonlight*xpi'))
    filelist.extend(glob.glob('info*.xhtml'))

    shafile = open(os.path.join(new_dir,'sha1sums-%s' % new_version),'a')
    for f in filelist:
        if (f[-4:] in ['.xpi','.rdf']): # Only add .xpi and .rdf to the checksum file
            shafile.write("%s  %s\n" % (get_sha1sum(f),f)) # Two spaces are required between sum and filename
        os.rename(f,os.path.join(new_dir,f))
    shafile.close()

    os.chdir('..') # not cross platform, but whatever
    shutil.rmtree(tmpdir,ignore_errors=True)

    print "Next step:"
    print "  - Review the contents of the %s directory" % new_version


if __name__ == '__main__':
    if len(sys.argv) < 2:
        fail("Usage: %s <moonlight.xpi>" % sys.argv[0])

    xpifilename = sys.argv[1]
    prepare_xpi(xpifilename)

# vim:ts=4:expandtab:
