# Notes:
#
# * Try to use makefile from :
#   http://www.go-mono.com/archive/helper/make-3.80-1.tar.bz2
#
# * Try to install all mono dependencies.
#
# * If possible show detect and show possible problems like wrong cygwin 
# package version.
#
# The list of dependencies for cygwin can be founded here:
#
#   http://anonsvn.mono-project.com/source/trunk/release/packaging/defs/mono
#
# And for gtk-sharp, here:
#
#   http://anonsvn.mono-project.com/source/trunk/release/packaging/defs/gtk-sharp
#
# The idea is to download this packages and use it.
#

GARNAME    = build
CATEGORIES = cygwin/tasks
GARVERSION = $(GARMONO_VERSION)

DEPENDS  = cygwin/deps/make
DEPENDS += cygwin/deps/glib
DEPENDS += cygwin/deps/pkgconfig
DEPENDS += cygwin/deps/zlib
DEPENDS += linux/mono/environment
DEPENDS += linux/mono/mono

DESCRIPTION = Mono Cygwin build meta package
define BLURB
 This meta package build and install mono environment for cygwin, all library
 dependecies is also instaled.
endef

# This should go before any hand-made rules.
include ../../../gar.mk

