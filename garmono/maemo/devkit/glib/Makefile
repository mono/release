GARNAME = glib
CATEGORIES = maemo/devkit
GARVERSION = 2.12.12
DISTFILES = $(GARNAME)-$(GARVERSION).tar.bz2
MASTER_SITES = ftp://ftp.gtk.org/pub/glib/2.12/

DESCRIPTION = $(GARNAME)

DESCRIPTION = GLib low-level core library
define BLURB
 GLib is the low-level core library that forms the basis of GTK+ and GNOME. It
 provides data structure handling for C, portability wrappers, and interfaces
 for such runtime functionality as an event loop, threads, dynamic loading, and
 an object system.
endef

GARMONO_DESTDIR = $(SBOX_PREFIX)

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = glib

CONFIGURE_ARGS = $(DIRPATHS)

include ../../../gar.mk

install-glib:
	install -d -m 755 $(prefix)/lib/glib
	install -m 755 $(WORKSRC)/glib/.libs/libglib-2.0.so.0.1200.12 $(DESTDIR)$(prefix)/lib/glib/libglib-2.0.so.0
	install -m 755 $(WORKSRC)/gmodule/.libs/libgmodule-2.0.so.0.1200.12 $(DESTDIR)$(prefix)/lib/glib/libgmodule-2.0.so.0
	install -m 755 $(WORKSRC)/gobject/.libs/libgobject-2.0.so.0.1200.12 $(DESTDIR)$(prefix)/lib/glib/libgobject-2.0.so.0
	install -m 755 $(WORKSRC)/gthread/.libs/libgthread-2.0.so.0.1200.12 $(DESTDIR)$(prefix)/lib/glib/libgthread-2.0.so.0
	$(MAKECOOKIE)

post-install:	
	strip $(DESTDIR)$(prefix)/lib/glib/libglib-2.0.so.0
	strip $(DESTDIR)$(prefix)/lib/glib/libgmodule-2.0.so.0
	strip $(DESTDIR)$(prefix)/lib/glib/libgobject-2.0.so.0
	strip $(DESTDIR)$(prefix)/lib/glib/libgthread-2.0.so.0
	$(MAKECOOKIE)

