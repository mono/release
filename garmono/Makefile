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

TGPATHS = $(shell find . -maxdepth 4 -mindepth 4 -name Makefile)
TARGETS = $(sort $(subst ./,, $(subst /Makefile,, $(TGPATHS))))

TKPATHS = $(shell find . -maxdepth 4 -mindepth 4 -name Makefile | grep /tasks/)
TASKS   = $(sort $(subst /tasks,, $(subst ./,, $(subst /Makefile,, $(TKPATHS)))))


default: help

build:
	@if [ $(HOST_OS) = "Cygwin" ]; then \
		$(MAKE) -C cygwin/tasks/$@ install; \
	else \
		$(MAKE) -C linux/tasks/$@ install; \
	fi;

clean:
	@for i in $(TARGETS) ; do \
		$(MAKE) -C $$i $@ ; \
	done

help:
	@echo -e $(HELPMSG) 
	@echo -e "Usage: make [task or target]\n"
	@echo -e "Tasks:\n"
	@for i in $(TASKS) ; do \
		echo "    $$i" ; \
	done
	@echo -e "\nTo show all available targets type 'make targets' \n"

tasks:
	@echo -e $(HELPMSG)
	@echo -e "\nAvailable tasks:\n"
	@for i in $(TASKS) ; do \
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

$(TASKS):
	$(MAKE) -C $(subst /,/tasks/,$@) install

$(TARGETS):
	$(MAKE) -C $@ install

%:
	@echo -e "Invalid task/target, use 'make help' to see available options\n"

.SILENT:
.PHONY: default build clean help tasks targets $(TASKS) $(TARGETS)

