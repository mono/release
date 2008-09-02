#
# spec file for package monodevelop-java (Version 1.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           monodevelop-java
Version:        1.0
Release:        1
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.monodevelop.com
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  ikvm mono-devel monodevelop
Requires:       ikvm
Summary:        Monodevelop Java Addin
Group:          Development/Languages/Mono
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-sharp2 monodoc-core
%endif

%description
Java language integration with MonoDevelop based on ikvm.



%files -f %{name}.lang
%defattr(-, root, root)
%_prefix/share/pkgconfig/monodevelop-java.pc
%_prefix/lib/monodevelop/AddIns/JavaBinding/JavaBinding.dll*
%dir %_prefix/lib/monodevelop/AddIns/JavaBinding
%dir %_prefix/lib/monodevelop/AddIns/JavaBinding/locale

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
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Wed Mar 26 2008 wberrier@novell.com
- Update to 1.0
 -Updated translations
 -Minor fixes to coincide with the MonoDevelop 1.0 release
* Tue Jan 15 2008 wberrier@suse.de
- Initial package (split out from monodevelop at the source level)
