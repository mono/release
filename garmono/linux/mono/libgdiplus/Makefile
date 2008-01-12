GARNAME    = libgdiplus
CATEGORIES = linux/mono
GARVERSION = $(LIBGDI_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DESCRIPTION = Libgdiplus
define BLURB
 Libgdiplus is the Mono library that provide a GDI+ comptible API on non-Windows
 operating systems.
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS) --with-cairo=system

# This should go before any hand-made rules.
include ../../../gar.mk

