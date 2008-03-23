GARNAME    = libgdiplus
CATEGORIES = maemo/debs
GARVERSION = $(LIBGDI_VERSION)
DISTFILES  = $(GARNAME)-$(GARVERSION).tar.bz2

#DEPENDS = maemo/devkit/mono

DESCRIPTION = Libgiplus
define BLURB
 Libgdiplus is a native library object needed by Mono WinForms implementation.
endef

CONFIGURE_SCRIPTS = deb
BUILD_SCRIPTS     = deb
INSTALL_SCRIPTS   = deb

include ../../../gar.mk

configure-deb:
	ln -sf $(CURDIR)/files/debian $(WORKSRC)/debian
	$(MAKECOOKIE)

build-deb:
	@cd $(WORKSRC) && dpkg-buildpackage -rfakeroot -tc
	$(MAKECOOKIE)

install-deb:
	@cd $(WORKSRC)
	install -d $(GARMONO_DEBSDIR)
	mv $(WORKSRC)/../*.deb $(GARMONO_DEBSDIR)
ifneq ($(shell arch), arm)
	mv $(WORKSRC)/../*.tar.gz $(GARMONO_DEBSDIR)
endif
	$(MAKECOOKIE)

