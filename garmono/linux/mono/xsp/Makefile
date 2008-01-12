GARNAME    = xsp
CATEGORIES = linux/mono
GARVERSION = $(XSP_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DEPENDS  = linux/mono/mono

DESCRIPTION = XSP
define BLURB
 XSP is a standalone web server written in C# that can be used to run your 
 ASP.NET applications with minimal effort. XSP works under both the Mono and 
 Microsoft runtimes.
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS)

# This should go before any hand-made rules.
include ../../../gar.mk

