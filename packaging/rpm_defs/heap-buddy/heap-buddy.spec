#
# spec file for package heap-buddy (Version 0.2)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

Name:           heap-buddy
License:        GNU General Public License (GPL)
Group:          Development/Tools/Other
Autoreqprov:    on
Version:        0.2
Release:        41
Summary:        Heap-buddy is a heap profiler for mono
URL:            http://www.mono-project.com/
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  mono-devel
# For sles9...
%define configure_options true
BuildRequires:  pkgconfig
%if 0%{?sles_version}
%if %sles_version == 9
%define configure_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
BuildRequires:  pkgconfig
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Heap-buddy is a heap profiler for mono.  It attaches to special hooks
in the mono runtime and tracks all of the managed memory allocations,
every garbage collection and every heap resize.  These statistics are
written out into a data file that we call an 'outfile'.



Authors:
--------
    Ben Maurer      <bmaurer@ximian.com>
    Jon Trowbridge  <trow@novell.com>

%prep
%setup -q

%build
%{?env_options}
%{configure_options}
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%_prefix \
    --libdir=%_libdir
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libmono-profiler-heap-buddy.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS NEWS README COPYING
%{_prefix}/bin/heap-buddy
%{_libdir}/heap-buddy
%{_libdir}/libmono-profiler-heap-buddy.so*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Fri Apr 13 2007 - wberrier@novell.com
- adapt for build service
* Wed Apr 11 2007 - wberrier@novell.com
- Add mono dep/req for older distros
* Tue Dec 05 2006 - joeshaw@suse.de
- Update heap-buddy to 0.2
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Dec 19 2005 - ro@suse.de
- added missing symlink to filelist
* Fri Dec 16 2005 - wberrier@suse.de
- Clean up deps (most mono packages don't need the full gnome-devel dep)
* Fri Dec 02 2005 - gekker@suse.de
- Fix directory ownership
* Thu Dec 01 2005 - gekker@suse.de
- Initial import into autobuild, version 0.1
