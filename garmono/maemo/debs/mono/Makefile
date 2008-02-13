GARNAME    = mono
CATEGORIES = maemo/debs
GARVERSION = $(MONO_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

DESCRIPTION = Mono deb packages for Maemo platform
define BLURB
 Mono provides the necessary software to develop and run .NET client and server
 applications on Linux, Solaris, Mac OS X, Windows, and Unix.
endef

ifeq ($(shell arch), arm)
DPKG_PARAMS = -B
else
DPKG_PARAMS = 
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
	mv $(WORKSRC)/../*.tar.gz $(GARMONO_DEBSDIR)
	$(MAKECOOKIE)

