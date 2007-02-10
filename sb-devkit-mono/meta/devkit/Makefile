GARNAME = mono-devkit
GARVERSION = 1
CATEGORIES = meta
GARDIR = ../..

DEPENDS  = devkit/mono
#DEPENDS  += devkit/gtk-sharp

DESCRIPTION = mono-devkit

define BLURB
 #FIXME: blurb goes here
endef

include ../../gar.mk

install-%/Makefile:
	@mkdir -p $(COOKIEDIR)/
	$(MAKECOOKIE)
