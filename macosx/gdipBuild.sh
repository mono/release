#!/bin/sh -x

DEPS=/Users/Shared/MonoBuild/Dependancies
MONORELEASE=/Users/Shared/mono/release/macosx
PATCHDIR=${MONORELEASE}/libgdiplus/jpeg/files
NAME=jpeg
VERSION=6b 
DISTNAME=${NAME}src.v${VERSION}.tar.gz
URL=ftp://ftp.uu.net/graphics/jpeg/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

CFLAGS="-I/Library/Frameworks/Mono.framework/Versions/Current/include/ -L/Library/Frameworks/Mono.framework/Versions/Current/lib/" 
export PATH=/usr/X11R6/bin/:/Library/Frameworks/Mono.framework/Versions/Current/bin:$PATH 
export PKG_CONFIG_PATH=/usr/X11R6/lib/pkgconfig/:$PKG_CONFIG_PATH
export ACLOCAL_FLAGS="-I /Library/Frameworks/Mono.framework/Versions/1.1.4/share/aclocal/"
#./autogen.sh 
#--prefix=/Library/Frameworks/Mono.framework/Versions/1.1.3/

#################################################
cd ${DEPS}    
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L -Z 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}
    patch config.guess ${PATCHDIR}/patch-config.guess
    patch config.sub ${PATCHDIR}/patch-config.sub
    patch ltmain.sh ${PATCHDIR}/patch-ltmain.sh
    patch ltconfig ${PATCHDIR}/patch-ltconfig

    sed -e 's/(prefix)\/man/(prefix)\/share\/man/g' makefile.cfg > makefile.cfg.patched
    mv makefile.cfg.patched makefile.cfg

    ./configure --enable-shared --enable-static --prefix=${MONOPREFIX}
    make
make install
fi

################################
PATCHDIR=${MONORELEASE}/libgdiplus/tiff/files
NAME=tiff
VERSION=3.7.1
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=ftp://ftp.freebsd.org/pub/FreeBSD/ports/distfiles/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L -Z 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}

    ./configure --mandir=${MONOPREFIX}/share/man \
	--with-jpeg-include-dir=${MONOPREFIX}/include \
	--with-jpeg-lib-dir=${MONOPREFIX}/lib
    make 
    make install
fi

###############################################
#PATCHDIR=${MONORELEASE}/libgdiplus/tiff/files
NAME=libpng
VERSION=1.2.8
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://umn.dl.sourceforge.net/sourceforge/libpng/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current
cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L -Z 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}

    cp scripts/makefile.darwin Makefile
    ./configure --prefix=${MONOPREFIX}
    #sed -e 's/(prefix)\/man/(prefix)\/share\/man/g' makefile.cfg > makefile.cfg.patched
    #mv makefile.cfg.patched makefile.cfg

    make
    make install
fi


###############################################
#PATCHDIR=${MONORELEASE}/libgdiplus/tiff/files
NAME=libungif
VERSION=4.1.3
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://umn.dl.sourceforge.net/sourceforge/libungif/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current                                       
cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L -Z 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}

    ./configure --prefix=${MONOPREFIX}
    make
    make install
fi

###############################################
NAME=libgdiplus
VERSION=1.1.4
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://www.go-mono.com/archive/1.1.4/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}
#MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/Current

cd ${DEPS}
if [ ! -e ${DEPS}/${WORKSRCDIR} ];then
    curl -L -Z 5 -s -O ${URL}
    gnutar -xzf ${DISTNAME}
    cd ${WORKSRCDIR}
    ./configure --prefix=${MONOPREFIX}
    make
    make install
fi

#http://www.go-mono.com/archive/1.1.4/libgdiplus-1.1.4.tar.gz