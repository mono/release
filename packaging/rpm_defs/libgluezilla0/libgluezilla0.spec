#
# spec file for package libgluezilla0 (Version 2.0)
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

%define real_name gluezilla

Name:           libgluezilla0
Version:        2.0
Release:        1
License:        GPL v2 only
Url:            http://www.mono-project.com
Source0:        %{real_name}-%{version}.tar.bz2
Summary:        Glue library for Winforms Web Control
Group:          Development/Languages/Mono
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++ gtk2-devel
####  suse  ####
%if 0%{?suse_version}
%if %suse_version >= 1030
BuildRequires:  mozilla-nspr-devel mozilla-xulrunner181-devel
%endif
%if %suse_version == 1020
BuildRequires:  mozilla-nspr-devel mozilla-xulrunner181-devel
%endif
%if %sles_version == 10
BuildRequires:  gecko-sdk mozilla-nspr-devel mozilla-xulrunner
%endif
%if %suse_version == 1010
BuildRequires:  gecko-sdk mozilla-nspr-devel mozilla-xulrunner
%endif
%if %sles_version == 9
# Broken: missing nsEmbedCID.h
# mozilla-devel-1.7.8-5.13
BuildRequires:  mozilla-devel pkgconfig
%endif
%endif
####  fedora  ####
%if 0%{?fedora_version}
%if %{fedora_version} == 7
# works if xpcomglue link flag is removed
BuildRequires:  firefox-devel
%endif
%if %{fedora_version} == 6
# Broken: missing nsEmbedAPI.h
# firefox-devel-1.5.0.7-7.fc6
BuildRequires:  firefox-devel
%endif
%if %{fedora_version} == 5
# End of life?
# Broken: missing nsEmbedCID.h
# mozilla-devel-1.7.12-5
BuildRequires:  mozilla-devel
%endif
%endif
%if 0%{?rhel_version}
BuildRequires:  firefox-devel
%endif

%description
A simple library to embed Gecko (xulrunner) for the Mono Winforms
WebControl.



Authors:
--------
    Andreia Gaita <avidigal@novell.com>
    Zac Bowling <zac@zacbowling.com>

%files
%defattr(-, root, root)
%_libdir/libgluezilla.so*
%doc AUTHORS COPYING ChangeLog* INSTALL README TODO

%prep
%setup -q -n %{real_name}-%{version}

%build
# Set PKG_CONFIG_PATH for sles9
%if 0%{?sles_version}
%if %sles_version == 9
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
%endif
%endif
export CFLAGS="$RPM_OPT_FLAGS"
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Unwanted files:
rm -f $RPM_BUILD_ROOT/usr/%_lib/libgluezilla.la

%clean
rm -rf "$RPM_BUILD_ROOT"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri Aug 22 2008 ajorgensen@novell.com
- Update to 2.0
  * Context menu event support
  * Progress event support
  * Some bugfixes
* Mon Apr 21 2008 wberrier@suse.de
- Update to 1.9.1:
 -Fix bug where two browser widgets couldn't be in the same app
* Tue Mar 25 2008 wberrier@suse.de
- Update to 1.9:
 -Fixed to support more versions of windows, not just the one
  it was built for.
 -call ldconfig directly instead of invoking a shell
 -Several other bug fixes
* Wed Jan 16 2008 wberrier@suse.de
- rename gluezilla -> libgluezilla0
* Fri Jan 11 2008 wberrier@suse.de
- initial package
