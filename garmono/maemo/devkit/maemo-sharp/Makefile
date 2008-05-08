GARNAME    = maemo-sharp
CATEGORIES = maemo/devkit
GARVERSION = $(MAEMOSHARP_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DEPENDS  = maemo/devkit/mono
DEPENDS += maemo/devkit/gtk-sharp

DESCRIPTION = Maemo# is a Gtk# bindings for Maemo libraries.
define BLURB
 This is Maemo# is a Gtk# bindings for Maemo libraries intented to run on 
 Scratchbox devkit.
endef

GARMONO_DESTDIR   = $(SBOX_PREFIX)

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS    = $(DIRPATHS)

include ../../../gar.mk

