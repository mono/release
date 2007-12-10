GARNAME = glib
GARVERSION = $(GLIB_VERSION)
CATEGORIES = mono-devkit
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2
DESCRIPTION = $(GARNAME)

PATCHFILES =

LIBDEPS = devkit/pkg-config
DEPENDS = 

DEBIAN_PACKAGES = 

CONFIGURE_ARGS = --prefix=$(prefix)
BUILD_ARGS = 

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = $(WORKSRC)/Makefile

include ../category.mk

post-install:	
	strip $(prefix)/lib/*.so

