GARNAME    = environment
GARVERSION = $(GARMONO_VERSION)
CATEGORIES = mono

DESCRIPTION = Environment vars scripts for Mono
define BLURB
 This package contains the environment vars scripts for mono, it can be used to
 obtain all environments vars needed to execute mono.
endef

BUILD_SCRIPTS = environment
INSTALL_SCRIPTS = environment

# This should go before any hand-made rules.
include ../../gar.mk

build-environment:
	$(MAKECOOKIE)

install-environment:
	mkdir -p $(bindir)
	install -m 755 files/monoenv $(bindir)/
	$(MAKECOOKIE)

