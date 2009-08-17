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

import MoonlightReleases
import create_update_rdfs

#------------------------------------------------------------------------------
def executeCmd(command, stderr=open(os.devnull)):
    ret = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=stderr)
    output = ret.communicate()[0]
    lines = output.split('\n')
    return lines


#------------------------------------------------------------------------------
def clean():
    # Delete any old generated files
    files = glob.glob("novell*xpi")
    #pdb.set_trace()
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

def reorder_xpi(xpiname):
    shutil.rmtree('tmp',ignore_errors=True)
    xpi = zipfile.ZipFile(xpiname,mode='r',compression=zipfile.ZIP_DEFLATED)
    xpi.extractall('tmp')
    os.chdir('tmp')

    newxpi = zipfile.ZipFile(xpiname,'w')

    newxpi.write(os.path.join('META-INF','zigbert.rsa'))
    newxpi.write(os.path.join('META-INF','zigbert.sf'))
    newxpi.write(os.path.join('META-INF','manifest.mf'))

    newxpi.write('chrome.manifest')
    newxpi.write('install.rdf')

    files = getfiles('plugins')
    files.extend(getfiles('skin'))
    for f in files:
        if not os.path.isdir(f):
            newxpi.write(f)

    #cd ..
    os.chdir('..')

    #rm $1 # Delete the original xpi
    os.remove(xpiname)
    #mv tmp/$1 .
    os.rename(os.path.join('tmp',xpiname),xpiname)

    #rm -rf tmp
    shutil.rmtree('tmp',ignore_errors=True)

#------------------------------------------------------------------------------
# Check to make sure there are two xpis in the zip file
def check_zip(z):
    xpis_list = z.namelist()
    if len(xpis_list) != 2:
        fail("There are %d files in the zip file" % len(xpis_list))

#------------------------------------------------------------------------------
# Pass in the rdf file to be signed
def sign_update_rdfs(rdf):

    mccoy_exe="/home/rhowell/code/moonlight-ms/moz_ext_update/mccoy/mccoy"

    # Passing -xpi just generates and adds the sha1 hash to the file
    # The hash is is already generated in create_update_rdfs.py
    #cmd = "%s -command update -updateRDF $SCRIPTDIR/$1 -key moonlight" % mccoy_exe
    curdir = os.path.dirname(os.path.realpath(__file__))
    rdf = os.path.join(curdir,rdf)
    cmd = "%s -command update -updateRDF %s -key moonlight" % (mccoy_exe,rdf)

    executeCmd(cmd)


#------------------------------------------------------------------------------
# MAIN function

def main():

    if len(sys.argv) < 2:
        fail("Usage: %s <moonlight_signed.zip" % sys.argv[0])

    zipfilename = sys.argv[1]
    new_version = MoonlightReleases.new_version

    if zipfilename == 'clean':
        clean()
        return

    if not os.path.exists(zipfilename):
        fail("Cannot find file %s" % zipfilename)

    clean()

    z = zipfile.ZipFile(zipfilename,'r')
    xpi_list = z.namelist()

    shafile = open('sha1sums-%s' % new_version,'w')

    for xpi in xpi_list:
        print "Reordering %s" % xpi
        z.extract(xpi)
        reorder_xpi(xpi)
        shafile.write("%s  %s\n" % (get_sha1sum(xpi),xpi)) # Two spaces are required between sum and filename
    shafile.close()

    #NEW_VERSION=$PREVIEW

    #./create_update_rdfs.py -p 2.0 -a i586,x86_64 -n $NEW_VERSION -o $OLD_VERSIONS
    create_update_rdfs.create_rdfs(new_version,MoonlightReleases.old_versions)

    for rdf in glob.glob("update*.rdf"):
        print "Signing %s..." % rdf
        sign_update_rdfs(rdf)


    #mkdir $NEW_VERSION
    os.mkdir(new_version)
    #mv update*.rdf novell-moonlight*.xpi sha1sums-* info*xhtml $NEW_VERSION
    filelist = glob.glob('update*rdf')
    filelist.extend(glob.glob('novell-moonlight*xpi'))
    filelist.extend(glob.glob('sha1sums-*'))
    filelist.extend(glob.glob('info*.xhtml'))

    for f in filelist:
        os.rename(f,os.path.join(new_version,f))


    print "Next step:"
    print "  - Review the contents of the %s directory" % new_version
    print "  - Run publish_preview.sh"


if __name__ == '__main__':
    main()
