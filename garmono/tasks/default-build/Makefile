GARNAME    = default-build
GARVERSION = $(GARMONO_VERSION)
CATEGORIES = tasks

DEPENDS  = mono/environment
DEPENDS += mono/mono
DEPENDS += mono/libgdiplus
DEPENDS += mono/gluezilla

DESCRIPTION = Mono linux build meta package
define BLURB
 This meta package build and install mono environment for linux, all library
 dependecies is also instaled.
endef

# This should go before any hand-made rules.
include ../../gar.mk

