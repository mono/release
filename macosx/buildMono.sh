#!/bin/sh -x

# this horrid little script updates a mono revision
# Author: Andy Satori <dru@satori-assoc.com>
# Modifications: kangaroo
# Changes June 10/2004
#  - Updated for beta3 0.96
# Changes June 2/2004
#  - Updated for beta2 0.95
#  - Updated to boehm.gc.a6
#  - Updated to glib-2.4.1

set -e 

INITIALDIR=$1
VERSION=$2
PREFIX=$INITIALDIR/PKGROOT/Library/Frameworks/Mono.framework/Versions/$VERSION
MONOURL="http://www.go-mono.com/archive/rc/mono-$VERSION.tar.gz"
#http://www.go-mono.com/archive/rc/mono-/usr/local/mono.build.tar.gz -O

echo $MONOURL

export C_INCLUDE_PATH=$C_INCLUDE_PATH:$PREFIX/include
export LDFLAGS=-L$PREFIX/lib
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/X11R6/lib:$PREFIX/lib

if test ! -d "$INITIALDIR/Dependancies"; then
    mkdir $INITIALDIR/Dependancies
fi

# make the directories as need for the Framework (which isn't really 
# a framework, but it looks like one and makes a nice placeholder until 
# someone smarter than I am can come in and make it better)

if test ! -d "/Library/Frameworks/Mono.framework"; then
    mkdir -p /Library/Frameworks/Mono.framework/Versions
fi

if test ! -d "/Library/Frameworks/Mono.framework/Versions/$VERSION"; then
    mkdir /Library/Frameworks/Mono.framework/Versions/$VERSION
fi

if test ! -d "$INITIALDIR/PKGROOT"; then
	mkdir $INITIALDIR/PKGROOT
fi

# set up the environment for the build
export PATH=$PATH:$PREFIX/bin:/usr/X11R6/bin
echo "The new path is ${PATH}"
export ACLOCAL_FLAGS="-I $PREFIX/share/aclocal/"
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/X11R6/lib/pkgconfig


cd $INITIALDIR/Dependancies

# pkg-config

if test ! -f "$PREFIX/bin/pkg-config"; then
    if test ! -d "pkgconfig-0.15.0"; then
		echo "Downloading pkg-config"
		curl -s http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-0.15.0.tar.gz -O
		tar xzf pkgconfig-0.15.0.tar.gz
		rm pkgconfig-0.15.0.tar.gz
	fi
    
    cd pkgconfig-0.15.0
	echo "Building pkg-config"
    
    ./configure -quiet --prefix=$PREFIX
    make
    make install
    make clean
    
    cd ..
fi

# gettext

echo +++ processing gettext

if test ! -f "$PREFIX/bin/gettext"; then

    if test ! -d "gettext-0.14.1"; then
		echo "Downloading gettext"
		curl -s http://ftp.gnu.org/pub/gnu/gettext/gettext-0.14.1.tar.gz -O
		tar xzf gettext-0.14.1.tar.gz
		rm gettext-0.14.1.tar.gz
	fi
    
    cd gettext-0.14.1
    
	echo "Building gettext"
    ./configure -quiet --prefix=$PREFIX
    make
    make install
    make clean
    
    cd ..
fi

# glib2

echo +++ processing glib2

if test ! -f "$PREFIX/lib/libgobject-2.0.la"; then
    if test ! -d "glib-2.4.1"; then
		echo "Downloading libgobject"
		curl -s ftp://ftp.gtk.org/pub/gtk/v2.4/glib-2.4.1.tar.gz -O
		tar xzf glib-2.4.1.tar.gz
		rm glib-2.4.1.tar.gz
	fi
    
    cd glib-2.4.1
    
	echo "Building libgobject"
    ./configure -quiet --prefix=$PREFIX 
    make
    make install
    make clean
    
    cd ..
fi

# boehm gc, is now built-in (since 0.95)

# icu ( http://oss.software.ibm.com/icu/index.html )


if test ! -f "$PREFIX/lib/libicuuc.dylib.28.0"; then
    if test ! -d "icu"; then
		echo "Downloading icu"
		curl -s ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz -O --disable-epsv
		tar xzf icu-2.8.tgz
		rm icu-2.8.tgz
    fi
    
    cd icu/source
	echo "Building icu"
    
    ./runConfigureICU MacOSX --with-data-packaging=library --prefix=$PREFIX --libdir=$PREFIX/lib/ 
    gnumake
    make install
    make clean
    
    cd $PREFIX/lib
    
    # libicudata
    install_name_tool -id $PREFIX/lib/libicudata.dylib.28 libicudata.dylib.28.0
    
    # libicui18n
    install_name_tool -id $PREFIX/lib/libicui18n.dylib.28 libicui18n.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicui18n.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicui18n.dylib.28.0
    
    # libicuio
    install_name_tool -id $PREFIX/lib/libicuio.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicui18n.dylib.28 $PREFIX/lib/libicui18n.dylib.28 libicuio.dylib.28.0
    
    # libicule
    install_name_tool -id $PREFIX/lib/libicule.dylib.28 libicule.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicule.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicule.dylib.28.0

    # libiculx
    install_name_tool -id $PREFIX/lib/libiculx.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicule.dylib.28 $PREFIX/lib/libicule.dylib.28 libiculx.dylib.28.0

    # libicutoolutil
    install_name_tool -id $PREFIX/lib/libicutoolutil.dylib.28 libicutoolutil.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicutoolutil.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicutoolutil.dylib.28.0

    # libicuuc
    install_name_tool -id $PREFIX/lib/libicuuc.dylib.28 libicuuc.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicuuc.dylib.28.0
    
    cd $INITIALDIR
fi

# mono

echo "patching libintl to not be statically linked"
perl -pi -e "s/old_library='libintl.a'/old_library=''/" $PREFIX/lib/libintl.la
echo "processing mono run-time libraries"

if test ! -f "$PREFIX/bin/mono"; then
    if test ! -d "$INITIALDIR/Bootstrap"; then
		mkdir $INITIALDIR/Bootstrap
	fi

    echo "Downloading Mono $VERSION"
    cd $INITIALDIR/Bootstrap    
    if test ! -d "mono-$VERSION"; then
		curl -s -O $MONOURL
		tar xzf mono-$VERSION.tar.gz
		rm mono-$VERSION.tar.gz
	fi
    
    cd mono-$VERSION
    
	echo "Building Mono $VERSION"
    ./configure -quiet --prefix=$PREFIX
    make
    make install
    make clean
    
    cd ..
fi

# setup the Current symlink

cd /Library/Frameworks/Mono.framework/Versions

if test -e "/Library/Frameworks/Mono.framework/Versions/Current"; then
    rm Current
fi

ln -s $VERSION Current
echo +++ Setup the rest of the framework
cd /Library/Frameworks/Mono.framework
ln -s Versions/Current/lib Libraries
ln -s Versions/Current/include Headers
ln -s Versions/Current/bin Commands
