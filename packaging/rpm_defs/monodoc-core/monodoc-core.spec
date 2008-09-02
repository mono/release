#
# spec file for package monodoc-core (Version 2.0)
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


Name:           monodoc-core
License:        GPL v2 or later
Group:          Development/Tools/Other
Summary:        Monodoc--A Documentation Browser Written in C#
Url:            http://go-mono.org/
Version:        2.0
Release:        1
Source0:        monodoc-%version.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       monodoc
Obsoletes:      monodoc
BuildArch:      noarch
BuildRequires:  mono-devel unzip
#####  suse  ####
%if 0%{?suse_version}
%define old_suse_buildrequires mono-web
%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Monodoc is a documentation browser for the Mono project. It is written
in C# using the GTK# libraries.



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

%prep
%setup -n monodoc-%{version} -q

%build
%{?env_options}
./configure \
  --prefix=/usr \
  --libdir=%{_prefix}/lib \
  --libexecdir=%{_prefix}/lib \
  --localstatedir="%{_localstatedir}" \
  --mandir=%{_mandir} \
  --infodir=/usr/share/info \
  --sysconfdir=%{_sysconfdir}
make

%install
%{?env_options}
make DESTDIR="$RPM_BUILD_ROOT" install
install -d $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig $RPM_BUILD_ROOT/usr/share
rm -f $RPM_BUILD_ROOT/usr/lib/monodoc/sources/gtk-sharp-docs.tree
rm -f $RPM_BUILD_ROOT/usr/lib/monodoc/sources/gtk-sharp-docs.zip

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/monodoc
%{_prefix}/lib/mono/monodoc
%{_bindir}/*
%{_prefix}/lib/monodoc
%{_prefix}/share/pkgconfig/monodoc.pc
%{_mandir}/man1/*
%{_mandir}/man5/*
# Should be in mono-tools now...?
#%{_prefix}/share/applications/monodoc.desktop
#%{_prefix}/share/pixmaps/monodoc.png
%doc AUTHORS ChangeLog NEWS README
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0
  * Documentation fixes and updates to match mono 2.0
* Tue Mar 25 2008 wberrier@suse.de
- Update to 1.9
 -Documentation fixes and updates to match mono 1.9
* Mon Jan 14 2008 wberrier@suse.de
- Update to 1.2.6
 -Documentation updates to match mono 1.2.6
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -Documentation updates to match mono 1.2.5
 -several improvements and fixes to 'monodocer' utility
* Wed Jun 06 2007 wberrier@novell.com
- Update to 1.2.4
 -Documentation updates to match mono 1.2.4
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Mar 01 2007 wberrier@suse.de
- Update to 1.2.3
 -API Documentation updates
 -Formatting fixes
 -Sub documentation for 2.0 APIs
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.1 (Fate #301111)
 -Sqlite Docs update
 -new manpages
 -doc generation updates and fixes
* Fri Oct 20 2006 wberrier@suse.de
- Update to 1.1.18
 -generics support and will display generic types
 -documents custom attributes with their actual constructor calls
 -monodocs2html now includes inherited members on type pages
* Thu Oct 19 2006 wberrier@suse.de
- Remove manual Requires.  mono-devel isn't needed, and all other
  deps will be generated automatically. (bnc #212972)
* Wed Aug 30 2006 wberrier@suse.de
- Update to 1.1.17
 - Updated documentation for mono 1.1.17
* Mon Jul 31 2006 wberrier@suse.de
- Update to 1.1.16
- Fixes problem with missing documentation (pathnames too long
  for a tar.gz file)
- Append the node kind to the node caption. Fixes a crash when
  editing uncompiled help sources.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jan 11 2006 ro@suse.de
- added mono-devel to nfb to get monoized provides
* Fri Jan 06 2006 wberrier@suse.de
- Update to 1.1.13, clean up deps
* Thu Dec 15 2005 wberrier@suse.de
- Update to 1.1.11, remove run_ldconfig
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10, remove icu deps
* Fri Oct 07 2005 wberrier@suse.de
- Update to 1.1.9
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Sun Sep 25 2005 ro@suse.de
- fix file-conflict with gtk-sharp2
* Fri Aug 26 2005 wberrier@suse.de
- renmae package to monodoc-core
* Mon Aug 15 2005 ro@suse.de
- added check-build.sh
* Thu Aug 11 2005 ro@suse.de
- fix last change
* Thu Aug 11 2005 ro@suse.de
- moved pkgconfig file to /usr/share (noarch package)
* Wed Aug 10 2005 ro@suse.de
- keep monodoc script until we have a mono-tools package
* Tue Aug 09 2005 gekker@suse.de
- Update to version 1.0.7
- Remove upstreamed patches
* Mon Jul 18 2005 dkukawka@suse.de
- changed package to noarch
* Tue Feb 22 2005 ro@suse.de
- fix build on x86_64
* Mon Feb 21 2005 clahey@suse.de
- Update to 1.0.6.
* Sun Feb 06 2005 ro@suse.de
- adapt pc-file
* Thu Jan 20 2005 ro@suse.de
- fix build on lib64
* Fri Dec 03 2004 dkukawka@suse.de
- fix libexecdir, now all {libdir}/monodoc files now at /usr/lib
  instead of /usr/lib64 (with symlink)
* Fri Dec 03 2004 ro@suse.de
- removed wrong re-definitions of find_{requires,provides}
* Tue Nov 30 2004 dkukawka@suse.de
- init
