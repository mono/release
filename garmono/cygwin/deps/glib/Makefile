GARNAME    = glib
CATEGORIES = cygwin/deps
GARVERSION = 2.12.4

DISTFILES  = $(GARNAME)-$(GARVERSION).zip
DISTFILES += $(GARNAME)-dev-$(GARVERSION).zip
DISTFILES += gettext-0.14.5.zip
DISTFILES += gettext-dev-0.14.5.zip
DISTFILES += libiconv-1.9.1.bin.woe32.zip

MASTER_SITES  = http://ftp.gtk.org/pub/glib/2.12/win32/ 
MASTER_SITES += http://ftp.gtk.org/pub/glib/2.12/win32/dependencies/

DESCRIPTION = GLib low-level core library
define BLURB
 GLib is the low-level core library that forms the basis of GTK+ and GNOME. It
 provides data structure handling for C, portability wrappers, and interfaces
 for such runtime functionality as an event loop, threads, dynamic loading, and
 an object system.
endef

INSTALL_SCRIPTS = deps

# This should go before any hand-made rules.
include ../../../gar.mk

install-deps:
	install -d $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/bin $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/include $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/lib $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/make $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/man $(DESTDIR)$(prefix)
	cp -rf $(WORKDIR)/share $(DESTDIR)$(prefix)
	# Don't know why but it fixes cygwin library copies, looks like cp handle
	# something incorrect, using install all works fine.
	install $(WORKDIR)/bin/*.dll $(DESTDIR)$(bindir)
	$(MAKECOOKIE)

