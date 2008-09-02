#
# spec file for package gtksourceview-sharp2 (Version 0.12)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           gtksourceview-sharp2
BuildRequires:  gnome-sharp2 gtk-sharp2-gapi gtksourceview-devel mono-devel monodoc-core
Version:        0.12
Release:        1
License:        GPL v2 or later
BuildArch:      noarch
Url:            http://www.go-mono.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         gtksourceview-sharp-2.0-%{version}.tar.bz2
Summary:        GtkSourceView bindings for Mono
Group:          Development/Libraries/Other
# Not needed with auto deps
#Requires:       gtksourceview >= 1.0 glib-sharp2 gnome-sharp2
Provides:       gtksourceview-sharp-2_0
Obsoletes:      gtksourceview-sharp-2_0
AutoReqProv:    on
# suse's gnome went from /opt/gnome to /usr, act accordingly
%define gtksourceview_prefix %(pkg-config --variable=prefix gtksourceview-1.0)
%if 0%{?suse_version}
%if %suse_version >= 1030
BuildRequires:  -gtksourceview-devel gtksourceview18-devel
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
This package provides Mono bindings for GtkSourceView, a child of the
GTK+ text widget which implements syntax highlighting and other
features typical of a source editor.



Authors:
--------
    Martin Willemoes Hansen <mwh@sysrq.dk>
    John Luke <jluke@cfl.rr.com>
    Todd Berman <tberman@sevenl.net>
    Pawel Rozanski <tokugawa@afn.no-ip.org>
    Mike Kestner <mkestner@speakeasy.net>

%prep
%setup  -n gtksourceview-sharp-2.0-%{version} -q

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/gtksourceview-sharp-2.0.pc $RPM_BUILD_ROOT/usr/share/pkgconfig
rm -f $RPM_BUILD_ROOT%{gtksourceview_prefix}/share/gtksourceview-1.0/language-specs/nemerle.lang
rm -f $RPM_BUILD_ROOT%{gtksourceview_prefix}/share/gtksourceview-1.0/language-specs/vbnet.lang

%clean
rm -Rf ${DESTDIR}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README
%{_prefix}/lib/mono/gac/gtksourceview-sharp
%{_prefix}/lib/mono/gtksourceview-sharp-2.0
%{_prefix}/share/pkgconfig/gtksourceview-sharp-2.0.pc
%{_prefix}/share/gapi-2.0/gtksourceview-api.xml
%{_prefix}/lib/monodoc/sources/gtksourceview-sharp-docs*
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Feb 26 2008 wberrier@novell.com
- Update to 0.12 (new gtk# requires this version)
* Thu Aug 16 2007 wberrier@suse.de
- add noarch again (even though this package depends on binary
  libraries, the package itself contains no architecture
  dependant code, and can run on any platform where mono runs)
- Update to use gtksourceview18 package (this package hasn't been
  ported to use 1.9 yet)
* Tue Jun 12 2007 ro@suse.de
- remove noarch: this package depends on binary libraries
* Wed Jun 06 2007 wberrier@novell.com
- remove upstream patch (also remove autoreconf, since there's
  no patches)
- Update to 0.11
 -removes circular dependency on 'monodoc' in mono-tools
 -updated samples
* Wed May 16 2007 wberrier@novell.com
- Fix BuildRequires for suse 10.0 (so .config can be resolved)
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Fri Apr 06 2007 wberrier@novell.com
- Adapt for buildservice, add monodoc patch so only monodoc-core
  is needed, not mono-tools. Clean up BuildRequires some more.
* Mon Feb 12 2007 aj@suse.de
- Remove unneeded BuildRequires.
* Wed Jan 24 2007 ro@suse.de
- GNOME moved to /usr
* Thu Oct 19 2006 ro@suse.de
- added mono-devel to buildrequires
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 13 2006 gekker@suse.de
- Fixup nfb and Requires for new gtk-sharp2 packaging
* Wed Nov 16 2005 wberrier@suse.de
- Remove icu deps
* Thu Oct 20 2005 ro@suse.de
- rename package, provide and obsolete old name
* Thu Sep 22 2005 ro@suse.de
- added norootforbuild
* Wed Sep 21 2005 wberrier@suse.de
- Use the buildroot and package the docs for monodoc (bug #116196)
* Fri Sep 16 2005 wberrier@suse.de
- Only package correct files (Bug #116196)
* Fri Aug 26 2005 ro@suse.de
- nfb: monodoc -> monodoc-core
* Mon Aug 15 2005 aj@suse.de
- Require 2.6.13 or newer kernel.
* Sun Aug 14 2005 aj@suse.de
- Add check-build.sh script.
* Sun Aug 07 2005 ro@suse.de
- fix location of pkgconfig files
* Sun Aug 07 2005 ro@suse.de
- rename package to gtksourceview-sharp-2_0 (no "." allowed in name)
* Thu Aug 04 2005 wberrier@suse.de
- Initial package
