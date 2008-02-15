GARNAME    = default-build-web
CATEGORIES = linux/tasks
GARVERSION = $(GARMONO_VERSION)

DEPENDS  = task/default-build
DEPENDS += linux/mono/xsp
#DEPENDS += mono/mod_mono

DESCRIPTION = Mono linux build meta package with web tools included
define BLURB
 This package build and install mono environment, normally at /opt/mono, it is
 the default behavior of GarMono and is most commonly used by developers that
 whats to have an up to date system.
endef

# This should go before any hand-made rules.
include ../../../gar.mk

