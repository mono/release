GARNAME = pkg-config
GARVERSION = $(PKGCONFIG_VERSION)
CATEGORIES = mono-devkit
DISTFILES = $(GARNAME)-$(GARVERSION).tar.gz
DESCRIPTION = $(GARNAME)

PATCHFILES =

LIBDEPS =
DEPENDS = 

DEBIAN_PACKAGES = 

CONFIGURE_ARGS = --prefix=$(prefix)
BUILD_ARGS = 

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = glib

include ../category.mk

install-glib:
	install -d -m 755 $(prefix)/bin
	install -m 755 $(WORKSRC)/pkg-config $(prefix)/bin/pkg-config
	$(MAKECOOKIE)

post-install:	
	strip $(prefix)/bin/pkg-config

