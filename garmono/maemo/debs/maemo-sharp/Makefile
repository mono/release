GARNAME    = maemo-sharp
CATEGORIES = maemo/debs
GARVERSION = $(MAEMOSHARP_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DESCRIPTION = Mono bindings for Maemo
define BLURB
 This package provides assemblies that allow CLI (.NET) programs to use the
 Maemo and Hildon libraries.
endef

BUILD_SCRIPTS     = deb
INSTALL_SCRIPTS   = deb

include ../../../gar.mk

build-deb:
	@cd $(WORKSRC) && dpkg-buildpackage -rfakeroot $(DPKG_PARAMS)
	$(MAKECOOKIE)

install-deb:
	@cd $(WORKSRC)
	install -d $(GARMONO_DEBSDIR)
	mv $(WORKSRC)/../*.deb $(GARMONO_DEBSDIR)
	mv $(WORKSRC)/../*.tar.gz $(GARMONO_DEBSDIR)
	$(MAKECOOKIE)

