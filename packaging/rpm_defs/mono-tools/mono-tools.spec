#
# spec file for package mono-tools (Version 2.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           mono-tools
BuildRequires:  gconf-sharp2 gecko-sharp2 mono-data-oracle mono-devel mono-jscript mono-nunit monodoc-core
Version:        2.0
Release:        1
License:        GPL v2 or later
BuildArch:      noarch
Url:            http://go-mono.org/
Source0:        %{name}-%{version}.tar.bz2
Summary:        Collection of Tools and Utilities for Mono
Group:          Development/Tools/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
%if %suse_version >= 1030
BuildRequires:  gtkhtml314-sharp
%else
BuildRequires:  gtkhtml-sharp2
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
# Not sure of the equivalent for fedora...
%define suse_update_desktop_file true
%if %fedora_version >= 8
BuildRequires:  gtkhtml314-sharp
%else
BuildRequires:  gtkhtml-sharp2
%endif
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%define suse_update_desktop_file true
BuildRequires:  gtkhtml-sharp2
%endif

%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Duncan Mak <duncan@ximian.com>
    Joshua Tauberer <tauberer@for.net>
    Lee Malabone
    Philip Van Hoof
    Johannes Roith <johannes@jroith.de>
    Alp Toker <alp@atoker.com>
    Piers Haken
    John Luke <jluke@cfl.rr.com>
    Ben Maurer
    Duncan Mak <duncan@ximian.com>
    Sebastien Pouliot <sebastien@ximian.com>

%files -f %{name}.lang
%defattr(-, root, root)
%_bindir/*
%_datadir/applications/gendarme-wizard.desktop
%_datadir/applications/gsharp.desktop
%_datadir/applications/ilcontrast.desktop
%_datadir/applications/monodoc.desktop
%_datadir/applications/mprof-heap-viewer.desktop
%_datadir/create-native-map
%_datadir/pixmaps/gendarme.svg
%_datadir/pixmaps/ilcontrast.png
%_datadir/pixmaps/monodoc.png
%_datadir/pkgconfig/create-native-map.pc
%_datadir/pkgconfig/gendarme-framework.pc
%_mandir/man1/create-native-map*
%_mandir/man1/gendarme*
%_mandir/man1/mperfmon*
%_mandir/man1/mprof-decoder*
%_mandir/man1/mprof-heap-viewer*
%_prefix/lib/create-native-map
%_prefix/lib/gendarme
%_prefix/lib/gsharp
%_prefix/lib/gui-compare
%_prefix/lib/ilcontrast
%_prefix/lib/mono-tools
%_prefix/lib/mono/1.0
%_prefix/lib/mono/2.0
%_prefix/lib/monodoc
%_prefix/lib/mperfmon

%prep
%setup  -q -n %{name}-%{version}

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var --enable-monowebbrowser

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
%suse_update_desktop_file -N "Mono Documentation" -G "Documentation Library" -C "Learn about using Mono" monodoc Development Documentation
%suse_update_desktop_file -N "Mono IL Contrast" -G "Development Tools" -C "Contrast Assemblies" ilcontrast Development Documentation
# Move create-native-map stuff out of lib into share
mkdir $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/create-native-map/MapAttribute.cs $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/pkgconfig $RPM_BUILD_ROOT/%_prefix/share
%find_lang %{name}

%clean
rm -Rf "$RPM_BUILD_ROOT"

%post
monodoc --make-index
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0
  * Gendarme
  * New wizard-based GUI runner. It also add support for .MDB and .PDB debugging symbols, allowing source lines numbers inside reports.
  * 151 rules (56 new and many updated) divided into 14 categories (2 new) and yet is faster than the version shipped with Mono 1.9
  * Various updates and fixes to other tools
* Thu Apr 10 2008 wberrier@novell.com
- Update BuildRequires on suse 10.3/11 and fedora8 to use
  the new gtkhtml314-sharp
* Wed Mar 26 2008 wberrier@novell.com
- Update to 1.9:
 -Includes new tools: gui-compare and Gendarme
 -Fix to check for new version of gtkhtml# (3.14)
 -Fixed docbrowser to work with gecko# again
  [Regression] Monodoc crashes in gtk_moz_embed_append_data
  (bnc#341815)
* Tue Feb 26 2008 wberrier@novell.com
- Add patch: mono-tools-fix_build_gnome_sharp.patch
  to fix build with new gtk#/gnome#
* Mon Jan 14 2008 wberrier@novell.com
- Update to 1.2.6
 -Always uses gtkhtml instead of xulrunner, which crashes
 -Various bug fixes
- Patch desktop files: mono-tools-desktop_standards.patch
- use find_lang for translation files
* Wed Jun 06 2007 wberrier@novell.com
- add post script to index documentation
- Update to 1.2.4
 -ilcontast: new util
 -create-native-map updates
 -docbrowser updates
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Apr 05 2007 wberrier@suse.de
- Adapt for buildservice
- Clean up BuildRequires
* Thu Mar 01 2007 wberrier@suse.de
- Update to 1.2.3
 -Adds --remote-mode used in conjuction with MonoDevelop
 -More lenient create-native-map
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.1 (Fate #301111)
 -New create-native-map tools
 -fix for monodoc to work with xulrunner in some cases
* Thu Oct 19 2006 ro@suse.de
- added mono-devel to buildrequires
* Wed Oct 04 2006 wberrier@suse.de
- Update to 1.1.17
  - Uses gtk-sharp2 instead of gtk-sharp.  Update BuildRequires
  accordingly
* Fri Feb 17 2006 gekker@suse.de
- Update .desktop file for UI team
* Wed Feb 01 2006 aj@suse.de
- Fix BuildRequires to build on x86-64 again.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 23 2006 gekker@suse.de
- fixup nfb for changes in gtk-sharp packaging
* Thu Dec 15 2005 wberrier@suse.de
- Update to 1.1.11
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10, add gecko-sharp dep
* Sun Oct 23 2005 ro@suse.de
- do not obsolete monodoc (already provided and obsoleted
  by monodoc-core)
* Tue Oct 11 2005 wberrier@suse.de
- Update to 1.1.9 and enable 2.0
* Fri Aug 26 2005 aj@suse.de
- Fix filelist.
* Fri Aug 26 2005 ro@suse.de
- nfb: monodoc -> monodoc-core
* Tue Aug 23 2005 wberrier@suse.de
- Initial package (Needed for monodoc gtk browser)
