Name:           mono-addins
Version:        0.5
Release:        7
License:        X11/MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.mono-project.com
Source0:        http://ftp.novell.com/pub/mono/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  gtk-sharp2 mono-devel
BuildRequires:  pkg-config
Summary:        Mono Addins Framework
Group:          Development/Languages/Mono
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Mono.Addins is a generic framework for creating extensible
applications, and for creating libraries which extend those
applications.



Authors:
--------
    Lluis Sanchez Gual  <lluis@novell.com>

%files
%defattr(-, root, root)
%_datadir/pkgconfig/*.pc
%_mandir/man1/mautil.1.gz
%_prefix/bin/mautil
%_prefix/lib/mono/gac/*Mono.Addins*
%_prefix/lib/mono/mono-addins
%_prefix/lib/mono/xbuild/Mono.Addins.targets

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%_prefix
make

%install
%{?env_options}
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%_prefix/share/pkgconfig
mv $RPM_BUILD_ROOT%_prefix/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%_prefix/share/pkgconfig

%clean
rm -rf "$RPM_BUILD_ROOT"
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
