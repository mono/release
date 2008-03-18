GARNAME    = gtk-sharp
CATEGORIES = maemo/devkit
GARVERSION = $(GTKSHARP_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DEPENDS = maemo/devkit/mono

DESCRIPTION = Gtk-Sharp, a GUI Toolkit
define BLURB
 Gtk-Sharp, a GUI Toolkit, is a set of .NET bindings for the gtk+ toolkit and 
 assorted GNOME libraries.
endef

GARMONO_DESTDIR   = $(SBOX_PREFIX)

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS    = $(DIRPATHS)

include ../../../gar.mk

