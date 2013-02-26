#!/bin/sh

VERSION="3.0.7"
BUILD="0"
CHECKOUT_ROOT="/sources/mono"
INSTALL_ROOT="/tmp/install"
PACKAGE_DEST="/release/packaging/zip_packages/win-4-i386/mono/$VERSION"
MONO_ZIP="$PACKAGE_DEST/mono-$VERSION-$BUILD.xamarin.x86.zip"
PACKAGE_OUTPUT="/release/windows-installer/Output/$VERSION/"


function error
{
    echo "$(date "+%F@%T") :: $1" 1>&2
    exit 1
}

function report
{
    echo "$(date "+%F@%T") :: $1"
}

function cleanup
{
    report "Cleaning up"

    rm $MONO_ZIP
    rm -rf $INSTALL_ROOT
    rm -rf $PACKAGE_OUTPUT

    (cd $CHECKOUT_ROOT; make clean)
}

function download
{
    report "Downloading Mono"

    if [ -d $CHECKOUT_ROOT ] ; then
        (cd $CHECKOUT_ROOT; git pull origin master; git reset --hard $BUILD_REVISION) || error "Cannot update mono"
    else
        git clone git://github.com/mono/mono.git $CHECKOUT_ROOT || error "Cannot checkout mono"
    fi

    if [ -d $CHECKOUT_ROOT ] ; then
        (cd $CHECKOUT_ROOT; git submodule update --init) || error "Cannot update git submodules"
    fi
}

function build
{
    report "Building Mono"

    pushd $CHECKOUT_ROOT
    ./autogen.sh --prefix=$INSTALL_ROOT || error "Cannot autogen.sh"
    make || error "Cannot make"
    make install || error "Cannot make install"
    popd
}


function package
{
    report "Zipping Mono"
    mkdir -p $PACKAGE_DEST
    (cd $INSTALL_ROOT; zip -r $MONO_ZIP .) || error "Cannot zip"
}


function run
{
    cleanup
    download
    build
    package
    report "Done"
}

run
