GARNAME      = make
CATEGORIES   = cygwin/deps
GARVERSION   = 3.80-1
DISTFILES    = $(GARNAME)-$(GARVERSION).tar.bz2
MASTER_SITES = http://www.go-mono.com/archive/helper/

DESCRIPTION = GNU make utility to maintain groups of programs
define BLURB
 The  purpose of the make utility is to determine automatically which pieces of
 a large program need to be recompiled, and issue the commands to recompile them.
endef

INSTALL_SCRIPTS = make

# This should go before any hand-made rules.
include ../../../gar.mk

install-make:
	install -d $(DESTDIR)$(bindir)
	-install -m 755 $(WORKDIR)/usr/bin/make.exe $(DESTDIR)$(bindir)/make.exe
	$(MAKECOOKIE)

