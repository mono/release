#
# spec file for package gtk-sharp2 (Version MACRO)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           gtk-sharp2
%define _name gtk-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
Url:            http://gtk-sharp.sf.net
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        .Net Language Bindings for GTK+
Patch0:         gtk-sharp-optflags.patch
Patch1:         gtk-sharp-revert_unportable_relocatable.patch
Patch2:         gtk-sharp-makefile.patch
Patch3:         gtk-sharp-find_gtkhtml_ver.patch
Patch4:         gtk-sharp-fix_vte_so_version.patch
Patch5:         gnome-sharp-revert_unportable_relocatable.patch
# PATCH-FIX-OPENSUSE Fix: Program returns random data in a function
Patch6:         gtk-warn-fix.patch
%define old_version 2.4.3
%define new_version 2.8.5
%define new_split_version 2.10.4
%define two_twelve_version 2.12.1
#####  suse  ####
%if 0%{?suse_version}
## which gtk version ###
%if %suse_version < 1010
%define _version %old_version
%endif
%if %suse_version == 1010
%define _version %new_version
%endif
%if %suse_version == 1020
%define _version %new_split_version
%endif
%if %suse_version >= 1030
%define _version %two_twelve_version
%endif
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2
%define new_suse_buildrequires librsvg-devel mono-devel vte-devel gnome-panel-devel  monodoc-core update-desktop-files
%if %sles_version == 10
BuildRequires: %{new_suse_buildrequires} gnome-panel-nld-devel -gnome-panel-devel
%endif
%if %suse_version >= 1020
BuildRequires:  %{new_suse_buildrequires} gtkhtml2-devel
%endif
%if %suse_version == 1010
BuildRequires:  %{new_suse_buildrequires} gtkhtml2-devel
%endif
%endif
#################
####  fedora  ####
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%if 0%{?fedora_version} < 6
%define _version %new_version
%endif
%if 0%{?fedora_version} == 6
%define _version %new_split_version
%endif
%if 0%{?fedora_version} == 7
%define _version %new_split_version
%endif
%if 0%{?fedora_version} >= 8
%define _version %two_twelve_version
%endif
# All fedora distros (5 and 6) have the same names, requirements
BuildRequires:  gnome-panel-devel gtkhtml3-devel libgnomeprintui22-devel librsvg2-devel mono-devel monodoc-core vte-devel
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2
%endif
# RHEL
%if 0%{?rhel_version} >= 500
%define env_options export MONO_SHARED_DIR=/tmp
%define _version %new_split_version
BuildRequires:  gnome-panel-devel gtkhtml3-devel libgnomeprintui22-devel librsvg2-devel mono-devel monodoc-core vte-devel
%endif
#################
##############
### Options that relate to a version of gtk#, not necessarily a distro
# Define true for 2.10 and 2.12
#  (Must do this inside of shell... rpm can't handle this expression)
%define platform_desktop_split %(if test x%_version = x%new_split_version || test x%_version = x%two_twelve_version ; then  echo "1" ; else echo "0" ; fi)
# define true for 2.12.0
%define include_atk_glue %(if test x%_version = x%two_twelve_version  ; then echo "1" ; else echo "0" ; fi )
###
##############
# Need to put this stuff down here after Version: gets defined
Version:        %_version
Release:        9
Source:         %{_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package contains Mono bindings for gtk+, gdk, atk, and pango.



%package gapi
License:        LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        C Source Parser and C Generator
Requires:       perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX

%description gapi
The gtk-sharp-gapi package includes the parser and code generator used
by the GTK if you want to bind GObject-based libraries, or need to
compile a project that uses it to bind such a library.



%package -n gtk-sharp2-doc
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Monodoc documentation for gtk-sharp2
Group:          System/GUI/GNOME
# Disable this for now, as it's a circular dep
#  Works ok in autobuild/buildservice, not so well in monobuild
#Requires:       mono-tools

%description -n gtk-sharp2-doc
This package contains the gtk-sharp2 documentation for monodoc.



%package -n glib-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for glib
Group:          System/GUI/GNOME

%description -n glib-sharp2
This package contains Mono bindings for glib.



%package -n glade-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        Mono bindings for glade

%description -n glade-sharp2
This package contains Mono bindings for glade.



%package -n gtk-sharp2-complete
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        GTK+ and GNOME bindings for Mono (virtual package)
Requires:       glade-sharp2 = %{version}-%{release}
Requires:       glib-sharp2 = %{version}-%{release}
Requires:       gtk-sharp2 = %{version}-%{release}
Requires:       gtk-sharp2-doc = %{version}-%{release}
Requires:       gtk-sharp2-gapi = %{version}-%{release}
%if %platform_desktop_split == 0
Requires:       art-sharp2 = %{version}-%{release}
Requires:       gconf-sharp2 = %{version}-%{release}
Requires:       gnome-sharp2 = %{version}-%{release}
Requires:       gnome-vfs-sharp2 = %{version}-%{release}
Requires:       gtkhtml-sharp2 = %{version}-%{release}
Requires:       rsvg-sharp2 = %{version}-%{release}
Requires:       vte-sharp2 = %{version}-%{release}
%endif

%description -n gtk-sharp2-complete
Gtk# is a library that allows you to build fully native graphical GNOME
applications using Mono. Gtk# is a binding to GTK+, the cross platform
user interface toolkit used in GNOME. It includes bindings for Gtk,
Atk, Pango, Gdk, libgnome, libgnomeui and libgnomecanvas.  (Virtual
package which depends on all gtk-sharp2 subpackages)



%if %platform_desktop_split == 0

%package -n gnome-sharp2
License:        LGPL v2.1 or later
Summary:        Mono bindings for Gnome
Group:          System/GUI/GNOME

%description -n gnome-sharp2
This package contains Mono bindings for Gnome.



%package -n rsvg-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for rsvg
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       librsvg

%description -n rsvg-sharp2
This package contains Mono bindings for librsvg.



%package -n gtkhtml-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       %gtkhtml_requires

%description -n gtkhtml-sharp2
This package contains Mono bindings for gtkhtml.



%package -n gnome-vfs-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gnomevfs
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       gnome-vfs2

%description -n gnome-vfs-sharp2
This package contains Mono bindings gnomevfs.



%package -n art-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for libart
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       libart_lgpl

%description -n art-sharp2
This package contains Mono bindings for libart.



%package -n vte-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte
# Not needed with rpm .config dep search
#Requires:       vte

%description -n vte-sharp2
This package contains Mono bindings for vte.



%package -n gconf-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gconf
Group:          System/GUI/GNOME

%description -n gconf-sharp2
This package contains Mono bindings for gconf and gconf peditors.



%endif
%prep
%setup -q -n %{_name}-%{version}
if [ %version \< 2.10.3 ] ; then
%patch0 -p1
fi
%if %platform_desktop_split == 0
%patch1 -p1
# 2.8.4 and later on 2.8.x branch doesn't need this patch
if [ %version \< 2.8.4 ] ; then
%patch2
fi
%patch3 -p1
%patch4 -p1
%patch5 -p1
%endif
if [ %version \< 2.12 ] ; then
%patch6
fi

%build
%{?env_options}
autoreconf -f -i
# FIXME: windowmanager.c:*: warning: dereferencing type-punned pointer will break strict-aliasing rules
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure\
	--libexecdir=%{_prefix}/lib\
	--enable-debug
make

%install
%{?env_options}
%makeinstall
rm $RPM_BUILD_ROOT%{_libdir}/*.*a
# Special handling for new files
touch %name.files
# atk glue for now...
%define atk_glue %{_libdir}/libatksharpglue-2.so
%if 0%{?include_atk_glue}
echo "%atk_glue" >> %name.files
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.files
%defattr(-, root, root)
%{_libdir}/libgdksharpglue-2.so
%{_libdir}/libgtksharpglue-2.so
%{_libdir}/libpangosharpglue-2.so
%{_libdir}/pkgconfig/gtk-sharp-2.0.pc
%{_libdir}/pkgconfig/gtk-dotnet-2.0.pc
%{_prefix}/lib/mono/gac/*atk-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*atk-sharp.dll
%{_prefix}/lib/mono/gac/*gdk-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gdk-sharp.dll
%{_prefix}/lib/mono/gac/*gtk-dotnet
%{_prefix}/lib/mono/gtk-sharp-2.0/*gtk-dotnet.dll
%{_prefix}/lib/mono/gac/*gtk-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gtk-sharp.dll
%{_prefix}/lib/mono/gac/*pango-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*pango-sharp.dll

%files gapi
%defattr(-, root, root)
%{_bindir}/gapi2-codegen
%{_bindir}/gapi2-fixup
%{_bindir}/gapi2-parser
%{_datadir}/gapi-2.0
%{_libdir}/pkgconfig/gapi-2.0.pc
%{_prefix}/lib/gtk-sharp-2.0/gapi_codegen.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-fixup.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi-parser.exe
%{_prefix}/lib/gtk-sharp-2.0/gapi_pp.pl
%{_prefix}/lib/gtk-sharp-2.0/gapi2xml.pl

%files -n gtk-sharp2-doc
%defattr(-, root, root)
%doc COPYING ChangeLog README
%{_prefix}/lib/monodoc

%files -n glib-sharp2
%defattr(-, root, root)
%{_libdir}/libglibsharpglue-2.so
%{_libdir}/pkgconfig/glib-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*glib-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*glib-sharp.dll

%files -n glade-sharp2
%defattr(-, root, root)
%{_libdir}/libgladesharpglue-2.so
%{_libdir}/pkgconfig/glade-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*glade-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*glade-sharp.dll

%files -n gtk-sharp2-complete
%defattr(-, root, root)
## This is the 'base' package so we put the common dirs of all in this package
# Otherwise, this package doesn't get created!
%dir %{_prefix}/lib/mono/gtk-sharp-2.0
%dir %{_prefix}/lib/gtk-sharp-2.0
##############################################################################
############# FILELIST START of packages split as gnome-sharp ################
%if %platform_desktop_split == 0

%files -n gnome-sharp2
%defattr(-,root,root)
%{_libdir}/libgnomesharpglue-2.so
%{_libdir}/pkgconfig/gnome-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gnome-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gnome-sharp.dll

%files -n rsvg-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/rsvg-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*rsvg-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*rsvg-sharp.dll

%files -n gtkhtml-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/gtkhtml-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gtkhtml-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gtkhtml-sharp.dll

%files -n gnome-vfs-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/gnome-vfs-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gnome-vfs-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gnome-vfs-sharp.dll

%files -n art-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/art-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*art-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*art-sharp.dll

%files -n vte-sharp2
%defattr(-, root, root)
%{_libdir}/libvtesharpglue-2.so
%{_libdir}/pkgconfig/vte-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*vte-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*vte-sharp.dll

%files -n gconf-sharp2
%defattr(-, root, root)
%{_bindir}/gconfsharp2-schemagen
%{_libdir}/pkgconfig/gconf-sharp-2.0.pc
%{_prefix}/lib/gtk-sharp-2.0/gconfsharp-schemagen.exe
%{_prefix}/lib/mono/gac/*gconf-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp.dll
# Other distros place these in gnome-sharp2??
%{_prefix}/lib/mono/gac/*gconf-sharp-peditors
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp-peditors.dll
%endif
############### FILELIST END of packages split as gnome-sharp ################
##############################################################################
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Thu May 08 2008 aj@suse.de
- Fix warnings about missing return.
* Fri Apr 25 2008 wberrier@suse.de
- Update to 2.12.1
  * Bugfix in GLib ref management for Gnome.Program crash in
  gnome-sharp
  * Enhanced Null-terminated string array marshaling
  * Bugfixes for Pango.AttrList
  * Added missing virtual methods and some reference management
  fixes in Atk
  * Bugfix for crash in Gtk.KeySnoopFunc delegate marshaling
  * PrintOperation cairo context reference management fix
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Thu Apr 03 2008 wberrier@suse.de
- Packaging updates to allow building of 2.12.0, and still build
  older versions (for the build service)
- Simplify (hopefully) version choosing for each distro
- Tie differences between gtk# versions to versions and not
  distros
- Update to 2.12.0
 -Memory and Reference Management Improvements
 -Gtk.Object destruction enhancements
 -Revamped the GLib.Object finalization mechanism
 -Better exception handling
 -Structure marshaling
 -GInterface Registration
* Wed Mar 26 2008 wberrier@suse.de
- Remove off_t patch now that it's in 2.10.4
- Update to 2.10.4
 -Various gug fixes, including: bnc #359561
- Changes in 2.10.3:
 -Performance, memory management, and object finalization
  improvements.
 -GLib.ExceptionManager to support exception handling in signal
  callbacks.
 -GLib.IOChannel and GLib.Spawn classes for process spawning.
 -Numerous bugfixes
* Wed Dec 05 2007 sbrabec@suse.cz
- Handle off_t as long (#319824),
* Fri Aug 03 2007 wberrier@suse.de
- Update to bigfix release: 2.10.2
 -Bugfixes: bugzilla.ximian.com:
  -82287, 78524, 79214, 82037, 82098, 82115
- Remove fix_callback_code_generator.patch, as it's been fixed in
  2.10.2
* Sun Jul 15 2007 aj@suse.de
- Add fix_callback_code_generator.patch to fix gapi's code
  generator for callbacks with out parameters (fixes gmime-sharp).
* Tue Jul 03 2007 wberrier@suse.de
- Correct time for May 2 entry (failing on s390 machines)
- Update to 2.10 for distros with gtk 2.10 (currently this is
  opensuse 10.2, 10.3, and fedora 7)
 -Make all subpackages that are in the new gnome-sharp package
  conditional for 2.10 and newer, leave them there for 2.8 and
  older)
 -2.10.1 Changes:
  -Memory leak and other various fixes
 -2.10 Changes:
  -subpackages split between platform/desktop for inclusion into
  Gnome (based on gtk# 2.8.3)
* Sun Jun 17 2007 wberrier@suse.de
- Correct time for May 2 entry (failing on s390 machines)
* Thu May 17 2007 wberrier@novell.com
- make sure vte is installed during suse 10.0 build to resolve
  .config dllmaps
* Fri May 04 2007 wberrier@novell.com
- revert_unportable_relocatable.patch so that the fedora packages
  don't need to depend on the 'which' package
* Thu May 03 2007 wberrier@novell.com
- Use the internally defined deps/reqs since the suse rpm support
  doesn't look for assembly .config files
  (set _use_internal_dependency_generator to 0 on fedora distros)
* Wed May 02 2007 wberrier@novell.com
- Rely on the new .config rpm dep generation for requires for:
  gtkhtml-sharp2
  rsvg-sharp2
  gnome-vfs-sharp2
  vte-sharp2
  (Also simplifies cross distro packaging, mainly suse vs. redhat)
* Thu Apr 26 2007 wberrier@suse.de
- Fix vte .so version in the .config file (fixes bnc #265854)
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Apr 05 2007 wberrier@novell.com
- Adapt for build service, final fix (at least hopefully for a long
  time) for gtkhtml
* Tue Mar 27 2007 sbrabec@suse.cz
- Build with the latest gtkhtml.
* Wed Jan 17 2007 meissner@suse.de
- use RPM_OPT_FLAGS.
* Fri Oct 20 2006 ro@suse.de
- added mono-devel to buildrequires
* Mon Oct 16 2006 schwab@suse.de
- Use install-data-hook instead of install-hook.
* Tue Aug 01 2006 wberrier@suse.de
- Update to 2.8.3
- Fix: Multiple calls to Gnome.Vfs.MimeType.Description triggers glibc error (77534)
* Tue May 09 2006 joeshaw@suse.de
- Add a patch to make GLib.ValueArray actually free in the main
  GTK thread rather than the finalizer thread.  Fixes deadlocks,
  like bnc #168650.
* Tue Feb 28 2006 wberrier@suse.de
- Update to 2.8.2.  Fixes the following bugs: (Ximian)
  - 77497
  - 77662
  - 77658 (64bit fix, needed by f-spot)
  - 154029 in Novell's Bugzilla
* Tue Feb 21 2006 rguenther@suse.de
- Fix build failure on ppc64.  [#152472]
* Thu Feb 16 2006 wberrier@suse.de
- Add .mdb files.  Fixes: https://bugzilla.novell.com/show_bug.cgi?id=151353
 - also, remove the explicit deps (they are provided by mono(assembly) deps
* Thu Feb 09 2006 wberrier@suse.de
- Update to 2.8.1.  Fixes the following bugs (Ximian bugzilla):
 - #77400
 - #77323
 - #77016
 - #76992
 - #77017
 - #77182
 - #77244
* Fri Feb 03 2006 aj@suse.de
- Cleanup BuildRequires.
- Add Requires for packages.
- Reorder spec file sections.
* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 24 2006 wberrier@suse.de
- Additional package splits: art, rsvg, gtkhtml, and gnome-vfs
* Fri Jan 13 2006 wberrier@suse.de
- Redo almost all of the packaging (Novell Bug #142367)
 - split package based on what another distro does
 - clean up nfb a little
 - remove unnecessary hard rpm deps
  - I don't understand why gnome-filesystem would be required?
 - Provide gtk-sharp2-complege virtual package depending on all sub packages
* Wed Jan 11 2006 wberrier@suse.de
- Update to 2.8.0
* Fri Dec 16 2005 wberrier@suse.de
- Update to 2.7.90
* Thu Dec 01 2005 wberrier@suse.de
- Clean up needed for build and install section
* Fri Nov 11 2005 wberrier@suse.de
- Update to 2.7.1
* Thu Oct 06 2005 wberrier@suse.de
- Update to 2.3.92
* Tue Oct 04 2005 gekker@suse.de
- Update to svn snapshot to fix crash when re-sizing windows
- Remove upstreamed patch
* Tue Sep 27 2005 ro@suse.de
- re-enable gtkhtml
* Mon Sep 26 2005 gekker@suse.de
- Fix build on x86_64
* Fri Sep 23 2005 wberrier@suse.de
- updated to 2.3.91.  New version also includes docs for monodoc
* Fri Sep 23 2005 ro@suse.de
- removed libgdiplus-devel from nfb (dropped)
* Sun Sep 04 2005 aj@suse.de
- Add check-build.sh.
* Fri Aug 19 2005 wberrier@suse.de
- Add dependencies on Perl xml packages for gapi (Novell [Bug 105055])
* Mon Jul 11 2005 gekker@suse.de
- fix build with current libgda/libgnomedb
* Wed Jul 06 2005 gekker@suse.de
- Fix to build all optional modules
* Wed Jul 06 2005 gekker@suse.de
- Branch for gtk-sharp2, initial version 1.9.5
* Thu May 19 2005 ro@suse.de
- fix build with current pkgconfig
* Fri May 06 2005 gekker@suse.de
- Fix requires in gtk-sharp to require gtk-sharp-gapi
* Wed Mar 16 2005 gekker@suse.de
- Update to version 1.0.8, leak fixes
- Remove upstreamed patches
* Wed Mar 09 2005 gekker@suse.de
- Update gtkhtml-sharp.diff for new .so version in gtkhtml2
* Tue Mar 08 2005 gekker@suse.de
- add gtkhtml-sharp.diff (66769, 66439)
* Thu Feb 24 2005 gekker@suse.de
- Fix requires (66439)
* Mon Feb 21 2005 clahey@suse.de
- Update to 1.0.6.
* Fri Jan 21 2005 ro@suse.de
- update to 1.0.4
* Fri Jan 14 2005 ro@suse.de
- build with gtkhtml-3.6
* Thu Dec 02 2004 ro@suse.de
- try to fix build on x86_64
* Mon Nov 29 2004 ro@suse.de
- run autoreconf
* Wed Sep 08 2004 joeshaw@suse.de
- Update the gtkhtml patch.
* Tue Sep 07 2004 joeshaw@suse.de
- Add a patch to use gtkhtml 3.1 instead of 3.0.  Ximian #63188
* Sat Sep 04 2004 clahey@suse.de
- Updated to 1.0.
* Tue Jun 29 2004 ro@suse.de
- use rpm scripts for find requires/provides
* Tue Jun 22 2004 clahey@suse.de
- Updated to 0.98.
* Wed May 26 2004 clahey@suse.de
- Initial import.
