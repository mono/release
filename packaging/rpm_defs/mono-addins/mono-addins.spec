
# norootforbuild

Name:     	mono-addins
Version: 	0.3.1
Release:	0
Vendor:		Novell, Inc.
License:	LGPL
BuildRoot:	/var/tmp/%{name}-%{version}-root
Autoreqprov:    on
BuildArch:      noarch
URL:		http://www.go-mono.com
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	mono-devel gtk-sharp2
Summary:	Mono Addins Framework
Group:		Development/Tools

%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif


%description
Mono.Addins is a generic framework for creating extensible applications,
and for creating libraries which extend those applications.
	  

%files
%defattr(-, root, root)
%dir %_prefix/lib/mono/mono-addins

%_prefix/bin/mautil
%_prefix/lib/mono/mono-addins/mautil.exe

%_prefix/lib/mono/gac/Mono.Addins
%_prefix/lib/mono/gac/policy.0.2.Mono.Addins
%_prefix/lib/mono/mono-addins/Mono.Addins.dll

%_prefix/lib/mono/gac/Mono.Addins.Setup
%_prefix/lib/mono/gac/policy.0.2.Mono.Addins.Setup
%_prefix/lib/mono/mono-addins/Mono.Addins.Setup.dll

%_prefix/lib/mono/gac/Mono.Addins.Gui
%_prefix/lib/mono/gac/policy.0.2.Mono.Addins.Gui
%_prefix/lib/mono/mono-addins/Mono.Addins.Gui.dll
%_prefix/share/pkgconfig/*.pc

%debug_package
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
