#
# spec file for package nant (Version 0.86_beta1)
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


Name:           nant
# We have to append a .0 to make sure the rpm upgrade versioning works.
#  nant's progression: 0.85-rc4, 0.85
#  working rpm upgrade path requires: 0.85-rc4, 0.85.0
Version:        0.86_beta1
Release:        37
License:        GPL v2 or later; LGPL v2.1 or later
BuildArch:      noarch
Url:            http://nant.sourceforge.net
Source0:        %{name}-0.86-beta1-src.tar.gz
Patch0:         nant-useruntime_fix.patch
Patch1:         nant-bootstrap.patch
Summary:        Ant for .NET
Group:          Development/Tools/Building
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# Only needed when building from prefer rpms (normally mono-devel depends on glib2-devel)
BuildRequires:  glib2-devel
BuildRequires:  mono-data mono-devel pkgconfig
####  suse  ####
%if 0%{?suse_version}
%define old_suse_buildrequires mono-winforms mono-web
%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%define env_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.



Authors:
--------
    Gerry Shaw

%files
%defattr(-, root, root)
%{_bindir}/nant
%{_datadir}/NAnt

%prep
%setup  -q -n %{name}-0.86-beta1
%patch0 -p1
%patch1

%build
%{?env_options}
make

%install
%{?env_options}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}
# Fix script (doesn't properly support prefix)
cat <<EOF > $RPM_BUILD_ROOT%{_prefix}/bin/nant
#!/bin/sh
exec %{_prefix}/bin/mono %{_prefix}/share/NAnt/bin/NAnt.exe "\$@"
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/nant

%clean
rm -rf "$RPM_BUILD_ROOT"
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
# ignore some bundled dlls
%define __find_provides env sh -c 'filelist=($(grep -v log4net.dll | grep -v scvs.exe | grep -v nunit | grep -v NDoc | grep -v neutral)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 12 2008 ajorgensen@novell.com
- Patch to allow us to bootstrap nant on mono-2.0
* Mon Dec 10 2007 wberrier@suse.de
- Update to 0.86_beta1
 -modify filelist munging to work for this release
 -remove patches: nant-1733671_threading_fix.patch
  nant-remove_overridden_obsolete.patch
 -new patch: nant-useruntime_fix.patch
-Ignore some bundled assemblies
* Mon Aug 06 2007 wberrier@suse.de
- Use upstream threading fix instead of workaround
  (remove nant-remove_pkgconfig_garbage.patch and replace with
  nant-1733671_threading_fix.patch)  This will fix other issues
  with nant as well.
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Fri Mar 30 2007 wberrier@suse.de
- Truely make noarch (don't use prefix var from runtime,
  because it could be '/usr/lib/pkgconfig/../..', and if this
  doesn't exists on x86_64, the nant script will fail.
- Use 'exec' in nant wrapper
* Tue Mar 06 2007 wberrier@suse.de
- nant-remove_overridden_obsolete.patch: mcs >= 1.2.3 doesn't allow
  obsolete overrides for non-obsolete methods.  future versions of
  csc will warn about this.
* Mon Nov 20 2006 wberrier@suse.de
- nant-remove_pkgconfig_garbage.patch: fix random builds failures
  of nant and boo (mostly on 64bit archs).  Workaround for now...
* Fri Oct 27 2006 dmueller@suse.de
- don't build as root
* Tue Oct 24 2006 wberrier@suse.de
- Updated to 0.85, fixed some inconsistent build errors on
  x86_64 and ia64 about invalid path chars on path::combine
 - had to append .0 to version to make sure rpm upgrades work
* Tue Aug 01 2006 wberrier@suse.de
- Initial package: 0.85-rc4
