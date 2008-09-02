#
# spec file for package mono-basic (Version 2.0)
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

%define prebuilt_release 0

Name:           mono-basic
BuildRequires:  mono-devel
License:        LGPL v2.1 or later
Group:          Development/Languages/Mono
Summary:        Mono's VB Runtime
Url:            http://go-mono.org/
Version:        2.0
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-%{version}-%{prebuilt_release}.novell.noarch.rpm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's VB runtime.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files
%defattr(-, root, root)
%_prefix/bin/vbnc
%_prefix/lib/mono/2.0/vbnc*
%_prefix/lib/mono/gac/Microsoft.VisualBasic
%_prefix/lib/mono/*/Microsoft.VisualBasic.dll

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=/usr
make

%install
%{?env_options}
make install DESTDIR=${RPM_BUILD_ROOT}
## Get ms.net runtime out of noarch rpm (building in buildservice or autobuild)
if [ -e %{S:1} ] ; then
	rpm2cpio %{S:1} | cpio -idv
	# Remove vbnc built runtime
	rm -Rf ${RPM_BUILD_ROOT}/usr/lib/mono/gac/Microsoft.VisualBasic
	rm -Rf ${RPM_BUILD_ROOT}/usr/lib/mono/2.0/Microsoft.VisualBasic.dll
	## Install runtime from noarch.rpm into new gac
	gacutil -package 1.0 -root ${RPM_BUILD_ROOT}/usr/lib -i usr/lib/mono/1.0/Microsoft.VisualBasic.dll
	gacutil -package 2.0 -root ${RPM_BUILD_ROOT}/usr/lib -i usr/lib/mono/2.0/Microsoft.VisualBasic.dll
else
        # Check for binaries built on windows (for building on monobuild)
	if test %{prebuilt_release} == 0 ; then
		release_dir=""
	else
		release_dir="-%{prebuilt_release}"
	fi
        f="mono-basic-%{version}-%{prebuilt_release}.win4.novell.x86.zip"
        p="win-4-i386/mono-basic/%{version}${release_dir}/files/downloads/$f"
        wget --tries=1 --timeout=10 http://build.mono.lab.novell.com/builds/RELEASE/$p || true
        wget --tries=1 --timeout=10 http://build.mono.lab.novell.com/builds/HEAD/$p || true
        # If we have windows built binaries, inject them into the package (to provide the 1.0 runtime)
        if [ -e "$f" ] ; then 
                unzip $f
                # Remove vbnc built runtime
                rm -Rf ${RPM_BUILD_ROOT}/%_prefix/lib/mono/gac/Microsoft.VisualBasic/7.0.*
                # Fix permissions on files so they are readable
                chmod 755 lib/mono/1.0/Microsoft.VisualBasic.dll
                ## Install into new gac
                gacutil -package 1.0 -root ${RPM_BUILD_ROOT}/usr/lib -i lib/mono/1.0/Microsoft.VisualBasic.dll
        else
                # If we're building from HEAD, print warning (HEAD doesn't have a version with periods)
                if test `echo "%{version}" | sed -e 's/\.//g'` == "%{version}" ; then
                        echo ""
                        echo "*** vbnc DEBUG BUILD!  Don't ship this RPM! ***"
                        echo ""
                # Otherwise RELEASE, fail build, because we don't want to ship an rpm without the 1.0 runtime
                else
                        false
                fi
        fi
fi
# Not needed in 1.2.4, since we can bootstrap vbnc
# ship prebuilt vbnc for now...
#mkdir -p ${RPM_BUILD_ROOT}/usr/bin
#cp -f usr/bin/vbnc ${RPM_BUILD_ROOT}/usr/bin
#cp usr/lib/mono/2.0/vbnc.* ${RPM_BUILD_ROOT}/usr/lib/mono/2.0
cd $RPM_BUILD_ROOT
rm -f .%{_prefix}/lib/mono/2.0/extract-source.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-console.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-execute.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt.exe*

%clean
rm -rf ${RPM_BUILD_ROOT}
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0
  * Better handling of error conditions
  * Fixes for bnc#325331, bnc#324807, bnc#361412
* Tue Mar 25 2008 wberrier@suse.de
- Automatically pick the correct file for the prebuilt vb runtime
- Update to 1.9
 -More support in the IO classes for Visual Basic
* Mon Jan 14 2008 wberrier@suse.de
- Update to 1.2.6
 -Updated internal version to work with versions of .net > 2.0
 -Several bug fixes in the vb runtime
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -support for late binding in vbnc (Option Strict Off and Option
  Explicit Off).
 -several bugfixes in vbnc, and vbruntime
 -error reporting is somewhat better now (now possible to get line
  numbers in stack traces)
* Tue Jun 05 2007 wberrier@novell.com
- Build vbnc instead of shipping from binary
- Update to 1.2.4
 -fixes to enable vb.net in asp.net
 -'My' namespace support in vbnc
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Wed Mar 14 2007 wberrier@suse.de
- Ship prebuilt binaries for now.  Some runtime fixes are needed
  before vbnc will compile on all archs
* Fri Mar 09 2007 wberrier@suse.de
- Update to 1.2.3.1
 -Includes vbnc compiler (which is self hosting, but we still
  ship the vbruntime built with with ms.net because vbnc doesn't
  support 1.0 assemblies yet)
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.2 (Fate #301111)
 -Testsuite updates
 -Runtime fixes and updates
* Fri Oct 20 2006 wberrier@suse.de
- Update to 1.1.18
 -many fixes to the basic runtime
* Wed Aug 30 2006 ro@suse.de
- remove ExclusiveArch from noarch package
* Tue Aug 29 2006 wberrier@suse.de
- Initial package
