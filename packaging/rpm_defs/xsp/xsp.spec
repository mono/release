#
# spec file for package xsp (Version 2.0)
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


Name:           xsp
Url:            http://go-mono.com/
License:        GPL v2 or later
Group:          Productivity/Networking/Web/Servers
AutoReqProv:    on
Version:        2.0
Release:        1
Summary:        Small Web Server Hosting ASP.NET
Source:         %{name}-%{version}.tar.bz2
#Patch:        xsp-libexecdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  mono-data-oracle mono-data-sqlite mono-devel mono-extras mono-jscript mono-nunit mono-web pkgconfig
# One of the test runs requires this
BuildRequires:  sqlite
# This must be manually entered according to xsp's protocol version
# Since this package is currently noarch, and mod_mono's name is different
# on different distros, we can't use this... yet
#Requires:       mod_mono >= %{version}
#####  suse  ####
%if 0%{?suse_version}
%define old_suse_buildrequires mono-data mono-winforms
%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
The XSP server is a small Web server that hosts the Mono System.Web
classes for running what is commonly known as ASP.NET.



%prep
%setup -q

%build
%{?env_options}
# Cannot use the configure macro because noarch-redhat-linux is not recognized by the auto tools in the tarball
./configure --prefix=%{_prefix} \
	    --libexecdir=%{_prefix}/lib \
	    --libdir=%{_prefix}/lib \
	    --mandir=%{_prefix}/share/man \
	    --infodir=%{_prefix}/share/info \
	    --sysconfdir=%{_sysconfdir}
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/usr/share
mv ${RPM_BUILD_ROOT}/usr/lib/pkgconfig ${RPM_BUILD_ROOT}/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/pkgconfig/*
%{_prefix}/share/man/*/*
%{_prefix}/lib/xsp
%{_prefix}/lib/mono/gac/Mono.WebServer
%{_prefix}/lib/mono/1.0/Mono.WebServer.dll
%{_prefix}/lib/mono/gac/Mono.WebServer2
%{_prefix}/lib/mono/2.0/Mono.WebServer2.dll
%{_prefix}/lib/mono/gac/xsp
%{_prefix}/lib/mono/1.0/xsp.exe
%{_prefix}/lib/mono/gac/xsp2
%{_prefix}/lib/mono/2.0/xsp2.exe
%{_prefix}/lib/mono/gac/mod-mono-server
%{_prefix}/lib/mono/1.0/mod-mono-server.exe
%{_prefix}/lib/mono/gac/mod-mono-server2
%{_prefix}/lib/mono/2.0/mod-mono-server2.exe
%{_prefix}/lib/mono/gac/fastcgi-mono-server
%{_prefix}/lib/mono/1.0/fastcgi-mono-server.exe
%{_prefix}/lib/mono/gac/fastcgi-mono-server2
%{_prefix}/lib/mono/2.0/fastcgi-mono-server2.exe
%doc NEWS README
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0
  * Fixes bnc#350779, bnc#359783, bnc#363404, bnc#372220,
  bnc#324204, bnc#408723
  * Sync with mod_mono changes
* Tue Apr 22 2008 wberrier@suse.de
- update to 1.9.1 (bugfix release)
 -Output date header (instead of asp.net doing it)
* Tue Mar 25 2008 wberrier@suse.de
- update to 1.9
 -minor test updates
 -BaseRequestBroker fix: Check if the request ID is valid inside
  the lock.
* Mon Jan 14 2008 wberrier@suse.de
- update to 1.2.6
 -FastCGI support
* Thu Aug 30 2007 wberrier@suse.de
- xsp_1.2.5_p5_final.patch: Fix for regression in the request
  broker
* Fri Aug 17 2007 wberrier@suse.de
- xsp_1.2.5_p4.patch.bz2: Bugfixes found in 1.2.5
 -bugs: 81699, 81906, 82379, 82057
 -fixes ability to handle large (GB) uploads (needed for iFolder)
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -More robust exception handling
 -Fixed permissions bits for non executable scripts
 -virtual host support
 -New Documentation for Mono.WebServer
 -Improved event handling
* Tue Jun 05 2007 wberrier@novell.com
- Remove unnecessary path defines (prefix, sysconfdir)
- Update to 1.2.4
 -fix some race conditions and crashes
 -add tracing support
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Mar 01 2007 wberrier@suse.de
- Update Update to 1.2.3
 -Bug fix #80230 (prevents possible nullref)
 -Support for response header encoding
* Mon Jan 22 2007 ro@suse.de
- drop requires for gnome-filesystem
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.1 (Fate #301111)
 -Bugfixes:
  -close the connection if there's an error reading the headers
  (including assembly loading exceptions due to a bad installation).
  -kill the warning that everyone is worried about.
* Fri Oct 20 2006 wberrier@suse.de
- Update to 1.1.18
 -2.0 updates
* Thu Oct 19 2006 wberrier@suse.de
- Add mono-devel to fix bnc #213576 (missing provides)
* Tue Sep 05 2006 wberrier@suse.de
- Update to 1.1.17.1 bugfix release
- Read from the stream, not the socket as the socket data is
  encrypted when using SSL.
* Wed Aug 30 2006 wberrier@suse.de
- Update to 1.1.17
 - Added support for X.509 client certificates
 - Update to handle newly created AppDomains
* Mon Jul 31 2006 wberrier@suse.de
- update to 1.1.16.1
- better connection handling
- fixes bugs: 77698,78034,78621
* Tue Apr 25 2006 wberrier@suse.de
- Security update (remove all the duplicated slashes
  and don't do an extra Replace on non-windows.) and minor fix for
  [#78034].
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 06 2006 wberrier@suse.de
- Update to 1.1.13, clean up deps
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10, set libdir to lib/
* Fri Oct 07 2005 wberrier@suse.de
- Update to 1.1.9.2 and cleanup (I Don't think noarch mono needs
  libexec, so I disabled the patch)
* Tue Jul 19 2005 sbrabec@suse.cz
- Build as noarch (#81109).
* Fri Jul 15 2005 sbrabec@suse.cz
- Updated to version 1.0.9 (#96776).
* Mon Feb 21 2005 clahey@suse.de
- Updated to 1.0.6.
* Sun Feb 06 2005 ro@suse.de
- use /usr/lib/mono
* Mon Dec 13 2004 clahey@suse.de
- New package.
