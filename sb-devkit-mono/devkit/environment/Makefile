GARNAME = environment
GARVERSION = 0
CATEGORIES = mono-devkit

LIBDEPS =
DEPENDS =

DESCRIPTION = environment

DEBIAN_PACKAGES = 

define BLURB
 # FIXME: blurb goes here
endef

INSTALL_SCRIPTS = environment

include ../category.mk

install-environment:
	install -m 644 files/target_setup.sh $(prefix)/
	install -m 644 files/environment $(sysconfdir)/
	$(MAKECOOKIE)
