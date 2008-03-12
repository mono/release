
%define db_packages mono-data-postgresql mono-data-sqlite mono-data-sybase 

# norootforbuild

Name:     	monodevelop-database
Version: 	1.0
Release:	0
Vendor:		Novell, Inc.
License:	LGPL
BuildRoot:	/var/tmp/%{name}-%{version}-root
Autoreqprov:    on
BuildArch:      noarch
URL:		http://www.monodevelop.com
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	mono-devel monodevelop %db_packages
Requires:	%db_packages
BuildRequires:	bytefx-data-mysql
Summary:	Monodevelop Database Addin
Group:		Development/Tools

%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-sharp2 monodoc-core
%endif

%description
Monodevelop Database Addin
	  
%files -f %{name}.lang
%defattr(-, root, root)
%_prefix/share/pkgconfig/monodevelop-database.pc
%_prefix/lib/monodevelop/AddIns/MonoDevelop.Database/*.dll
%dir %_prefix/lib/monodevelop/AddIns/MonoDevelop.Database
%dir %_prefix/lib/monodevelop/AddIns/MonoDevelop.Database/locale

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

%find_lang %{name}

%clean
rm -rf "$RPM_BUILD_ROOT"

%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
