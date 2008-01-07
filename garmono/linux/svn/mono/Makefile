GARNAME    = mono
GARVERSION = svn
CATEGORIES = svn

DISTFILES  = mono
DISTFILES += mcs

MASTER_SITES = $(GARMONO_SVNROOT)
#WORKDIR      = $(DESTDIR)$(sourcedir)

DESCRIPTION = Mono
define BLURB
 Mono provides the necessary software to develop and run .NET client and server
 applications on Linux, Solaris, Mac OS X, Windows, and Unix.
endef

CONFIGURE_SCRIPTS = $(WORKSRC)/autogen.sh
BUILD_SCRIPTS = $(WORKSRC)/Makefile
INSTALL_SCRIPTS = $(WORKSRC)/Makefile

CONFIGURE_ARGS = $(DIRPATHS)

# This should go before any hand-made rules.
include ../../gar.mk
include ../../gar.devel.mk


