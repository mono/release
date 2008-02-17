GARNAME    = environment
CATEGORIES = maemo/devkit
GARVERSION = 0

DESCRIPTION = Environment vars for Mono Devkit
define BLURB
 Environment vars needed by Mono Scratchbox Devkit.
endef

GARMONO_DESTDIR = $(SBOX_PREFIX)
INSTALL_SCRIPTS = environment

include ../../../gar.mk

install-environment:
	echo $(sysconfdir)/
	echo "---------------------------------"
	mkdir -p $(sysconfdir)
	install -m 644 files/environment $(sysconfdir)/
	install -m 644 files/target_setup.sh $(prefix)/
	$(MAKECOOKIE)
