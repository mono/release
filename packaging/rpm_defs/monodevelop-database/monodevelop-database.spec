
%define db_packages mono-data-postgresql mono-data-sqlite mono-data-sybase 

# norootforbuild

Name:     	monodevelop-database
Version: 	0.17
Release:	0
Vendor:		Novell, Inc.
License:	LGPL
BuildRoot:	/var/tmp/%{name}-%{version}-root
Autoreqprov:    on
BuildArch:      noarch
URL:		http://www.go-mono.com
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	mono-devel monodevelop %db_packages
Requires:	%db_packages
BuildRequires:	bytefx-data-mysql
Summary:	Monodevelop Database Addin
Group:		Development/Tools

%description
Monodevelop Database Addin
	  
%files
%defattr(-, root, root)
%_prefix/share/pkgconfig/monodevelop-database.pc
%_prefix/lib/monodevelop/AddIns/MonoDevelop.Database/*.dll
%_prefix/lib/monodevelop/AddIns/MonoDevelop.Database/locale/*/LC_MESSAGES/monodevelop-database.mo

%prep
%setup -q

%build
./configure --prefix=%_prefix
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%_prefix/share/pkgconfig
mv $RPM_BUILD_ROOT%_prefix/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%_prefix/share/pkgconfig

%clean
rm -rf "$RPM_BUILD_ROOT"

# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog
