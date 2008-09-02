#
# spec file for package mono-addins (Version 0.3.1)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           mono-addins
Version:        0.3.1
Release:        1
License:        X11/MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.mono-project.com
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  gtk-sharp2 mono-devel
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
* Wed Mar 26 2008 wberrier@suse.de
- Update to 0.3.1
 -Fix compatibility with new Mono
 -Delete subdirectory when uninstalling
 -Improve error reporting
* Mon Jan 14 2008 wberrier@suse.de
- Initial package (needed by MD and other mono apps)
