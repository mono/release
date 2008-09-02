#
# spec file for package monodevelop-boo (Version 1.0)
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

%define boo_version %(rpm -q boo-devel --queryformat '%{VERSION}')

Name:           monodevelop-boo
Version:        1.0
Release:        73
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.monodevelop.com
Source0:        %{name}-%{version}.tar.gz
Patch0:         shell-properties.patch
BuildRequires:  boo-devel mono-devel monodevelop
Summary:        Monodevelop Boo Addin
Group:          Development/Languages/Mono
# Boo's assemblies are always version at 1.0.0.0.  Force built against or newer.
Requires:       boo-devel >= %boo_version
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-sharp2 monodoc-core
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Boo language integration with Mono develop.  Supports syntax
highlighting and code completion.



%files -f %{name}.lang
%defattr(-, root, root)
%_prefix/share/pkgconfig/monodevelop-boo.pc
%_prefix/lib/monodevelop/AddIns/BooBinding/BooShell.dll*
%_prefix/lib/monodevelop/AddIns/BooBinding/BooBinding.dll*
%dir %_prefix/lib/monodevelop/AddIns/BooBinding
%dir %_prefix/lib/monodevelop/AddIns/BooBinding/locale

%prep
%setup -q
%patch0

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
* Tue Aug 12 2008 ajorgensen@novell.com
- BuildRequire boo-devel
* Wed Mar 26 2008 wberrier@novell.com
- Update to 1.0:
 -updated translations
 -Bug fixes:
  - Boo templates syntactically incorrect (bnc#350626)
  - Boo library template fails to compile (bnc#358368)
  - Boo Code Completion appends instead of replaces what you've
  typed (bnc#361267)
* Tue Jan 15 2008 wberrier@suse.de
- Initial package (split out from monodevelop at the source level)
