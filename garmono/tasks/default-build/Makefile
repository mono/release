GARNAME    = default-build
GARVERSION = $(GARMONO_VERSION)
CATEGORIES = tasks

DEPENDS  = mono/environment
DEPENDS += mono/mono
DEPENDS += mono/libgdiplus
DEPENDS += mono/gluezilla

DESCRIPTION = Mono linux build meta package
define BLURB
 This package build and install mono environment, normally at /opt/mono, it is
 the default behavior of GarMono and is most commonly used by developers that
 whats to have an up to date system.
endef

# This should go before any hand-made rules.
include ../../gar.mk

