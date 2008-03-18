GARNAME    = gtk-sharp
CATEGORIES = maemo/debs
GARVERSION = $(GTKSHARP_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

#DEPENDS = maemo/devkit/mono

DESCRIPTION = Gtk-Sharp2, a GUI Toolkit
define BLURB
 Gtk-Sharp2, a GUI Toolkit, is a set of .NET bindings for the gtk+ toolkit and 
 assorted GNOME libraries.
endef

ifeq ($(shell arch), arm)
DPKG_PARAMS = -tc -B
else
DPKG_PARAMS = -tc
endif

CONFIGURE_SCRIPTS = deb
BUILD_SCRIPTS     = deb
INSTALL_SCRIPTS   = deb

include ../../../gar.mk

configure-deb:
	ln -sf $(CURDIR)/files/debian $(WORKSRC)/debian
	$(MAKECOOKIE)

build-deb:
	@cd $(WORKSRC) && dpkg-buildpackage -rfakeroot $(DPKG_PARAMS)
	$(MAKECOOKIE)

install-deb:
	@cd $(WORKSRC)
	install -d $(GARMONO_DEBSDIR)
	mv $(WORKSRC)/../*.deb $(GARMONO_DEBSDIR)
ifneq ($(shell arch), arm)
	mv $(WORKSRC)/../*.tar.gz $(GARMONO_DEBSDIR)
endif
	$(MAKECOOKIE)

