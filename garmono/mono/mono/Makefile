GARNAME    = mono
GARVERSION = 1.2.6
CATEGORIES = mono
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DESCRIPTION = Mono
define BLURB
 Mono provides the necessary software to develop and run .NET client and server
 applications on Linux, Solaris, Mac OS X, Windows, and Unix.
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS)

# This should go before any hand-made rules.
include ../../gar.mk

