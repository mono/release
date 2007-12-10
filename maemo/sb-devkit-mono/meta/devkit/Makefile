GARNAME = mono-devkit
GARVERSION = 1
CATEGORIES = meta
DESCRIPTION = mono-devkit
GARDIR = ../..

DEPENDS  = devkit/mono
DEPENDS += devkit/environment

include ../../gar.mk

install-%/Makefile:
	@mkdir -p $(COOKIEDIR)/
	$(MAKECOOKIE)
