GARNAME    = build-svn
CATEGORIES = cygwin/tasks
GARVERSION = $(GARMONO_VERSION)

DEPENDS  = cygwin/deps/make
DEPENDS += cygwin/deps/glib
DEPENDS += cygwin/deps/pkgconfig
DEPENDS += cygwin/deps/zlib
DEPENDS += mono/environment
DEPENDS += mono/mono

DESCRIPTION = Mono Cygwin build meta package (SVN)
define BLURB
 This meta package build and install mono environment for cygwin, all library
 dependecies is also instaled.
endef

# This should go before any hand-made rules.
include ../../../gar.mk

