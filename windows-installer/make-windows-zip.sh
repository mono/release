#!/bin/sh

VERSION="2.11"
BUILD="0"
CHECKOUT_ROOT="$HOME/git/mono"
INSTALL_ROOT="/tmp/install"
PACKAGE_DEST="/release/packaging/zip_packages/win-4-i386/mono/2.11/"

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

function clean_install_root
{
    rm -rf $INSTALL_ROOT
}

function download_mono
{
    if [ -d $CHECKOUT_ROOT ] ; then
        cd $CHECKOUT_ROOT; git pull || error_exit "Cannot update mono"
    else
        git clone git@github.com:mono/mono $CHECKOUT_ROOT || error_exit "Cannot checkout mono"
    fi
}


function build_mono
{
    cd $CHECKOUT_ROOT
    ./autogen.sh --prefix=$INSTALL_ROOT || error_exit "Cannot autogen.sh"
    make || error_exit "Cannot make"
    make install || error_exit "Cannot make install"
}


function package_mono
{
    cd $INSTALL_ROOT
    zip -r $PACKAGE_DEST/mono-$VERSION-$BUILD.xamarin.x86.zip . || error_exit "Cannot zip"
}


function run
{
    clean_install_root
    download_mono
    build_mono
    package_mono
}

run
