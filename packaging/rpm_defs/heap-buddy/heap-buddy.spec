
# norootforbuild

Name:           heap-buddy
License:        GNU General Public License (GPL)
Group:          Development/Tools/Other
Autoreqprov:    on
Version:        0.2
Release:        1
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
BuildRequires: pkgconfig
%endif
%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
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

%debug_package
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
