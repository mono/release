GARNAME    = build
CATEGORIES = linux/tasks
GARVERSION = $(GARMONO_VERSION)

DEPENDS  = linux/mono/environment
DEPENDS += linux/mono/mono
DEPENDS += linux/mono/libgdiplus
DEPENDS += linux/mono/gluezilla

DESCRIPTION = Mono linux build meta package
define BLURB
 This meta package build and install mono environment for linux, all library
 dependecies is also instaled.
endef

# This should go before any hand-made rules.
include ../../../gar.mk

