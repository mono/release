GARNAME = mono
GARVERSION = $(MONO_VERSION)
CATEGORIES = mono-devkit
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2

PATCHFILES =

LIBDEPS = devkit/glib
DEPENDS = 

DESCRIPTION = $(GARNAME)

DEBIAN_PACKAGES = mono mono-dev

define BLURB
 # FIXME: blurb goes here
endef

CONFIGURE_ARGS = --prefix=$(prefix)
BUILD_ARGS = 

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = $(WORKSRC)/Makefile

include ../category.mk

post-install:
	strip -s $(prefix)/bin/mono
	strip -s $(prefix)/bin/monodis
	strip -s $(prefix)/bin/monodiet
	strip -s $(prefix)/bin/monograph
	strip -s $(prefix)/bin/pedump
	strip -s $(prefix)/lib/libMonoPosixHelper.so

	
