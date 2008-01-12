GARNAME    = build
GARVERSION = $(GARMONO_VERSION)
CATEGORIES = linux/tasks

DEPENDS  = linux/pkgs/environment
DEPENDS += linux/pkgs/mono
DEPENDS += linux/pkgs/libgdiplus
DEPENDS += linux/pkgs/gluezilla

DESCRIPTION = Mono linux build meta package
define BLURB
 This meta package build and install mono environment for linux, all library
 dependecies is also instaled.
endef

# This should go before any hand-made rules.
include ../../gar.mk

