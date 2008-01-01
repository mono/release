GARNAME      = pkgconfig
GARVERSION   = 0.15
CATEGORIES   = deps/cygwin
DISTFILES    = $(GARNAME)-$(GARVERSION).zip
MASTER_SITES = http://www.gimp.org/~tml/gimp/win32/

DEPENDS += deps/cygwin/glib

DESCRIPTION = The pkg-config returns metainformation about installed libraries
define BLURB
 The pkg-config program is used to retrieve information about installed 
 libraries in the system.  It is typically used to compile and link against one
 or more libraries.
endef

INSTALL_SCRIPTS = pkgconfig

# This should go before any hand-made rules.
GARDIR ?= ../../..
include ../../../gar.mk

install-pkgconfig:
	install -d $(DESTDIR)$(bindir)
	install -m 755 $(WORKDIR)/bin/pkg-config.exe $(DESTDIR)$(bindir)/pkg-config.exe
	$(MAKECOOKIE)

