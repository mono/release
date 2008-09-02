#
# spec file for package monodevelop-database (Version 1.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

%define db_packages mono-data-postgresql mono-data-sqlite mono-data-sybase 

Name:           monodevelop-database
Version:        1.0
Release:        1
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.monodevelop.com
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  %db_packages mono-devel monodevelop
Requires:       %db_packages
BuildRequires:  bytefx-data-mysql
Summary:        Monodevelop Database Addin
Group:          Development/Languages/Mono
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-sharp2 monodoc-core
%endif

%description
Addin for MonoDevelop for an integrated database explorer and editor.



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
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(grep -v "Mono.Data.Sqlite\\|MySql.Data")) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Wed Mar 26 2008 wberrier@novell.com
- Update to 1.0:
 -Updated translations
 -Bug Fixes:
  - Database browser: Tables do not render columsn (bnc#339726)
* Tue Jan 15 2008 wberrier@suse.de
- Initial package (split out from monodevelop at the source level)
