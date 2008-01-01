GARNAME      = zlib
GARVERSION   = 1.2.3
CATEGORIES   = deps/cygwin
DISTFILES    = $(GARNAME)-$(GARVERSION)-bin.zip
DISTFILES   += $(GARNAME)-$(GARVERSION)-lib.zip
MASTER_SITES = http://internap.dl.sourceforge.net/sourceforge/gnuwin32/

DESCRIPTION = Compression/decompression library
define BLURB
  The zlib library is a general purpose data compression library.
endef

INSTALL_SCRIPTS = zlib

# This should go before any hand-made rules.
GARDIR ?= ../../..
include ../../../gar.mk

install-zlib:
	# bin
	install -d $(DESTDIR)$(bindir)
	install -m 644 $(WORKDIR)/bin/zlib1.dll $(DESTDIR)$(bindir)/zlib1.dll
	# include
	install -d $(DESTDIR)$(includedir)
	install -m 644 $(WORKDIR)/include/zconf.h $(DESTDIR)$(includedir)/zconf.h
	install -m 644 $(WORKDIR)/include/zlib.h $(DESTDIR)$(includedir)/zlib.h
	#lib
	install -d $(DESTDIR)$(libdir)
	install -m 644 $(WORKDIR)/lib/libz.a $(DESTDIR)$(libdir)/libz.a
	install -m 644 $(WORKDIR)/lib/libz.dll.a $(DESTDIR)$(libdir)/libz.dll.a
	install -m 644 $(WORKDIR)/lib/zlib-bcc.lib $(DESTDIR)$(libdir)/zlib-bcc.lib
	install -m 644 $(WORKDIR)/lib/zlib.def $(DESTDIR)$(libdir)/zlib.def
	install -m 644 $(WORKDIR)/lib/zlib.lib $(DESTDIR)$(libdir)/zlib.lib
	$(MAKECOOKIE)

