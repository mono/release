GARNAME    = mod_mono
CATEGORIES = linux/mono
GARVERSION = $(MODMONO_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DEPENDS  = linux/mono/mono
DEPENDS += linux/mono/xsp

DESCRIPTION = Mod Mono
define BLURB
 Mod_Mono is an Apache 1.3/2.0/2.2 module that provides ASP.NET support for the
 web's favorite server, Apache (http://httpd.apache.org).
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/configure
BUILD_SCRIPTS     = $(WORKSRC)/Makefile
INSTALL_SCRIPTS   = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS)

# This should go before any hand-made rules.
include ../../../gar.mk

# NOTES:
# mod_mono can be build only with root privilegies.
