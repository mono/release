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
	sed -e 's,#mono-prefix#,$(GARMONO_DESTDIR),' files/monoenv.in > $(WORKSRC)/monoenv
	$(MAKECOOKIE)

install-environment:
	install -d $(DESTDIR)$(bindir)
	install -m 755 $(WORKSRC)/monoenv $(DESTDIR)$(bindir)/
	$(MAKECOOKIE)

