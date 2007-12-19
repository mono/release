#
# GarMono: Top-level Makefile for the entire tree.
# 
# Redistribution and/or use, with or without modification, is permitted.  This 
# software is without warranty of any kind.  The author(s) shall not be liable 
# in the event that use of the software causes damage.
#
# Copyright (c) 2007-2008 Novell, Inc.
#
# Author(s):
#	Everaldo Canuto  <ecanuto@novell.com>
#

VERSION  = "1.2.6alpha"
HELPMSG  = "GARMONO $(VERSION) is a utility that allows users to build Mono from sources"
HOST_OS  = $(shell uname -o)

TGPATHS  = $(shell find . -maxdepth 4 -mindepth 3 -name Makefile)
TARGETS  = $(sort $(subst ./,, $(subst /Makefile,, $(TGPATHS))))
PACKAGES = $(filter-out tasks/%, $(TARGETS))
TASKS    = $(subst tasks/,, $(filter tasks/%, $(TARGETS)))

default: help

$(TASKS):
	$(MAKE) -C tasks/$@ install

$(PACKAGES):
	$(MAKE) -C $@ install

clean:
	@for i in $(TARGETS) ; do \
		$(MAKE) -C $$i $@ ; \
	done

help:
	@echo -e $(HELPMSG) 
	@echo -e "Usage: make [task or package]\n"
	@echo -e "Tasks:\n"
	@for i in $(TASKS) ; do \
		echo "    $$i" ; \
	done
	@echo -e "\nTo show all available packages type 'make packages'\n"

packages:
	@echo -e $(HELPMSG)
	@echo -e "\nAvailable packages:\n"
	@for i in $(PACKAGES) ; do \
		echo "    $$i" ; \
	done
	@echo ""

targets:
	@echo -e $(HELPMSG)
	@echo -e "\nTargets:\n"
	@for i in $(TARGETS) ; do \
		echo "    $$i" ; \
	done
	@echo ""

%:
	@echo -e "Invalid task/package, use 'make help' to see available options\n"

.SILENT:
.PHONY: default $(TASKS) $(PACKAGES) clean help help-packages 

