#
# spec file for package gecko-sharp2 (Version 0.13)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           gecko-sharp2
BuildRequires:  gtk-sharp2 gtk-sharp2-gapi gtk2-devel mono-devel monodoc-core
Version:        0.13
Release:        1
License:        LGPL v2.1 or later; MOZILLA PUBLIC LICENSE (MPL/NPL)
BuildArch:      noarch
Url:            www.monodevelop.com
Source0:        gecko-sharp-2.0-%{version}.tar.bz2
Summary:        Gecko bindings for Mono
Group:          Development/Libraries/Other
Provides:       gecko-sharp-2_0 gecko-sharp2-docs gecko-sharp-2.0
Obsoletes:      gecko-sharp-2_0 gecko-sharp2-docs gecko-sharp-2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
# To share the rpms in monobuild, ignore the .config from scanning
%define requires_list cat
%if 0%{?monobuild} == 01
%define requires_list grep -v gecko-sharp.dll.config
%endif
%define xulrunner_version 181
%if 0%{?suse_version}
%if %suse_version >= 1020
BuildRequires:  mozilla-xulrunner%{xulrunner_version}
# not needed with the .config scanning
#Requires:       mozilla-xulrunner%{xulrunner_version}
%endif
%if %suse_version == 1010
BuildRequires:  mozilla-xulrunner
# not needed with the .config scanning
#  Turns out it is needed, otherwise build system doesn't know whether satisfy the dep with
#  xulrunner or seamonkey.
Requires:       mozilla-xulrunner
%endif
%if %suse_version <= 1000
BuildRequires:  mozilla
# not needed with the .config scanning
#Requires:       mozilla
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
# Only needed to resolve libgtkembedmoz.so at mono-find-requires time
%if %fedora_version <= 5
BuildRequires:  mozilla
%endif
%if %fedora_version >= 6
BuildRequires:  firefox
%endif
%endif

%description
This package provides Mono bindings for the Gecko engine, through an
easy-to-use widget that will allow you to embed a Mozilla browser
window into your Gtk# application.



Authors:
--------
    John Luke <jluke@cfl.rr.com>
    Mark Crichton <crichton@gimp.org>
    Mike Kestner <mkestner@ximian.com>
    Todd Berman <tberman@sevenl.net>
    Geoff Norton <gnorton@customerdna.com>
    Raja R Harinath <rharinath@novell.com>
    Zac Bowling <zac@zacbowling.com>
    Christian Hergert <christian.hergert@gmail.com>
    Alp Toker <alp@atoker.com>
    Ben Maurer <bmaurer@ximian.com>

%prep
%setup  -q -n gecko-sharp-2.0-%{version}

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var

%install
%{?env_options}
make install DESTDIR=%{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/share/pkgconfig

%clean
rm -rf "%{buildroot}"

%files
%defattr(-, root, root)
/usr/lib/mono/gecko-sharp-2.0
/usr/lib/mono/gac/gecko-sharp
/usr/share/pkgconfig/*.pc
/usr/lib/monodoc/sources/*
# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(%requires_list)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Wed Mar 26 2008 ajorgensen@novell.com
- Update to 0.13
- Fixes bnc#341815 - [Regression] Monodoc crashes in gtk_moz_embed_append_data
* Sat Jul 07 2007 wberrier@novell.com
- Update to 0.12
 -Depend on monodoc-core instead of mono-tools to break cyclic dep
 -Resolve naming conflicts in automake files
 -Remove upstreamed patches:
  gecko-sharp2-r69353_break_cyclic_dep.patch
  gecko-sharp2-r69372_fix_autoconf_docdir.patch
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Jan 04 2007 wberrier@suse.de
- obsolete gecko-sharp2-docs for upgrade path
 -bnc #227363
* Tue Dec 12 2006 wberrier@suse.de
- Undo gecko-sharp2 doc package split.
 -gecko-sharp2-r69353_break_cyclic_dep.patch: Patch to depend on
  monodoc-core instead of mono-tools to break cyclic dep
 -gecko-sharp2-r69372_fix_autoconf_docdir.patch: now that we use
  autoreconf for the above patch, we must rename docdir to
  monodocdir so docdir doesn't get overwritten
* Thu Nov 30 2006 sbrabec@suse.cz
- Fixed xulrunner dependencies for older products.
* Tue Nov 14 2006 ro@suse.de
- remove mono-tools from buildrequires and build docs in separate
  specfile to break cycle between mono-tools and gecko-sharp2
* Mon Nov 13 2006 sbrabec@suse.cz
- Use exact xulrunner version 181 (#218792, #216100).
* Fri Oct 20 2006 ro@suse.de
- added mono-devel to buildrequires
* Fri Jul 07 2006 lrupp@suse.de
- Requires mozilla-xulrunner180 for %%suse_version > 1010
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 13 2006 gekker@suse.de
- Fixup nfb and Requires for new gtk-sharp2 packaging
* Fri Dec 09 2005 wberrier@suse.de
- Replace mozilla dep with mozilla-xulrunner, clean up deps, and
  add documentation
* Fri Oct 21 2005 ro@suse.de
- rename package, provide and obsolete old name
* Sat Oct 08 2005 wberrier@suse.de
- Update to 0.11
* Mon Aug 15 2005 ro@suse.de
- added check-build.sh
* Tue Aug 09 2005 lnussel@suse.de
- use buildroot and build as user
* Mon Aug 08 2005 ro@suse.de
- fix location of pkgconfig file
* Mon Aug 08 2005 ro@suse.de
- rename package to gecko-sharp-2_0 (no "." allowed in name)
* Thu Aug 04 2005 wberrier@suse.de
- Initial package
