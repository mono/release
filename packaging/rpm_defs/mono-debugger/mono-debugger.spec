#
# spec file for package mono-debugger (Version 2.0)
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


Name:           mono-debugger
License:        GPL v2 or later; X11/MIT
Group:          Development/Languages/Mono
Summary:        Mono Debugger
Url:            http://www.mono-project.com/Debugger
Version:        2.0
Release:        2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2
Provides:       mono-debugger = %{version}-%{release}
ExclusiveArch:  %ix86 x86_64
Requires:       mono-core = %{version}
BuildRequires:  mono-devel mono-nunit
# For older distros (but are harmless for new distros)
BuildRequires:  mono-web pkgconfig
#### suse options ###
%if 0%{?suse_version}
# factory needed this... ?
#  All distro versions need it, but it was installed by default up until 10.3
%if %{suse_version} > 1020
BuildRequires:  ncurses-devel
%endif
# For SLES9
%if %sles_version == 9
%define configure_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
BuildRequires:  pkgconfig
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
# Note: this fails to build on fedora5 x86_64 because of this bug:
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=189324
%endif

%description
A debugger is an important tool for development. The Mono Debugger
(MDB) can debug both managed and unmanaged applications.  It provides a
reusable library that can be used to add debugger functionality to
different front-ends. The debugger package includes a console debugger
named "mdb", and MonoDevelop (http://www.monodevelop.com) provides a
GUI interface to the debugger.



Authors:
--------
    Martin Baulig <martin@ximian.com>
    Chris Toshok <toshok@ximian.com>
    Miguel de Icaza <miguel@ximian.com>

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README NEWS
/usr/bin/mdb
%{_libdir}/*.so*
%{_prefix}/lib/mono/2.0/mdb.exe
%{_prefix}/lib/mono/2.0/mdb-symbolreader.exe
%{_prefix}/lib/mono/gac/Mono.Debugger
%{_prefix}/lib/mono/gac/Mono.Debugger.SymbolWriter
%{_prefix}/lib/mono/mono-debugger
%{_libdir}/pkgconfig/mono-debugger.pc

%prep
%setup  -q -n mono-debugger-%{version}

%build
%{?env_options}
%{?configure_options}
CFLAGS="$RPM_OPT_FLAGS"
%if %{suse_version} >= 1100
CFLAGS="$RPM_OPT_FLAGS `ncurses5-config --cflags`"
%endif
%configure
make

%install
%{?env_options}
make DESTDIR="$RPM_BUILD_ROOT" install
# Remove unnecessary devel files
rm -f $RPM_BUILD_ROOT%_libdir/libmonodebuggerreadline.*a
rm -f $RPM_BUILD_ROOT%_libdir/libmonodebuggerserver.*a

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Mon Sep 01 2008 ro@suse.de
- respect CFLAGS setting (for RPM_OPT_FLAGS)
  (patch present but disabled, too many errors)
- make term.c include ncurses/termcap.h to fix build
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0
  * Will be released with Mono going forward to ensure compatibility
  * Many bugfixes
* Tue May 06 2008 aj@suse.de
- Use <sys/users.h> to fix build.
* Tue Jan 15 2008 wberrier@novell.com
- Update to 0.60
 -Updated to run with mono 1.2.6 runtime
 -Various bux fixes
* Sat Jun 09 2007 wberrier@novell.com
- Add post/un ldconfig scripts
- Update to 0.50
 -Lots of bug-fixes, usability improvements and increased stability.
 -New object formatter:
  When printing a class object, we now include fields from its parents.
 -Added support for Displays (thanks to Massimiliano Mantione).
 -New threading model:
  By default, all threads are now stopped when the debugger is in
  control.
 -Ctrl-C now stops all threads.
 -We now support stripped `mono' binaries.
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Apr 05 2007 wberrier@novell.com
- Adapt for buildservice
* Wed Dec 06 2006 dmueller@suse.de
- don't build as root
* Wed Nov 15 2006 wberrier@suse.de
- Update to 0.31
 - (contains a gpl friendly libedit)
- Remove old patches
- mono-debugger_libedit_cast.patch: castings for new libedit
* Wed Aug 30 2006 wberrier@suse.de
- Update to 0.30.  Add requires mono-core >= 1.1.16
- 0.30 Changes:
 - Redesigned and improved the session code.
 - Stability improvements and bug fixes.
 - Fixed i386 support.
- 0.20 Changes:
 - We now preserve breakpoints across different invocations of
  the same target.
 - Big API cleanups.
 - Cleaned up method lookups; there's a very complex test for them
  in test/testsuite/TestMethodLookup.cs.
 - Lots of stability improvements.
 - Fixed a very old GC bug which was preventing us from running
  xsp inside the debugger.
 - Fixed a very old race condition which was causing crashes at exit.
 - Fixed line numbers in stack traces.
 - Added experimental support for hardware watchpoints - I needed
  them to track down a race condition.
- 0.13 Changes:
 - The test suite has been migrated to NUnit.
 - Multi-Process support: The debugger can now follow fork()s
  and exec()s and thus debug multiple processes at the same time.
- 0.12 Changes:
 - The debugger no longer uses a `mono-debugger-mini-wrapper',
  it's now using the normal `mono' instead.
 - We can now attach to processes and examine core files -
  this still needs some testing; bug reports are very welcome ...
 - We no longer run the backend in another process/appdomain;
  most of the remoting stuff is gone to make the debugger faster
  and more reliable.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Dec 22 2005 wberrier@suse.de
- Clean up spec, update to 0.11, add NULL patch for libedit, only
  build on x86 and x86_64
* Mon Aug 29 2005 aj@suse.de
- Add check-build.sh.
* Tue Aug 02 2005 ro@suse.de
- make it build ...
* Wed Jul 20 2005 wberrier@suse.de
- Initial submission
