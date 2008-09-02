#
# spec file for package apache2-mod_mono (Version 2.0)
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


Name:           apache2-mod_mono
%define apxs /usr/sbin/apxs2
%define apache2_sysconfdir %(%{apxs} -q SYSCONFDIR)/conf.d
Obsoletes:      mod_mono
%define modname mod_mono
%define apache2_libexecdir %(%{apxs} -q LIBEXECDIR)
%define apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)
Url:            http://go-mono.com/
License:        The Apache Software License
Group:          Productivity/Networking/Web/Servers
AutoReqProv:    on
Version:        2.0
Release:        1
Summary:        Run ASP.NET Pages on Unix with Apache and Mono
Source:         %{modname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       mod_mono = %{version}-%{release}
# This must be manually entered according to xsp's protocol version
Requires:       xsp >= %{version}
############### Suse based options
%if 0%{?suse_version}
BuildRequires:  apache2-devel mono-devel
Requires:       apache2 %{apache_mmn} 
%if %{suse_version} >= 1010
BuildRequires:  libapr-util1-devel
%endif
%if %{sles_version} == 9
BuildRequires:  pkgconfig
%endif
%endif
############### redhat based options
%if 0%{?fedora_version} || 0%{?rhel_version}
BuildRequires:  httpd-devel pkgconfig
Requires:       httpd
%endif

%description
mod_mono is a module that interfaces Apache with Mono and allows
running ASP.NET pages on Unix and Unix-like systems. To load the module
into Apache, run the command "a2enmod mono" as root.



%prep
%setup -n %{modname}-%{version} -q

%build
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT APXS_SYSCONFDIR="%{apache2_sysconfdir}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{apache2_libexecdir}/*
%{apache2_sysconfdir}/*
%{_mandir}/man8/mod_mono.8*

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0 (preview 2)
  * Fixes bnc#374272, bnc#392235,
* Tue Apr 29 2008 wberrier@suse.de
- Fix .conf and apxs file location for redhat/fedora
* Tue Mar 25 2008 wberrier@suse.de
- Update to 1.9
 -New support for controlling the number of requests that are
  passed to the mod-mono-server process
* Mon Jan 14 2008 wberrier@suse.de
- Update to 1.2.6
 -New directives for controlling the life span of mod-mono-server
 -Startup of mod_mono backends synchronized across all the child
  apache processes (via a shared memory dashboard).
* Thu Aug 30 2007 wberrier@suse.de
- mod_mono_1.2.5_p5_final.patch: fix regression: avoid sem leak
* Fri Aug 17 2007 wberrier@suse.de
- put mod_mono.conf in /etc/apache2/conf.d instead of /etc/apache2
- mod_mono_1.2.5_p4.patch.bz2: Bugfixes found in 1.2.5
 -stabilization and performance fixes that accompany the bugs
  found in xsp 1.2.5
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -Error logging
 -support for ServerAlias directive
* Tue Jun 05 2007 wberrier@novell.com
- Update to 1.2.4
 -Connection cancellation fixes
 -better detection of apu at buildtime
* Tue Apr 03 2007 wberrier@novell.com
- Get building in build service for suse and fedora
 -mod_mono-check_headers_apuconfig.patch: patch to enable
  autodetection of apr-util headers on suse 10.1
* Mon Jan 22 2007 ro@suse.de
- drop requires for gnome-filesystem
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.1 (Fate #301111)
 -handle the new configurable umask directive
* Mon Nov 13 2006 poeml@suse.de
- add Provides: mod_mono = %%{version}-%%{release}
* Mon Nov 13 2006 poeml@suse.de
- fix build with versions < 10.1 of the distro where libapr-util1
  did not yet exist as a package (libapr* was in apache2-devel)
* Mon Nov 13 2006 poeml@suse.de
- rename to apache2-mod_mono
* Fri Oct 20 2006 wberrier@suse.de
- Update 1.1.18
 -fix for autohosting and virtual hosts
* Wed Aug 30 2006 wberrier@suse.de
- Update to 1.1.17
- Remove upstream patches
- Added support for X.509 client certificates
* Mon Jul 31 2006 wberrier@suse.de
- Added some patches to build against apache 2.2.2
- Removed xsp from build deps
- Update to 1.1.16.1
- src/mod_mono.c: when using autoapplications, pass all the options that
  don't have an explicit alias to XXGLOBAL, which is the internal name
  used for the mod-mono-server instance that will create new applications
  on demand. Using XXGLOBAL as an identifier is forbidden now.
- src/mod_mono.c: allow setting MonoDebug when using automatic
  applications. Before this fix, no mod-mono-server would be started.
  Fixes bug #78672.
* Fri Apr 07 2006 wberrier@novell.com
- Update to 1.1.13.5, minor bug fix release
 -Fix DoS (Critical fix for iFolder)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Sat Jan 07 2006 wberrier@suse.de
- Get building with apache 2.2
 - use apr 1.1.x instead of apr provided with httpd
 - needed CPPFLAGS to find apr dev files
 - autoreconf fixes configure in order to find apache/apr headers
- Cleaned up deps (no gtk/x/gnome needed)
* Fri Nov 11 2005 wberrier@suse.de
- 1.1.10 tarball was updated
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10, remove icu deps
* Fri Oct 07 2005 wberrier@suse.de
- Updated to 1.1.9.2
* Tue Aug 09 2005 gekker@suse.de
- Update to version 1.0.9
* Mon Feb 21 2005 clahey@suse.de
- Update to 1.0.6.
* Tue Dec 14 2004 clahey@suse.de
- New package.
