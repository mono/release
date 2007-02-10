#-*- mode: Makefile; tab-width: 4; -*-
# ex:ts=4

# This file contains configuration variables that are global to
# the GAR system.  Users wishing to make a change on a
# per-package basis should edit the category/package/Makefile, or
# specify environment variables on the make command-line.

# Variables that define the default *actions* (rather than just
# default data) of the system will remain in bbc.gar.mk
# (bbc.port.mk)

-include $(GARDIR)/.gar-local.conf

# Scratchbox-specific values.  You should override SBOX_DIR and
# SBOX_VERSION on the command line or via the environment.

SBOX_ROOT ?= 
SBOX_VERSION ?= $(shell date +"%F %T")
export SBOX_ROOT SBOX_VERSION

SBOX_DIR = $(SBOX_ROOT)/scratchbox
#SBOX_SPECS = /scratchbox/compilers/host-gcc/host-gcc.specs
SBOX_LDFLAGS = -Wl,-rpath -Wl,/scratchbox/host_shared/lib/ -Wl,-rpath -Wl,/scratchbox/tools/lib/ -Wl,-rpath -Wl,$(SBOX_PREFIX)/lib/

MASTER_SITES ?= http://go-mono.com/sources/mono/ ftp://ftp.gtk.org/pub/gtk/v2.8/

# If the color codes are interfering with your terminal, consider
# commenting this next line out.

COLOR_GAR ?= yes

# changing this to "yes" will cause the GAR build to use the
# "stow" utility to merge packages into the system tree using
# symlinks.  

USE_STOW ?= no
STOW_PREFIX ?= $(prefix)/stow/

# Setting this variable will cause the results of your builds to
# be cleaned out after being installed.  Uncomment only if you
# desire this behavior!

# export BUILD_CLEAN = true

ALL_DESTIMGS = main

# These are the standard directory name variables from all GNU
# makefiles.  They're also used by autoconf, and can be adapted
# for a variety of build systems.
# 
# TODO: set $(SYSCONFDIR) and $(LOCALSTATEDIR) to never use
# /usr/etc or /usr/var

# Directory config for the "main" image
main_prefix ?= $(SBOX_PREFIX)
main_exec_prefix = $(prefix)
main_bindir = $(exec_prefix)/bin
main_sbindir = $(exec_prefix)/bin
main_libexecdir = $(exec_prefix)/libexec
main_datadir = $(prefix)/share
main_sysconfdir = $(prefix)/etc
main_sharedstatedir = $(prefix)/share
main_localstatedir = $(prefix)/var
main_libdir = $(exec_prefix)/lib
main_infodir = $(prefix)/info
main_lispdir = $(prefix)/share/emacs/site-lisp
main_includedir = $(prefix)/include
main_mandir = $(prefix)/man
main_docdir = $(prefix)/share/doc
main_sourcedir = $(prefix)/src
main_licensedir = $(prefix)/licenses

# the DESTDIR is used at INSTALL TIME ONLY to determine what the
# filesystem root should be.  Each different DESTIMG has its own
# DESTDIR.
main_DESTDIR ?= $(SBOX_ROOT)

main_CPPFLAGS += 
main_CFLAGS += 
main_CXXFLAGS += 
main_LDFLAGS += $(SBOX_LDFLAGS)

# Default main_CC to gcc, $(DESTIMG)_CC to main_CC and set CC based on $(DESTIMG)
#main_CC ?= gcc -specs=$(SBOX_SPECS)
#main_CXX ?= g++ -specs=$(SBOX_SPECS)
main_CC ?= gcc 
main_CXX ?= g++ 
main_LD ?= ld
main_RANLIB ?= ranlib
main_CPP ?= cpp
main_AS ?= as
main_AR ?= ar

# gar.mk needs this
build_CC ?= gcc

# GARCH and GARHOST for main.  Override these for cross-compilation
main_GARCH ?= $(shell arch)
main_GARHOST ?= $(shell gcc -dumpmachine)

# Assume the same of main, also check for python
main_NODEPEND += lang/c lang/c++
main_NODEPEND += $(if $(shell which perl),lang/perl,)
main_NODEPEND += $(if $(shell which python),lang/python,)

# Most stuff is written in C, so SOURCE_LANGUAGES will default to that
SOURCE_LANGUAGES ?= c

# This is for foo-config chaos
PKG_CONFIG_PATH=$(DESTDIR)$(libdir)/pkgconfig/

# Put these variables in the environment during the
# configure build and install stages
STAGE_EXPORTS = DESTDIR prefix exec_prefix bindir sbindir libexecdir datadir
STAGE_EXPORTS += sysconfdir sharedstatedir localstatedir libdir infodir lispdir
STAGE_EXPORTS += includedir mandir docdir sourcedir
STAGE_EXPORTS += CPPFLAGS CFLAGS LDFLAGS
STAGE_EXPORTS += CC CXX CPP LD RANLIB AS AR

CONFIGURE_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
BUILD_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
INSTALL_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")
MANIFEST_ENV += $(foreach TTT,$(STAGE_EXPORTS),$(TTT)="$($(TTT))")

# Global environment
export GARBUILD
#export PATH LD_LIBRARY_PATH #LD_PRELOAD
#export PKG_CONFIG_PATH

# prepend the local file listing
FILE_SITES = file://$(FILEDIR)/
