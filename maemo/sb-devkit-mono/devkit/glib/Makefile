GARNAME = glib
GARVERSION = $(GLIB_VERSION)
CATEGORIES = mono-devkit
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2

PATCHFILES =

LIBDEPS =
DEPENDS = 

DESCRIPTION = $(GARNAME)

DEBIAN_PACKAGES = 

define BLURB
 # FIXME: blurb goes here
endef

CONFIGURE_ARGS = --prefix=$(prefix)
BUILD_ARGS = 

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = glib

include ../category.mk

install-glib:
	install -d -m 755 $(prefix)/lib/glib
	install -m 755 $(WORKSRC)/glib/.libs/libglib-2.0.so.0.800.6 $(prefix)/lib/glib/libglib-2.0.so.0
	install -m 755 $(WORKSRC)/gmodule/.libs/libgmodule-2.0.so.0.800.6 $(prefix)/lib/glib/libgmodule-2.0.so.0
	install -m 755 $(WORKSRC)/gobject/.libs/libgobject-2.0.so.0.800.6 $(prefix)/lib/glib/libgobject-2.0.so.0
	install -m 755 $(WORKSRC)/gthread/.libs/libgthread-2.0.so.0.800.6 $(prefix)/lib/glib/libgthread-2.0.so.0
	$(MAKECOOKIE)

post-install:	
	strip $(prefix)/lib/libglib-2.0.so.0
	strip $(prefix)/lib/libgmodule-2.0.so.0
	strip $(prefix)/lib/libgobject-2.0.so.0
	strip $(prefix)/lib/libgthread-2.0.so.0
