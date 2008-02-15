GARNAME    = mono
CATEGORIES = maemo/devkit
GARVERSION = $(MONO_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

LIBDEPS = maemo/devkit/glib

DESCRIPTION = Mono
define BLURB
 Mono provides the necessary software to develop and run .NET client and server
 applications on Linux, Solaris, Mac OS X, Windows, and Unix.
endef

GARMONO_DESTDIR   = $(SBOX_PREFIX)

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS    = $(DIRPATHS) --with-moonlight=no --with-static_mono=yes --with-ikvm-native=no

include ../../../gar.mk

post-configure:
	# HAVE_SCHED_SETAFFINITY can cause problem on devkit compilation
	sed -e 's,#define HAVE_SCHED_SETAFFINITY 1,/*#define HAVE_SCHED_SETAFFINITY 1*/,' -i $(WORKSRC)/config.h
	$(MAKECOOKIE)

