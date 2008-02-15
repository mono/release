GARNAME    = environment
CATEGORIES = maemo/devkit
GARVERSION = 0

DESCRIPTION = environment
define BLURB
 # FIXME: blurb goes here
endef

INSTALL_SCRIPTS = environment

include ../../../gar.mk

install-environment:
	mkdir -p $(sysconfdir)
	install -m 644 files/environment $(sysconfdir)/
	install -m 644 files/target_setup.sh $(prefix)/
	$(MAKECOOKIE)
