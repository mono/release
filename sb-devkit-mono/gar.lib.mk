#-*- mode: Makefile; tab-width: 4; -*-
# ex:ts=4 sw=4

# Copyright (C) 2001 Nick Moffitt
# 
# Redistribution and/or use, with or without modification, is
# permitted.  This software is without warranty of any kind.  The
# author(s) shall not be liable in the event that use of the
# software causes damage.

# cookies go here, so we have to be able to find them for
# dependency checking.
VPATH += $(COOKIEDIR)

# So these targets are all loaded into bbc.port.mk at the end,
# and provide actions that would be written often, such as
# running configure, automake, makemaker, etc.  
#
# The do- targets depend on these, and they can be overridden by
# a port maintainer, since they'e pattern-based.  Thus:
#
# extract-foo.tar.gz:
#	(special stuff to unpack non-standard tarball, such as one
#	accidentally named .gz when it's really bzip2 or something)
#
# and this will override the extract-%.tar.gz rule.

# convenience variable to make the cookie.
MAKECOOKIE = mkdir -p $(COOKIEDIR)/$(@D) && date >> $(COOKIEDIR)/$@
#################### FETCH RULES ####################

URLS = $(subst ://,//,$(foreach SITE,$(FILE_SITES) $(MASTER_SITES),$(addprefix $(SITE),$(DISTFILES))) $(foreach SITE,$(FILE_SITES) $(PATCH_SITES) $(MASTER_SITES),$(addprefix $(SITE),$(PATCHFILES))))


# Download the file if and only if it doesn't have a preexisting
# checksum file.  Loop through available URLs and stop when you
# get one that doesn't return an error code.
$(DOWNLOADDIR)/%:  
	@if test -f $(COOKIEDIR)/checksum-$*; then : ; else \
		echo -e " $(WORKCOLOR)==> Grabbing $(BOLD)$@$(NORMALCOLOR)"; \
		for i in $(filter %/$*,$(URLS)); do  \
			echo -e " 	$(WORKCOLOR)==> Trying $(BOLD)$$i$(NORMALCOLOR)"; \
			$(MAKE) -s $$i || continue; \
			mv $(PARTIALDIR)/$* $@; \
			break; \
		done; \
		if test -r $@ ; then : ; else \
			echo -e "$(ERRORCOLOR)*** GAR GAR GAR!  Failed to download $@!  GAR GAR GAR! ***$(NORMALCOLOR)" 1>&2; \
			false; \
		fi; \
	fi

# download an http URL (colons omitted)
http//%: 
	@wget -c -P $(PARTIALDIR) -T 120 -t 3 http://$*

# download an ftp URL (colons omitted)
ftp//%: 
	@wget -c --passive-ftp -P $(PARTIALDIR) -T 120 -t 3 ftp://$*

# link to a local copy of the file
# (absolute path)
file///%: 
	@if test -f /$*; then \
		ln -sf /$* $(PARTIALDIR)/$(notdir $*); \
	else \
		false; \
	fi

# link to a local copy of the file
# (relative path)
file//%: 
	@if test -f $*; then \
		ln -sf "$(CURDIR)/$*" $(PARTIALDIR)/$(notdir $*); \
	else \
		false; \
	fi

# Using Jeff Waugh's rsync rule.
# DOES NOT PRESERVE SYMLINKS!
rsync//%: 
	@rsync -azvLP rsync://$* $(PARTIALDIR)/

# Using Jeff Waugh's scp rule
scp//%:
	@scp -C $* $(PARTIALDIR)/

cvs//%:
	@cvs -d :pserver:$(shell dirname $* | sed 's,/,:/,') login; \
	cd $(PARTIALDIR); \
	cvs -z3 -d :pserver:$(shell dirname $* | sed 's,/,:/,') co $(shell basename $*)


#################### CHECKSUM RULES ####################

# check a given file's checksum against $(CHECKSUM_FILE) and
# error out if it mentions the file without an "OK".
checksum-%: $(CHECKSUM_FILE) 
	@echo -e " $(WORKCOLOR)==> Running checksum on $(BOLD)$*$(NORMALCOLOR)"
	@rm -f $(CHECKSUM_FILE).tmp
	@cat $(CHECKSUM_FILE) | sed -e 's~ download/~ $(DOWNLOADDIR)/~' > $(CHECKSUM_FILE).tmp
	@if grep -- '$*' $(CHECKSUM_FILE).tmp; then \
		if LC_ALL="C" LANG="C" md5sum -c $(CHECKSUM_FILE).tmp 2>&1 | grep -- '$*' | grep -v ':[ ]\+OK'; then \
			echo -e "$(ERRORCOLOR)*** GAR GAR GAR!  $* failed checksum test!  GAR GAR GAR! ***$(NORMALCOLOR)" 1>&2; \
			rm -f $(CHECKSUM_FILE).tmp ;\
			false; \
		else \
			echo -e "$(SUCCESSCOLOR)file $(BOLD)$* $(SUCCESSCOLOR)passes checksum test!$(NORMALCOLOR)"; \
			rm -f $(CHECKSUM_FILE).tmp ;\
			$(MAKECOOKIE); \
		fi \
	else \
		echo -e "$(ERRORCOLOR)*** GAR GAR GAR!  $* not in $(CHECKSUM_FILE) file!  GAR GAR GAR! ***$(NORMALCOLOR)" 1>&2; \
		rm -f $(CHECKSUM_FILE).tmp ;\
		false; \
	fi


#################### GARCHIVE RULES ####################

# while we're here, let's just handle how to back up our
# checksummed files

$(GARCHIVEDIR)/%: $(GARCHIVEDIR)
	-cp -Lr $(DOWNLOADDIR)/$* $@ 


#################### EXTRACT RULES ####################

# rule to extract uncompressed tarballs
tar-extract-%:
	@echo -e " $(WORKCOLOR)==> Extracting $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@tar -xf $(DOWNLOADDIR)/$* -C $(EXTRACTDIR)
	@$(MAKECOOKIE)

# rule to extract files with tar xzf
tar-gz-extract-%:
	@echo -e " $(WORKCOLOR)==> Extracting $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@gzip -dc $(DOWNLOADDIR)/$* | tar -xf - -C $(EXTRACTDIR)
	@$(MAKECOOKIE)

# rule to extract files with tar and bzip
tar-bz-extract-%:
	@echo -e " $(WORKCOLOR)==> Extracting $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@bzip2 -dc $(DOWNLOADDIR)/$* | tar -xf - -C $(EXTRACTDIR)
	@$(MAKECOOKIE)

# rule to extract files with unzip
zip-extract-%:
	@echo -e " $(WORKCOLOR)==> Extracting $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@unzip $(DOWNLOADDIR)/$* -d $(EXTRACTDIR)
	@$(MAKECOOKIE)

# this is a null extract rule for files which are constant and
# unchanged (not archives)
cp-extract-%:
	@echo -e " $(WORKCOLOR)==> Copying $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@cp -a $(DOWNLOADDIR)/$* $(WORKDIR)/
	@$(MAKECOOKIE)

#gets the meat of a .deb into $(WORKSRC)
deb-bin-extract-%:
	@echo -e " $(WORKCOLOR)==> Extracting $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@ar x $(DOWNLOADDIR)/$*
	@rm debian-binary && mv *.tar.gz $(DOWNLOADDIR) && mkdir $(WORKSRC) && tar -xvz -C $(WORKSRC) -f $(DOWNLOADDIR)/data.tar.gz
	@$(MAKECOOKIE)

### EXTRACT FILE TYPE MAPPINGS ###
# These rules specify which of the above extract action rules to use for a
# given file extension.  Often support for a given extract type can be handled
# by simply adding a rule here.

extract-%.tar: tar-extract-%.tar
	@$(MAKECOOKIE)

extract-%.tar.gz: tar-gz-extract-%.tar.gz
	@$(MAKECOOKIE)

extract-%.tar.Z: tar-gz-extract-%.tar.Z
	@$(MAKECOOKIE)

extract-%.tgz: tar-gz-extract-%.tgz
	@$(MAKECOOKIE)

extract-%.taz: tar-gz-extract-%.taz
	@$(MAKECOOKIE)

extract-%.tar.bz: tar-bz-extract-%.tar.bz
	@$(MAKECOOKIE)

extract-%.tar.bz2: tar-bz-extract-%.tar.bz2
	@$(MAKECOOKIE)

extract-%.tbz: tar-bz-extract-%.tbz
	@$(MAKECOOKIE)

extract-%.zip: zip-extract-%.zip
	@$(MAKECOOKIE)

extract-%.ZIP: zip-extract-%.ZIP
	@$(MAKECOOKIE)

extract-%.deb: deb-bin-extract-%.deb
	@$(MAKECOOKIE)

# For extracting configure script caches
extract-$(GARHOST).cache:
	@echo -e " $(WORKCOLOR)== Copying $(BOLD)$(DOWNLOADDIR)/$(GARHOST).cache$(NORMALCOLOR)"
	@cp $(DOWNLOADDIR)/$(GARHOST).cache $(WORKSRC)/config.cache
	@$(MAKECOOKIE)

# anything we don't know about, we just assume is already
# uncompressed and unarchived in plain format
extract-%: cp-extract-%
	@$(MAKECOOKIE)


#################### PATCH RULES ####################

PATCHDIR ?= $(WORKDIR)
PATCHDIRLEVEL ?= 1
PATCHDIRFUZZ ?= 2
GARPATCH = patch -d$(PATCHDIR) -p$(PATCHDIRLEVEL) -F$(PATCHDIRFUZZ)

# apply bzipped patches
bz-patch-%:
	@echo -e " $(WORKCOLOR)==> Applying patch $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@bzip2 -dc $(DOWNLOADDIR)/$* |$(GARPATCH)
	@$(MAKECOOKIE)

# apply gzipped patches
gz-patch-%:
	@echo -e " $(WORKCOLOR)==> Applying patch $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@gzip -dc $(DOWNLOADDIR)/$* |$(GARPATCH)
	@$(MAKECOOKIE)

# apply normal patches
normal-patch-%:
	@echo -e " $(WORKCOLOR)==> Applying patch $(BOLD)$(DOWNLOADDIR)/$*$(NORMALCOLOR)"
	@$(GARPATCH) <$(DOWNLOADDIR)/$*
	@$(MAKECOOKIE)

# This is used by makepatch
%/gar-base.diff:
	@echo -e " $(WORKCOLOR)==> Creating patch $(BOLD)$@$(NORMALCOLOR)"
	@$(MAKE) EXTRACTDIR=$(SCRATCHDIR) COOKIEDIR=$(SCRATCHDIR)-$(COOKIEDIR) extract
	@if diff --speed-large-files --minimal -Nru $(SCRATCHDIR) $(WORKDIR) > $@; then \
		rm $@; \
	fi

### PATCH FILE TYPE MAPPINGS ###
# These rules specify which of the above patch action rules to use for a given
# file extension.  Often support for a given patch format can be handled by
# simply adding a rule here.

patch-%.bz: bz-patch-%.bz
	@$(MAKECOOKIE)

patch-%.bz2: bz-patch-%.bz2
	@$(MAKECOOKIE)

patch-%.gz: gz-patch-%.gz
	@$(MAKECOOKIE)

patch-%.Z: gz-patch-%.Z
	@$(MAKECOOKIE)

patch-%.diff: normal-patch-%.diff
	@$(MAKECOOKIE)

patch-%.patch: normal-patch-%.patch
	@$(MAKECOOKIE)

#################### CONFIGURE RULES ####################

TMP_DIRPATHS = --prefix=$(prefix) --exec_prefix=$(exec_prefix) --bindir=$(bindir) --sbindir=$(sbindir) --libexecdir=$(libexecdir) --datadir=$(datadir) --sysconfdir=$(sysconfdir) --sharedstatedir=$(sharedstatedir) --localstatedir=$(localstatedir) --libdir=$(libdir) --infodir=$(infodir) --lispdir=$(lispdir) --includedir=$(includedir) --mandir=$(mandir)

NODIRPATHS += --lispdir

DIRPATHS = $(filter-out $(addsuffix %,$(NODIRPATHS)), $(TMP_DIRPATHS))

# configure a package that has an autoconf-style configure
# script.
configure-%/configure: 
	@echo -e " $(WORKCOLOR)==> Running configure in $(BOLD)$*$(NORMALCOLOR)"
	@cd $* && $(CONFIGURE_ENV) ./configure $(CONFIGURE_ARGS)
	@$(MAKECOOKIE)

# configure a package that uses imake
# FIXME: untested and likely not the right way to handle the
# arguments
configure-%/Imakefile: 
	@echo -e " $(WORKCOLOR)==> Running imake in $(BOLD)$*$(NORMALCOLOR)"
	@cd $* && $(CONFIGURE_ENV) imake -DUseInstalled -DBOOTSTRAPCFLAGS="$(CFLAGS)" -I$(DESTDIR)$(libdir)/X11/config $(CONFIGURE_ARGS)
	@$(MAKECOOKIE)

# configure a package that uses a "config" or "oldconfig" make
# target
configure-%/Makefile:
	@echo -e " $(WORKCOLOR)==> Running make in $(BOLD)$*$(NORMALCOLOR)"
	@$(CONFIGURE_ENV) $(firstword $(MAKE)) $(PARALLELMFLAGS) -C $* $(CONFIGURE_ARGS)
	@$(MAKECOOKIE)

#################### BUILD RULES ####################

# build from a standard gnu-style makefile's default rule.
build-%/Makefile:
	@echo -e " $(WORKCOLOR)==> Running make in $(BOLD)$*$(NORMALCOLOR)"
	@$(BUILD_ENV) $(firstword $(MAKE)) $(PARALLELMFLAGS) $(foreach TTT,$(BUILD_OVERRIDE_DIRS),$(TTT)="$($(TTT))") -C $* $(BUILD_ARGS)
	@$(MAKECOOKIE)

build-%/makefile:
	@echo -e " $(WORKCOLOR)==> Running make in $(BOLD)$*$(NORMALCOLOR)"
	@$(BUILD_ENV) $(firstword $(MAKE)) $(PARALLELMFLAGS) $(foreach TTT,$(BUILD_OVERRIDE_DIRS),$(TTT)="$($(TTT))") -C $* $(BUILD_ARGS)
	@$(MAKECOOKIE)

build-%/GNUmakefile:
	@echo -e " $(WORKCOLOR)==> Running make in $(BOLD)$*$(NORMALCOLOR)"
	@$(BUILD_ENV) $(firstword $(MAKE)) $(PARALLELMFLAGS) $(foreach TTT,$(BUILD_OVERRIDE_DIRS),$(TTT)="$($(TTT))") -C $* $(BUILD_ARGS)
	@$(MAKECOOKIE)

#################### STRIP RULES ####################
# The strip rule should probably strip uninstalled binaries.
# TODO: Seth, what was the exact parameter set to strip that you
# used to gain maximal space on the LNX-BBC?

# Strip all binaries listed in the manifest file
# TODO: actually write it!
#  This will likely become almost as hairy as the actual
#  installation code.
strip-$(MANIFEST_FILE):
	@echo -e "$(ERRORCOLOR)Not finished$(NORMALCOLOR)"

# The Makefile must have a "make strip" rule for this to work.
strip-%/Makefile:
	@echo -e " $(WORKCOLOR)==> Running make strip in $(BOLD)$*$(NORMALCOLOR)"
	@$(BUILD_ENV) $(firstword $(MAKE)) -C $* $(BUILD_ARGS) strip
	@$(MAKECOOKIE)

#################### INSTALL RULES ####################

INSTALL_TARGET ?= install

install-%: prefix := $(if $(filter $(USE_STOW),yes),$(STOW_PREFIX)/$(GARNAME)-$(GARVERSION),$(prefix))

# just run make install and hope for the best.
install-%/Makefile:
	@echo -e " $(WORKCOLOR)==> Running make install in $(BOLD)$*$(NORMALCOLOR)"
	@$(firstword $(MAKE)) $(INSTALL_ENV) DESTDIR=$(DESTDIR) $(foreach TTT,$(INSTALL_OVERRIDE_DIRS),$(TTT)="$(DESTDIR)$($(TTT))") -C $* $(INSTALL_ARGS) $(INSTALL_TARGET)
	@$(MAKECOOKIE)

install-%/makefile:
	@echo -e " $(WORKCOLOR)==> Running make install in $(BOLD)$*$(NORMALCOLOR)"
	@$(firstword $(MAKE)) $(INSTALL_ENV) DESTDIR=$(DESTDIR) $(foreach TTT,$(INSTALL_OVERRIDE_DIRS),$(TTT)="$(DESTDIR)$($(TTT))") -C $* $(INSTALL_ARGS) $(INSTALL_TARGET)
	@$(MAKECOOKIE)

install-%/GNUmakefile:
	@echo -e " $(WORKCOLOR)==> Running make install in $(BOLD)$*$(NORMALCOLOR)"
	@$(firstword $(MAKE)) $(INSTALL_ENV) DESTDIR=$(DESTDIR) $(foreach TTT,$(INSTALL_OVERRIDE_DIRS),$(TTT)="$(DESTDIR)$($(TTT))") -C $* $(INSTALL_ARGS) $(INSTALL_TARGET)
	@$(MAKECOOKIE)

# LICENSE INSTALLATION

LICENSEDIR = $(GARDIR)/licenses

GPL_LICENSE_TEXT = $(LICENSEDIR)/GPL.txt
GPL1_LICENSE_TEXT = $(LICENSEDIR)/GPL1.txt
GPL2_LICENSE_TEXT = $(LICENSEDIR)/GPL2.txt
LGPL_LICENSE_TEXT = $(LICENSEDIR)/LGPL.txt
LGPL2_LICENSE_TEXT = $(LICENSEDIR)/LGPL2.txt
LGPL2_1_LICENSE_TEXT = $(LICENSEDIR)/LGPL2_1.txt
BSD_LICENSE_TEXT = $(LICENSEDIR)/BSD.txt
IBMPL_LICENSE_TEXT = $(LICENSEDIR)/IBMPL.txt
ISC_LICENSE_TEXT = $(LICENSEDIR)/ISC.txt
MIT_LICENSE_TEXT = $(LICENSEDIR)/MIT.txt
MIT_X_LICENSE_TEXT = $(LICENSEDIR)/MIT.txt
MPL_LICENSE_TEXT = $(LICENSEDIR)/MPL.txt
Artistic_LICENSE_TEXT = $(LICENSEDIR)/Artistic.txt
Clarified_Artistic_LICENSE_TEXT = $(LICENSEDIR)/Clarified-Artistic.txt
Public_Domain_LICENSE_TEXT = $(LICENSEDIR)/public-domain.txt

install-license-%: $($*_LICENSE_TEXT)
	@echo -e " $(WORKCOLOR)==> Installing $(BOLD)$* $(WORKCOLOR)license text$(NORMALCOLOR)"
	@install -d $(DESTDIR)$(licensedir)/$(GARNAME)/
	@install -m 644 $($*_LICENSE_TEXT) $(DESTDIR)$(licensedir)/$(GARNAME)/
	@$(MAKECOOKIE)

# pkg-config scripts

install-%-config:
	@mkdir -p $(STAGINGDIR)/$(GARNAME)
	@cp -f $(DESTDIR)$(bindir)/$*-config $(STAGINGDIR)/$(GARNAME)/
	@$(MAKECOOKIE)

#################### STOW RULES ####################

stow-%:
	@mkdir -p $(DESTDIR)$(prefix)/stow/$*
	@echo -e " $(WORKCOLOR)==> Relinking $(BOLD)$* $(WORKCOLOR) to become the default version$(NORMALCOLOR)"
	-@mv $(DESTDIR)$(STOW_PREFIX)$(GARNAME) $(DESTDIR)$(STOW_PREFIX)$(GARNAME)-old
	@ln -sf $(DESTDIR)$(STOW_PREFIX)$* $(DESTDIR)$(STOW_PREFIX)$(GARNAME)
	@echo -e " $(WORKCOLOR)==> Stowing $(BOLD)$(GARNAME) $(GARVERSION)$(NORMALCOLOR)"
	@stow -v -d $(DESTDIR)$(STOW_PREFIX) -t $(DESTDIR)$(prefix) -R $(GARNAME)
	@$(MAKECOOKIE)

unstow-%:
	@echo -e " $(WORKCOLOR)==> Unstowing $(BOLD)$*$(NORMALCOLOR)"
	@stow -v -d $(DESTDIR)$(STOW_PREFIX) -t $(DESTDIR)$(prefix) -D $(GARNAME)
	@rm -f $(DESTDIR)$(STOW_PREFIX)/$(GARNAME)
	@rm -f $(COOKIEDIR)/stow-$*



######################################
# Use a manifest file of the format:
# src:dest[:mode[:owner[:group]]]
#   as in...
# ${WORKSRC}/nwall:${bindir}/nwall:2755:root:tty
# ${WORKSRC}/src/foo:${sharedstatedir}/foo
# ${WORKSRC}/yoink:${sysconfdir}/yoink:0600

# Okay, so for the benefit of future generations, this is how it
# works:
# 
# First of all, we have this file with colon-separated lines.
# The $(shell cat foo) routine turns it into a space-separated
# list of words.  The foreach iterates over this list, putting a
# colon-separated record in $(ZORCH) on each pass through.
# 
# Next, we have the macro $(MANIFEST_LINE), which splits a record
# into a space-separated list, and $(MANIFEST_SIZE), which
# determines how many elements are in such a list.  These are
# purely for convenience, and could be inserted inline if need
# be.
MANIFEST_LINE = $(subst :, ,$(ZORCH)) 
MANIFEST_SIZE = $(words $(MANIFEST_LINE))

# So the install command takes a variable number of parameters,
# and our records have from two to five elements.  Gmake can't do
# any sort of arithmetic, so we can't do any really intelligent
# indexing into the list of parameters.
# 
# Since the last three elements of the $(MANIFEST_LINE) are what
# we're interested in, we make a parallel list with the parameter
# switch text (note the dummy elements at the beginning):
MANIFEST_FLAGS = notused notused --mode= --owner= --group=

# The following environment variables are set before the
# installation boogaloo begins.  This ensures that WORKSRC is
# available to the manifest and that all of the location
# variables are suitable for *installation* (that is, using
# DESTDIR)

MANIFEST_ENV += WORKSRC=$(WORKSRC)
# This was part of the "implicit DESTDIR" regime.  However:
# http://gar.lnx-bbc.org/wiki/ImplicitDestdirConsideredHarmful
#MANIFEST_ENV += $(foreach TTT,prefix exec_prefix bindir sbindir libexecdir datadir sysconfdir sharedstatedir localstatedir libdir infodir lispdir includedir mandir,$(TTT)=$(DESTDIR)$($(TTT)))

# ...and then we join a slice of it with the corresponding slice
# of the $(MANIFEST_LINE), starting at 3 and going to
# $(MANIFEST_SIZE).  That's where all the real magic happens,
# right there!
# 
# following that, we just splat elements one and two of
# $(MANIFEST_LINE) on the end, since they're the ones that are
# always there.  Slap a semicolon on the end, and you've got a
# completed iteration through the foreach!  Beaujolais!

# FIXME: using -D may not be the right thing to do!
install-$(MANIFEST_FILE):
	@echo -e " $(WORKCOLOR)==> Installing from $(BOLD)$(MANIFEST_FILE)$(NORMALCOLOR)"
	$(MANIFEST_ENV) ; $(foreach ZORCH,$(shell cat $(MANIFEST_FILE)), install -Dc $(join $(wordlist 3,$(MANIFEST_SIZE),$(MANIFEST_FLAGS)),$(wordlist 3,$(MANIFEST_SIZE),$(MANIFEST_LINE))) $(word 1,$(MANIFEST_LINE)) $(word 2,$(MANIFEST_LINE)) ;)
	@$(MAKECOOKIE)

# stanard steps for installing a minit script
install-%.init:
	@echo -e " $(WORKCOLOR)==> Installing minit script $(BOLD)$*$(NORMALCOLOR)"
	@install -D -m 755 $(WORKDIR)/$*.init $(DESTDIR)$(sysconfdir)/init.d/$*
	@if ! grep "^NOSTOP[ ]=" $(WORKDIR)/$*.init > /dev/null; then \
		install -d $(DESTDIR)$(sysconfdir)/rchalt.d $(DESTDIR)$(sysconfdir)/rcreboot.d ;\
		ln -sf ../init.d/$* $(DESTDIR)$(sysconfdir)/rchalt.d/K$* ;\
		ln -sf ../init.d/$* $(DESTDIR)$(sysconfdir)/rcreboot.d/K$* ;\
	fi
	@$(MAKECOOKIE)

#################### DEPENDENCY RULES ####################

# These three lines are here to grandfather in all the packages that use
# BUILDDEPS, LIBDEPS and DEPENDS.  BUILDDEPS, LIBDEPS, and DEPENDS are not
# obsolete... merely integrated into a more general mechanism
$(DESTIMG)_DEPENDS += $(addprefix lang/,$(filter-out none,$(SOURCE_LANGUAGES))) $(LIBDEPS) $(DEPENDS)
IMGDEPS += $(sort $(if $(BUILDDEPS),build,) $(if $(strip $($(DESTIMG)_DEPENDS)),$(DESTIMG),))
build_DEPENDS += $(BUILDDEPS)

# Standard deps install into the standard install dir.  For the
# BBC, we set the includedir to the build tree and the libdir to
# the install tree.  Most dependencies work this way.

$(GARDIR)/%/$(COOKIEROOTDIR)/$(__DESTIMG).d/install:
	@echo -e " $(WORKCOLOR)==> Building $(BOLD)$* $(WORKCOLOR)as a dependency$(NORMALCOLOR)"
	@$(MAKE) -C $(GARDIR)/$* install DESTIMG=$(__DESTIMG)

# builddeps need to have everything put in the build DESTIMG
#$(GARDIR)/%/$(COOKIEROOTDIR)/build.d/install:
#	@echo ' ==> Building $* as a build dependency'
#	@$(MAKE) -C $(GARDIR)/$* install	DESTIMG=build

# Source Deps grab the source code for another package
# XXX: nobody uses this, but it should really be more like
# $(GARDIR)/%/cookies/patch:
srcdep-$(GARDIR)/%:
	@echo -e " $(WORKCOLOR)==> Grabbing source for $(BOLD)$* $(WORKCOLOR)as a dependency$(NORMALCOLOR)"
	@$(MAKE) -C $(GARDIR)/$* patch-p extract-p > /dev/null 2>&1 || \
	 $(MAKE) -C $(GARDIR)/$* patch

# Image deps create dependencies on package installations in
# images other than the current package's DESTIMG.
IMGDEP_TARGETS = $(foreach TTT,$(filter-out $($*_NODEPEND),$($*_DEPENDS)),$(subst xyzzy,$(TTT),$(GARDIR)/xyzzy/$(COOKIEROOTDIR)/$*.d/install))
imgdep-%:
	@$(if $(IMGDEP_TARGETS),$(MAKE) __DESTIMG="$*" $(IMGDEP_TARGETS),true)
	@$(MAKECOOKIE)

# SOURCEPKG
# This is sort of like a srcdep, except it extracts and patches the
# source for the specified package into the current packages $(WORKDIR)

$(COOKIEDIR)/sourcepkg-%/patch:
	@$(MAKE) -C $(GARDIR)/$* DESTIMG="$(DESTIMG)" DOWNLOADDIR="$(GARDIR)/$(CATEGORIES)/$(GARNAME)/$(DOWNLOADDIR)" EXTRACTDIR="$(GARDIR)/$(CATEGORIES)/$(GARNAME)/$(EXTRACTDIR)" WORKDIR="$(GARDIR)/$(CATEGORIES)/$(GARNAME)/$(WORKDIR)" COOKIEDIR="$(GARDIR)/$(CATEGORIES)/$(GARNAME)/$(COOKIEDIR)/sourcepkg-$*" patch

# Igor's info and man gzipper rule
gzip-info-man: gzip-info gzip-man

gzip-info:
	find $(DESTDIR) -type f -iname *.info* -not -iname *.gz | \
        xargs -r gzip --force

gzip-man:
	find $(DESTDIR) -type f -iname *.[1-8] -size +2 -print | \
        xargs -r gzip --force

#################### PRUNING RULES #######################

# Pruning targets are for use by packages which take a DESTDIR and package it
# up into something.  For example, meta/singularity packages a DESTDIR up as a
# cloop-compressed romfs, and meta/build-chroot packages up a DESTDIR as a
# tarball.  The DESTDIR is presumed to have been copied into $(WORKSRC).

# Full removal of stuff
# This rule cannot have a $MAKECOOKIE... consider the following example:
# prune-delete-$(WORKSRC)/usr/share/doc
# prune-delete-$(WORKSRC)/usr
# the first will create its cookie: $(COOKIEDIR)/prune-delete-$(WORKSRC)/usr/share/doc
# the second will NOT BE ABLE to create its cookie: $(COOKIEDIR)/prune-delete-$(WORKSRC)/usr
# because "usr" is a directory in the path of the first one.
#
# I suppose we could add a weird suffix to all of our cookies to avoid this
# sort of collision.  Like ".ck" or something.
#
# The effect of not having a $(MAKECOOKIE) on this rule is that GAR might attempt
# to remove things multiple times... OH WELL.
prune-delete-$(WORKSRC)%:
	@rm -rf $(WORKSRC)$*

prune-boot:
	rm -f $(WORKSRC)/boot/bzImage
	$(MAKECOOKIE)

prune-terminfo:
	# terminfo should be handled carefully because we need a few
	# of those terminals (vt*, linux, xterm, screen, ...), but
	# not most of them!
	cd $(WORKSRC)/share/terminfo && tar cvf ../terminfo.tar $(KEEPTERMINFO)
	cd $(WORKSRC)/share/terminfo && rm -rf *
	cd $(WORKSRC)/share/terminfo && tar xvf ../terminfo.tar && rm -f ../terminfo.tar
	$(MAKECOOKIE)

prune-language-modules:
	# XXX: TODO for Perl and Ruby
	# XXX: also remove some modules which users are unlikely to need
	@echo -e "$(WORKCOLOR)Deleting compiled Python modules...$(NORMALCOLOR)"
	[ ! -d $(WORKSRC)/lib/python2.2 ] || find $(WORKSRC)/lib/python2.2 -name '*.py[co]' -exec rm -f '{}' ';'
	@echo -e "$(WORKCOLOR)Removing Python config directory...$(NORMALCOLOR)"
	rm -rf $(WORKSRC)/lib/python2.2/config
	@echo -e "$(WORKCOLOR)Deleting Perl documentation...$(NORMALCOLOR)"
	[ ! -d $(WORKSRC)/lib/perl5 ] || find $(WORKSRC)/lib/perl5 -name '*.pod' -exec rm -f '{}' ';'
	@echo -e "$(WORKCOLOR)Deleting Perl unicore...$(NORMALCOLOR)"
#	[ ! -d $(WORKSRC)/lib/perl5 ] || find $(WORKSRC)/lib/perl5 -type d -name unicore -exec rm -rf '{}' ';'
	[ ! -d $(WORKSRC)/lib/perl5/5.8.0/unicore ] || rm -rf $(WORKSRC)/lib/perl5/5.8.0/unicore
	$(MAKECOOKIE)

prune-xemacs:
	@echo -e "$(WORKCOLOR)Pruning XEmacs distribution...$(NORMALCOLOR)"
	[ ! -d $(WORKSRC)$(libdir)/xemacs-21.4.9/etc/photos ] || rm -rf $(WORKSRC)$(libdir)/xemacs-21.4.9/etc/photos
	[ ! -d $(WORKSRC)$(libdir)/xemacs-21.4.9/info ] || rm -rf $(WORKSRC)$(libdir)/xemacs-21.4.9/info
	[ ! -d $(WORKSRC)$(libdir)/xemacs-21.4.9/lisp ] || (for f in $$(find $(WORKSRC)$(libdir)/xemacs-21.4.9/lisp -name "*.el" -or -name "*.elc"  | sed "s/elc/el/g"  | sort | uniq -d); do rm -rf $$f; done)
	[ ! -d $(WORKSRC)$(libdir)/xemacs-21.4.9/etc ] || rm -rf $(WORKSRC)$(libdir)/xemacs-21.4.9/etc/{ORDERS*,OONEWS,TUTORIAL*}
	# xpms may be required if we later compile with x11 support
	[ ! -d $(WORKSRC)$(libdir)/xemacs-21.4.9/etc ] || (for f in $$(find $(WORKSRC)$(libdir)/xemacs-21.4.9/etc -name "*.xpm"); do rm -f $$f; done)
	$(MAKECOOKIE)

prune-xemacs-packages: prune-xemacs
	@echo -e "$(WORKCOLOR)Pruning XEmacs packages...$(NORMALCOLOR)"
	[ ! -d $(WORKSRC)$(libdir)/xemacs/xemacs-packages/lisp ] || (for f in $$(find $(WORKSRC)$(libdir)/xemacs/xemacs-packages/lisp -name "*.el" -or -name "*.elc"  | sed "s/elc/el/g"  | sort | uniq -d); do rm -rf $$f; done)
	[ ! -d $(WORKSRC)$(libdir)/xemacs/xemacs-packages/info ] || rm -rf $(WORKSRC)$(libdir)/xemacs/xemacs-packages/info
	[ ! -d $(WORKSRC)$(libdir)/xemacs/xemacs-packages/man ] || rm -rf $(WORKSRC)$(libdir)/xemacs/xemacs-packages/man
	# etc contains some xpms -- if we later compile xemacs with x11 support they may be needed
	[ ! -d $(WORKSRC)$(libdir)/xemacs/xemacs-packages/etc ] || rm -rf $(WORKSRC)$(libdir)/xemacs/xemacs-packages/etc
	$(MAKECOOKIE)

prune-x11:
	# assuming X11 stuff is not in /usr/X11, just plain DESTDIR
	rm -rf $(WORKSRC)$(libdir)/X11/doc
	rm -rf $(WORKSRC)$(libdir)/X11/config
	rm -rf $(WORKSRC)$(libdir)/X11/locale
	$(MAKECOOKIE)

# XXX: we can probably remove even more sections than just .note and .comment
# XXX: and if we can remove 1k per binary, we could save hundreds of k overall
GOODSTRIP ?= strip --strip-all -R .note -R .comment

prune-strip: prune-strip-binaries prune-strip-shared-libraries

prune-strip-binaries:
	# ignore errors in strip (they result from things like inability
	# to strip shell scripts)
	$(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/bin/*)) || true
	$(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/usr/bin/*)) || true
	$(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/sbin/*)) || true
	$(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/usr/sbin/*)) || true
	$(MAKECOOKIE)

prune-strip-shared-libraries:
	# There was a claim that stripping shared libraries damaged them.
	# As far as we can determine, stripping _static_ libraries will
	# damage them, but stripping shared libraries is OK.  Note that
	# we do not attempt to strip static libraries at all -- instead,
	# we delete them!
	# $(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/lib/*)) || true
	# $(GOODSTRIP) $(filter-out $(addprefix %, $(NOSTRIP)), $(shell echo $(WORKSRC)/usr/X11R6/lib/*)) || true
	# XXX: does stripping _all_ .so files work properly?
	find $(WORKSRC) -name '*.so' -exec $(GOODSTRIP) '{}' ';'
	$(MAKECOOKIE)

prune-documentation:
	rm -rf $(WORKSRC)/doc
	rm -rf $(WORKSRC)/info
	rm -rf $(WORKSRC)/usr/share/info
	rm -rf $(WORKSRC)/man
	rm -rf $(WORKSRC)/man6
	rm -rf $(WORKSRC)/share/man
	rm -rf $(WORKSRC)/share/gnupg/FAQ $(WORKSRC)/share/gnupg/faq.html
	mkdir -p $(WORKSRC)/share/doc.keep
	test -z "$(wildcard $(WORKSRC)/share/doc/README.*)" || mv $(WORKSRC)/share/doc/README.* $(WORKSRC)/share/doc.keep
	rm -rf $(WORKSRC)/share/doc
	mv $(WORKSRC)/share/doc.keep $(WORKSRC)/share/doc
	$(MAKECOOKIE)

prune-shared-files:
	# get rid of extraneous stuff in /share and /usr/share
	# XXX: some users will be unhappy about wiping out locales! XXX we should
	# have some locale data, probably!
	rm -rf $(WORKSRC)/share/locale $(WORKSRC)/usr/share/locale $(WORKSRC)/share/i18n
	rm -rf $(WORKSRC)/share/zoneinfo
	rm -rf $(WORKSRC)/share/vim/vim61/syntax
	rm -rf $(WORKSRC)/share/vim/vim61/macros
	rm -rf $(WORKSRC)/share/cvs
	rm -rf $(WORKSRC)/share/aclocal  # only needed if compiling
	rm -rf $(WORKSRC)/share/de  $(WORKSRC)/share/el  $(WORKSRC)/share/es  $(WORKSRC)/share/et  $(WORKSRC)/share/it  $(WORKSRC)/share/no  $(WORKSRC)/share/pl
	[ ! -d $(WORKSRC)/share/vim/vim61/doc ] || find $(WORKSRC)/share/vim/vim61/doc -not -name help.txt -and -not -name intro.txt -and -not -name uganda.txt -and -not -name tags -exec rm -f '{}' ';'
	# XXX: this should not be in /usr/share in the first place, probably
	rm -rf $(WORKSRC)/share/keymaps/{amiga,atari,mac,ppc,sun}
	$(MAKECOOKIE)

relink-duplicates:
	# some hard links didn't seem to survive
	cd $(WORKSRC)$(bindir) && ln -sf python2.2 python
	cd $(WORKSRC)$(bindir) && ln -sf perl5.8.0 perl
	cd $(WORKSRC)$(bindir) && ln -sf mkisofs mkhybrid
	$(MAKECOOKIE)

prune-devel: prune-headers prune-sources prune-compiler prune-static-libraries

# Wholesale deletion of various include directories
# XXX: Is there any reason to list /usr/*?
prune-headers: $(addprefix prune-delete-$(WORKSRC),$(includedir) /usr/X11R6/include /usr/share/keymaps/include /usr/share/keymaps/i386/include /usr/share/keymaps/mac/include $(libdir)/glib)
	$(MAKECOOKIE)

# Wholesale deletion of $(sourcedir)
prune-sources: \
	prune-delete-$(WORKSRC)$(sourcedir)
	$(MAKECOOKIE)

# All the place where the compiler lives
prune-compiler: $(addprefix prune-delete-$(WORKSRC),$(exec_prefix)/$(GARTARGET) $(libdir)/gcc-lib)
	$(MAKECOOKIE)

# Deletion of static libraries from various lib directories
# XXX: Is there any reason to list /usr/*?
prune-static-libraries:
	rm -f $(WORKSRC)/lib/*.a
	rm -f $(WORKSRC)/usr/lib/*.a
	rm -f $(WORKSRC)/usr/X11R6/lib/*.a
	rm -f $(WORKSRC)/usr/local/lib/*.a
	@echo "$(WORKCOLOR)NOT deleting all other static library archives."
	@echo "Remaining static libraries in DESTDIR are currently$(BOLD)"
	find $(WORKSRC) -name '*.a' -print
	@echo -e "$(NORMALCOLOR)"
	$(MAKECOOKIE)

prune-superfluous-binaries:
	# XXX: TODO
	# XXX: will this affect localization?
	rm -rf $(WORKSRC)/lib/gconv
	rm -f $(WORKSRC)$(bindir)/xaumix
	$(MAKECOOKIE)

valueof-%:
	@echo "$($*)"

show-%s:
	@$(MAKE) -s DESTIMG=$(DESTIMG) deep-valueof-$* | sort | uniq

# Mmm, yesssss.  cookies my preciousssss!  Mmm, yes downloads it
# is!  We mustn't have nasty little gmakeses deleting our
# precious cookieses now must we?
.PRECIOUS: $(DOWNLOADDIR)/% $(COOKIEDIR)/% $(FILEDIR)/%
