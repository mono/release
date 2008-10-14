#
# spec file for package mono-core (Version 2.0)
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

%{!?ext_man: %define ext_man .gz}
Name:           mono-core
License:        LGPL v2.1 or later
Group:          Development/Languages/Mono
Summary:        A .NET Runtime Environment
Url:            http://go-mono.org/
Version:        2.0
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        mono-%{version}.tar.bz2
ExclusiveArch:  %ix86 x86_64 ppc hppa armv4l sparc s390 ia64 s390x
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       mono = %{version}-%{release}
Provides:       mono-ikvm = %{version}-%{release}
Obsoletes:      mono
Obsoletes:      mono-drawing
Obsoletes:      mono-cairo
Obsoletes:      mono-xml-relaxng
Obsoletes:      mono-posix
Obsoletes:      mono-ziplib
Obsoletes:      mono-ikvm
Provides:       mono-drawing
Provides:       mono-cairo
Provides:       mono-xml-relaxng
Provides:       mono-posix
Provides:       mono-ziplib
# This version of mono has issues with the following versions of apps:
#  (not because of regressions, but because bugfixes in mono uncover bugs in the apps)
Conflicts:      helix-banshee <= 0.13.1
Conflicts:      banshee <= 0.13.1
Conflicts:      f-spot <= 0.3.5
Conflicts:      mono-addins <= 0.3
# 1.9 branch conflicts:
#  Can't do this because this rpm could be used on a distro with gtk# 2.8...
#Conflicts:	gtk-sharp2 < 2.10.3
# Require when in the buildserivce
%if 0%{?opensuse_bs}
Requires:       libgdiplus0
%endif
%if 0%{?monobuild}
Requires:       libgdiplus0
%endif
# for autobuild
%if 0%{?monobuild} == 0
%if 0%{?opensuse_bs} == 0
# suse would rather have recommends so that all sorts of graphic libs aren't 
#  pulled in when libgdiplus is installed
Recommends:     libgdiplus0
Recommends:     libgluezilla0
%endif
%endif
BuildRequires:  glib2-devel zlib-devel
#######  distro specific changes  ########
#####
#### suse options ####
%if 0%{?suse_version}
# For some reason these weren't required in 10.2 and before... ?
%if %{suse_version} >= 1030
BuildRequires:  bison
# Add valgrind support for 10.3 and above on archs that have it
%ifarch %ix86 x86_64 ppc ppc64
BuildRequires:  valgrind-devel
%endif
%endif
%if %{suse_version} >= 1020
BuildRequires:  xorg-x11-libX11
%endif
%if %{sles_version} == 10
BuildRequires:  xorg-x11-devel
%endif
%if %{suse_version} == 1010
BuildRequires:  xorg-x11-devel
%endif
%if %{sles_version} == 9
%define configure_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
BuildRequires:  XFree86-devel XFree86-libs pkgconfig
%endif
%endif
# Fedora x11
%if 0%{?fedora_version}
BuildRequires:  libX11
%endif
# rhel x11
%if 0%{?rhel_version}
BuildRequires:  libX11
%endif
#####
#######  End of distro specific changes  ########
# Why was this needed?
%ifarch s390 s390x
PreReq:         grep
%endif
# This lib only needed for ia64
%ifarch ia64
BuildRequires:  libunwind-devel
%endif
# TODO:
# This won't work until the rpm package passes .config files to mono-find-requires
#%define __find_provides env MONO_PREFIX=%{buildroot}/usr /usr/lib/rpm/find-provides
#%define __find_requires env MONO_PREFIX=%{buildroot}/usr /usr/lib/rpm/find-requires
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}/usr %{buildroot}%{_bindir}/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}/usr %{buildroot}%{_bindir}/mono-find-requires ; } | sort | uniq'

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -f mcs.lang
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog NEWS README
%_bindir/mono
%_libdir/libmono.so*
%_mandir/man1/mono.1%ext_man
# manpages
%_mandir/man5/mono-config.5%ext_man
%_mandir/man1/mcs.1%ext_man
%_mandir/man1/certmgr.1%ext_man
%_mandir/man1/chktrust.1%ext_man
%_mandir/man1/csharp.1%ext_man
%_mandir/man1/setreg.1%ext_man
%_mandir/man1/gacutil.1%ext_man
%_mandir/man1/sn.1%ext_man
%_mandir/man1/mozroots.1%ext_man
# wrappers
%_bindir/certmgr
%_bindir/chktrust
%_bindir/csharp
%_bindir/gacutil
%_bindir/gacutil2
%_bindir/gmcs
%_bindir/mono-test-install
%_bindir/mcs
%_bindir/mcs1
%_bindir/smcs
%_bindir/mozroots
%_bindir/setreg
%_bindir/sn
# exes
%_prefix/lib/mono/1.0/certmgr.exe*
%_prefix/lib/mono/1.0/chktrust.exe*
%_prefix/lib/mono/1.0/gacutil.exe*
%_prefix/lib/mono/2.0/gacutil.exe*
%_prefix/lib/mono/2.0/csharp.exe*
%_prefix/lib/mono/2.0/gmcs.exe*
%_prefix/lib/mono/1.0/mcs.exe*
%_prefix/lib/mono/1.0/mozroots.exe*
%_prefix/lib/mono/1.0/setreg.exe*
%_prefix/lib/mono/1.0/sn.exe*
%_prefix/lib/mono/gac/cscompmgd
%_prefix/lib/mono/1.0/cscompmgd.dll
%_prefix/lib/mono/2.0/cscompmgd.dll
%_prefix/lib/mono/gac/I18N.West
%_prefix/lib/mono/1.0/I18N.West.dll
%_prefix/lib/mono/2.0/I18N.West.dll
%_prefix/lib/mono/gac/I18N
%_prefix/lib/mono/1.0/I18N.dll
%_prefix/lib/mono/2.0/I18N.dll
%_prefix/lib/mono/gac/Mono.CompilerServices.SymbolWriter
%_prefix/lib/mono/1.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/2.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/gac/Mono.GetOptions
%_prefix/lib/mono/1.0/Mono.GetOptions.dll
%_prefix/lib/mono/2.0/Mono.GetOptions.dll
%_prefix/lib/mono/gac/Mono.Simd
%_prefix/lib/mono/2.0/Mono.Simd.dll
%_prefix/lib/mono/gac/Mono.Management
%_prefix/lib/mono/gac/Mono.Security
%_prefix/lib/mono/1.0/Mono.Security.dll
%_prefix/lib/mono/2.0/Mono.Security.dll
%_prefix/lib/mono/gac/System.Security
%_prefix/lib/mono/1.0/System.Security.dll
%_prefix/lib/mono/2.0/System.Security.dll
%_prefix/lib/mono/gac/System.Xml
%_prefix/lib/mono/1.0/System.Xml.dll
%_prefix/lib/mono/2.0/System.Xml.dll
%_prefix/lib/mono/2.1/System.Xml.dll
%_prefix/lib/mono/gac/System.Xml.Linq
%_prefix/lib/mono/2.0/System.Xml.Linq.dll
%_prefix/lib/mono/gac/System
%_prefix/lib/mono/1.0/System.dll
%_prefix/lib/mono/2.0/System.dll
%_prefix/lib/mono/2.1/System.dll
%_prefix/lib/mono/gac/System.Configuration
%_prefix/lib/mono/2.0/System.Configuration.dll
%_prefix/lib/mono/1.0/mscorlib.dll*
%_prefix/lib/mono/2.0/mscorlib.dll*
%_prefix/lib/mono/2.1/mscorlib.dll*
%_prefix/lib/mono/2.1/smcs.exe*
%dir %_sysconfdir/mono
%dir %_sysconfdir/mono/1.0
%dir %_sysconfdir/mono/2.0
%dir %_prefix/lib/mono
%dir %_prefix/lib/mono/1.0
%dir %_prefix/lib/mono/2.0
%dir %_prefix/lib/mono/2.1
%dir %_prefix/lib/mono/3.5
%dir %_prefix/lib/mono/gac
%config %_sysconfdir/mono/config
%config %_sysconfdir/mono/1.0/machine.config
%config %_sysconfdir/mono/2.0/machine.config
%config %_sysconfdir/mono/2.0/settings.map
%_prefix/lib/mono/gac/Mono.C5
%_prefix/lib/mono/2.0/Mono.C5.dll
# ikvm helper
%_prefix/%_lib/libikvm-native.so
%_prefix/lib/mono/gac/System.Drawing
%_prefix/lib/mono/1.0/System.Drawing.dll
%_prefix/lib/mono/2.0/System.Drawing.dll
%_libdir/libMonoPosixHelper.so*
%_prefix/lib/mono/gac/Mono.Posix
%_prefix/lib/mono/1.0/Mono.Posix.dll
%_prefix/lib/mono/2.0/Mono.Posix.dll
%_prefix/lib/mono/gac/Mono.Cairo
%_prefix/lib/mono/1.0/Mono.Cairo.dll
%_prefix/lib/mono/2.0/Mono.Cairo.dll
%_prefix/lib/mono/gac/ICSharpCode.SharpZipLib
%_prefix/lib/mono/1.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/compat-1.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/compat-2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/gac/Microsoft.VisualC
%_prefix/lib/mono/1.0/Microsoft.VisualC.dll
%_prefix/lib/mono/2.0/Microsoft.VisualC.dll
%_prefix/lib/mono/gac/Commons.Xml.Relaxng
%_prefix/lib/mono/1.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/2.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/gac/CustomMarshalers
%_prefix/lib/mono/1.0/CustomMarshalers.dll
%_prefix/lib/mono/2.0/CustomMarshalers.dll
%_prefix/lib/mono/gac/OpenSystem.C
%_prefix/lib/mono/1.0/OpenSystem.C.dll
%_prefix/lib/mono/2.0/OpenSystem.C.dll
%_prefix/lib/mono/gac/System.Core
%_prefix/lib/mono/2.0/System.Core.dll
%_prefix/lib/mono/2.1/System.Core.dll
%_prefix/lib/mono/gac/System.Net
%_prefix/lib/mono/2.1/System.Net.dll
%_prefix/lib/mono/gac/Mono.CSharp
%_prefix/lib/mono-options
# localizations?
#%_datadir/locale/*/LC_MESSAGES/mcs.mo
# Not sure if autobuild allows this...
%_libdir/pkgconfig/smcs.pc

%post
/sbin/ldconfig
%ifarch s390 s390x
if grep -q "machine = 9672" /proc/cpuinfo 2>/dev/null ; then
    # anchor for rebuild on failure
    echo "mono may not work correctly on G5"
fi
%endif

%postun -p /sbin/ldconfig

%package -n mono-jscript
License:        LGPL v2.1 or later
Summary:        JScript .NET support for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-jscript
This package contains the JScript .NET compiler and language runtime.
This allows you to compile and run JScript.NET application and
assemblies.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-jscript
%defattr(-, root, root)
%_bindir/mjs
%_prefix/lib/mono/1.0/mjs.exe*
%_prefix/lib/mono/gac/Microsoft.JScript
%_prefix/lib/mono/1.0/Microsoft.JScript.dll
%_prefix/lib/mono/2.0/Microsoft.JScript.dll

%package -n mono-locale-extras
License:        LGPL v2.1 or later
Summary:        Extra locale information
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-locale-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra locale information.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-locale-extras
%defattr(-, root, root)
%_prefix/lib/mono/gac/I18N.MidEast
%_prefix/lib/mono/1.0/I18N.MidEast.dll
%_prefix/lib/mono/2.0/I18N.MidEast.dll
%_prefix/lib/mono/gac/I18N.Rare
%_prefix/lib/mono/1.0/I18N.Rare.dll
%_prefix/lib/mono/2.0/I18N.Rare.dll
%_prefix/lib/mono/gac/I18N.CJK
%_prefix/lib/mono/1.0/I18N.CJK.dll
%_prefix/lib/mono/2.0/I18N.CJK.dll
%_prefix/lib/mono/gac/I18N.Other
%_prefix/lib/mono/1.0/I18N.Other.dll
%_prefix/lib/mono/2.0/I18N.Other.dll

%package -n mono-data
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-ms-enterprise
Obsoletes:      mono-novell-directory
Obsoletes:      mono-directory
Provides:       mono-ms-enterprise
Provides:       mono-novell-directory
Provides:       mono-directory

%description -n mono-data
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data
%defattr(-, root, root)
%_prefix/lib/mono/2.0/sqlsharp.exe*
%_bindir/sqlsharp
%_mandir/man1/sqlsharp.1%ext_man
%_prefix/lib/mono/gac/System.Data
%_prefix/lib/mono/1.0/System.Data.dll
%_prefix/lib/mono/2.0/System.Data.dll
%_prefix/lib/mono/gac/System.Data.Linq
%_prefix/lib/mono/2.0/System.Data.Linq.dll
%_prefix/lib/mono/gac/Mono.Data
%_prefix/lib/mono/1.0/Mono.Data.dll
%_prefix/lib/mono/2.0/Mono.Data.dll
%_prefix/lib/mono/gac/Mono.Data.Tds
%_prefix/lib/mono/1.0/Mono.Data.Tds.dll
%_prefix/lib/mono/2.0/Mono.Data.Tds.dll
%_prefix/lib/mono/gac/Mono.Data.TdsClient
%_prefix/lib/mono/1.0/Mono.Data.TdsClient.dll
%_prefix/lib/mono/2.0/Mono.Data.TdsClient.dll
%_prefix/lib/mono/gac/System.EnterpriseServices
%_prefix/lib/mono/1.0/System.EnterpriseServices.dll
%_prefix/lib/mono/2.0/System.EnterpriseServices.dll
%_prefix/lib/mono/gac/Novell.Directory.Ldap
%_prefix/lib/mono/1.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/2.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/gac/System.DirectoryServices
%_prefix/lib/mono/1.0/System.DirectoryServices.dll
%_prefix/lib/mono/2.0/System.DirectoryServices.dll
%_prefix/lib/mono/gac/System.Transactions
%_prefix/lib/mono/2.0/System.Transactions.dll
%_prefix/lib/mono/gac/System.Data.DataSetExtensions
%_prefix/lib/mono/2.0/System.Data.DataSetExtensions.dll

%package -n mono-winforms
License:        LGPL v2.1 or later
Summary:        Mono's Windows Forms implementation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Provides:       mono-window-forms
Obsoletes:      mono-window-forms

%description -n mono-winforms
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's Windows Forms implementation.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-winforms
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.Windows.Forms
%_prefix/lib/mono/1.0/System.Windows.Forms.dll
%_prefix/lib/mono/2.0/System.Windows.Forms.dll
%_prefix/lib/mono/gac/Accessibility
%_prefix/lib/mono/1.0/Accessibility.dll
%_prefix/lib/mono/2.0/Accessibility.dll
%_prefix/lib/mono/gac/System.Design
%_prefix/lib/mono/1.0/System.Design.dll
%_prefix/lib/mono/2.0/System.Design.dll
%_prefix/lib/mono/gac/System.Drawing.Design
%_prefix/lib/mono/1.0/System.Drawing.Design.dll
%_prefix/lib/mono/2.0/System.Drawing.Design.dll
# TODO: Post 1.2.5:
%_prefix/lib/mono/1.0/Mono.WebBrowser.dll
%_prefix/lib/mono/2.0/Mono.WebBrowser.dll
%_prefix/lib/mono/gac/Mono.WebBrowser

%package -n ibm-data-db2
License:        LGPL v2.1 or later
Summary:        Database connectivity for DB2
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n ibm-data-db2
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for DB2.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n ibm-data-db2
%defattr(-, root, root)
%_prefix/lib/mono/gac/IBM.Data.DB2
%_prefix/lib/mono/1.0/IBM.Data.DB2.dll
%_prefix/lib/mono/2.0/IBM.Data.DB2.dll

%package -n mono-extras
License:        LGPL v2.1 or later
Summary:        Extra packages
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-ms-extras
Provides:       mono-ms-extras

%description -n mono-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra packages.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-extras
%defattr(-, root, root)
%_mandir/man1/mono-service.1%ext_man
%_bindir/mono-service
%_bindir/mono-service2
# These are errors because they should be symlinks, but they are copies, so rpmlint detects duplicate files
%_prefix/lib/mono/gac/mono-service
%_prefix/lib/mono/1.0/mono-service.exe*
%_prefix/lib/mono/2.0/mono-service.exe*
%_prefix/lib/mono/gac/System.Management
%_prefix/lib/mono/1.0/System.Management.dll
%_prefix/lib/mono/2.0/System.Management.dll
%_prefix/lib/mono/gac/System.Messaging
%_prefix/lib/mono/1.0/System.Messaging.dll
%_prefix/lib/mono/2.0/System.Messaging.dll
%_prefix/lib/mono/gac/System.ServiceProcess
%_prefix/lib/mono/1.0/System.ServiceProcess.dll
%_prefix/lib/mono/2.0/System.ServiceProcess.dll
%_prefix/lib/mono/gac/System.Configuration.Install
%_prefix/lib/mono/1.0/System.Configuration.Install.dll
%_prefix/lib/mono/2.0/System.Configuration.Install.dll
%_prefix/lib/mono/gac/Microsoft.Vsa
%_prefix/lib/mono/1.0/Microsoft.Vsa.dll
%_prefix/lib/mono/2.0/Microsoft.Vsa.dll

%package -n mono-data-sqlite
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release
# TODO: Disable this, until a better solution is found
#Requires:       sqlite2

%description -n mono-data-sqlite
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-sqlite
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Data.SqliteClient
%_prefix/lib/mono/1.0/Mono.Data.SqliteClient.dll
%_prefix/lib/mono/2.0/Mono.Data.SqliteClient.dll
%_prefix/lib/mono/gac/Mono.Data.Sqlite
%_prefix/lib/mono/1.0/Mono.Data.Sqlite.dll
%_prefix/lib/mono/2.0/Mono.Data.Sqlite.dll

%package -n mono-data-sybase
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-sybase
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-sybase
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Data.SybaseClient
%_prefix/lib/mono/1.0/Mono.Data.SybaseClient.dll
%_prefix/lib/mono/2.0/Mono.Data.SybaseClient.dll

%package -n mono-wcf
Summary:        Mono implementation of WCF, Windows Communication Foundation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-wcf
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of WCF, Windows Communication Foundation



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>


%files -n mono-wcf
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.IdentityModel
%_prefix/lib/mono/2.0/System.IdentityModel.dll
%_prefix/lib/mono/gac/System.IdentityModel.Selectors
%_prefix/lib/mono/2.0/System.IdentityModel.Selectors.dll
%_prefix/lib/mono/gac/System.Runtime.Serialization
%_prefix/lib/mono/2.0/System.Runtime.Serialization.dll
%_prefix/lib/mono/gac/System.ServiceModel
%_prefix/lib/mono/2.0/System.ServiceModel.dll
%_prefix/lib/mono/gac/System.ServiceModel.Web
%_prefix/lib/mono/2.0/System.ServiceModel.Web.dll
%_libdir/pkgconfig/wcf.pc

%package -n mono-web
License:        LGPL v2.1 or later
Summary:        Mono implementation of ASP.NET, Remoting and Web Services
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-web-forms
Obsoletes:      mono-web-services
Obsoletes:      mono-remoting
Provides:       mono-web-forms
Provides:       mono-web-services
Provides:       mono-remoting

%description -n mono-web
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET, Remoting and Web Services.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-web
%defattr(-, root, root)
%_prefix/lib/mono/gac/Mono.Http
%_prefix/lib/mono/1.0/Mono.Http.dll
%_prefix/lib/mono/2.0/Mono.Http.dll
%_prefix/lib/mono/gac/Mono.Web
%_prefix/lib/mono/2.0/Mono.Web.dll
%_prefix/lib/mono/gac/System.Runtime.Remoting
%_prefix/lib/mono/1.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/2.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/gac/System.Web
%_prefix/lib/mono/1.0/System.Web.dll
%_prefix/lib/mono/2.0/System.Web.dll
%_prefix/lib/mono/gac/System.Runtime.Serialization.Formatters.Soap
%_prefix/lib/mono/1.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/2.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/gac/System.Web.Services
%_prefix/lib/mono/1.0/System.Web.Services.dll
%_prefix/lib/mono/2.0/System.Web.Services.dll
%_prefix/lib/mono/gac/System.Web.Abstractions
%_prefix/lib/mono/2.0/System.Web.Abstractions.dll
%_prefix/lib/mono/gac/System.Web.Routing
%_prefix/lib/mono/2.0/System.Web.Routing.dll
%_prefix/lib/mono/gac/System.Web.Extensions
%_prefix/lib/mono/2.0/System.Web.Extensions.dll
%_prefix/lib/mono/gac/System.Web.Extensions.Design
%_prefix/lib/mono/2.0/System.Web.Extensions.Design.dll
%_prefix/lib/mono/3.5/System.Web.Extensions.Design.dll
# exes
%_prefix/lib/mono/1.0/disco.exe*
%_prefix/lib/mono/1.0/soapsuds.exe*
%_prefix/lib/mono/1.0/wsdl.exe*
%_prefix/lib/mono/2.0/wsdl.exe*
%_prefix/lib/mono/1.0/xsd.exe*
%_prefix/lib/mono/2.0/xsd.exe*
%_prefix/lib/mono/2.0/mconfig.exe*
# shell wrappers
%_bindir/disco
%_bindir/mconfig
%_bindir/soapsuds
%_bindir/wsdl
%_bindir/wsdl1
%_bindir/wsdl2
%_bindir/xsd
%_bindir/xsd2
# man pages
%_mandir/man1/disco.1%ext_man
%_mandir/man1/soapsuds.1%ext_man
%_mandir/man1/wsdl.1%ext_man
%_mandir/man1/xsd.1%ext_man
%_mandir/man1/mconfig.1%ext_man
%config %_sysconfdir/mono/browscap.ini
%dir %_sysconfdir/mono/mconfig
%config %_sysconfdir/mono/mconfig/config.xml
%config %_sysconfdir/mono/1.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/2.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/2.0/web.config
%config %_sysconfdir/mono/2.0/Browsers

%package -n mono-data-oracle
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-oracle
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-oracle
%defattr(-, root, root)
%_prefix/lib/mono/gac/System.Data.OracleClient
%_prefix/lib/mono/1.0/System.Data.OracleClient.dll
%_prefix/lib/mono/2.0/System.Data.OracleClient.dll

%package -n mono-data-postgresql
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-postgresql
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-data-postgresql
%defattr(-, root, root)
%_prefix/lib/mono/gac/Npgsql
%_prefix/lib/mono/1.0/Npgsql.dll
%_prefix/lib/mono/2.0/Npgsql.dll

%package -n bytefx-data-mysql
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n bytefx-data-mysql
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n bytefx-data-mysql
%defattr(-, root, root)
%_prefix/lib/mono/gac/ByteFX.Data
%_prefix/lib/mono/1.0/ByteFX.Data.dll
%_prefix/lib/mono/2.0/ByteFX.Data.dll

%package -n mono-nunit
License:        LGPL v2.1 or later
Summary:        NUnit Testing Framework
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%package -n mono-data-firebird
License:        LGPL v2.1 or later
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release

%description -n mono-data-firebird
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.



%files -n mono-data-firebird
%defattr(-, root, root)
%_prefix/lib/mono/gac/FirebirdSql.Data.Firebird
%_prefix/lib/mono/1.0/FirebirdSql.Data.Firebird.dll

%description -n mono-nunit
NUnit is a unit-testing framework for all .Net languages.  Initially
ported from JUnit, the current release, version 2.2,  is the fourth
major release of this  Unit based unit testing tool for Microsoft .NET.
It is written entirely in C# and  has been completely redesigned to
take advantage of many .NET language		 features, for example
custom attributes and other reflection related capabilities. NUnit
brings xUnit to all .NET languages.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-nunit
%defattr(-, root, root)
%_prefix/bin/nunit-console
%_prefix/bin/nunit-console2
%_prefix/lib/mono/1.0/nunit-console.exe*
%_prefix/lib/mono/2.0/nunit-console.exe*
%_prefix/lib/mono/gac/nunit.util
%_prefix/lib/mono/1.0/nunit.util.dll
%_prefix/lib/mono/2.0/nunit.util.dll
%_prefix/lib/mono/gac/nunit.core
%_prefix/lib/mono/1.0/nunit.core.dll
%_prefix/lib/mono/2.0/nunit.core.dll
%_prefix/lib/mono/gac/nunit.framework
%_prefix/lib/mono/1.0/nunit.framework.dll
%_prefix/lib/mono/2.0/nunit.framework.dll
%_prefix/lib/mono/gac/nunit.mocks
%_prefix/lib/mono/1.0/nunit.mocks.dll
%_prefix/lib/mono/2.0/nunit.mocks.dll
%_libdir/pkgconfig/mono-nunit.pc

%package -n mono-devel
License:        LGPL v2.1 or later
Summary:        Mono development tools
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       glib2-devel

%description -n mono-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. This package contains compilers and
other tools needed to develop .NET applications.

Mono development tools.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%post -n mono-devel
/sbin/ldconfig
if [ ! -d /opt/gnome ]; then
sed -i 's:/opt/gnome:/usr:g' %_libdir/libmono.la
fi

%postun -n mono-devel -p /sbin/ldconfig

%files -n mono-devel
%defattr(-, root, root)
# libs
%_libdir/libmono.a
%verify(not size md5 mtime) %_libdir/libmono.la
# exes
%_prefix/lib/mono/1.0/makecert.exe*
%_prefix/lib/mono/1.0/mono-api-info.exe*
%_prefix/lib/mono/2.0/mono-api-info.exe*
%_prefix/lib/mono/1.0/mono-api-diff.exe*
%_prefix/lib/mono/1.0/al.exe*
%_prefix/lib/mono/2.0/al.exe*
%_prefix/lib/mono/1.0/caspol.exe*
%_prefix/lib/mono/1.0/cert2spc.exe*
%_prefix/lib/mono/1.0/mono-cil-strip.exe*
%_prefix/lib/mono/1.0/dtd2xsd.exe*
%_prefix/lib/mono/1.0/genxs.exe*
%_prefix/lib/mono/2.0/httpcfg.exe*
%_prefix/lib/mono/1.0/ictool.exe*
%_prefix/lib/mono/1.0/ilasm.exe*
%_prefix/lib/mono/2.0/ilasm.exe*
%_prefix/lib/mono/1.0/installvst.exe*
%_prefix/lib/mono/1.0/installutil.exe*
%_prefix/lib/mono/2.0/installutil.exe*
%_prefix/lib/mono/1.0/mkbundle.exe*
%_prefix/lib/mono/2.0/mkbundle.exe*
%_prefix/lib/mono/1.0/monop.exe*
%_prefix/lib/mono/2.0/monop.exe*
%_prefix/lib/mono/1.0/permview.exe*
%_prefix/lib/mono/1.0/resgen.exe*
%_prefix/lib/mono/2.0/resgen.exe*
%_prefix/lib/mono/1.0/secutil.exe*
%_prefix/lib/mono/2.0/sgen.exe*
%_prefix/lib/mono/1.0/signcode.exe*
%_prefix/lib/mono/1.0/prj2make.exe*
%_prefix/lib/mono/1.0/macpack.exe*
%_prefix/lib/mono/1.0/mono-shlib-cop.exe*
%_prefix/lib/mono/1.0/dtd2rng.exe*
%_prefix/lib/mono/1.0/mono-xmltool.exe*
# xbuild related files
%_prefix/lib/mono/2.0/xbuild.exe*
%_prefix/lib/mono/2.0/Microsoft.Build.xsd
%_prefix/lib/mono/2.0/Microsoft.Common.tasks
%_prefix/lib/mono/2.0/Microsoft.Common.targets
%_prefix/lib/mono/2.0/Microsoft.CSharp.targets
%_prefix/lib/mono/2.0/Microsoft.VisualBasic.targets
%_prefix/lib/mono/2.0/MSBuild
%_prefix/lib/mono/2.0/xbuild.rsp
# man pages
%_mandir/man1/cert2spc.1%ext_man
%_mandir/man1/mono-cil-strip.1%ext_man
%_mandir/man1/dtd2xsd.1%ext_man
%_mandir/man1/genxs.1%ext_man
%_mandir/man1/httpcfg.1%ext_man
%_mandir/man1/ilasm.1%ext_man
%_mandir/man1/macpack.1%ext_man
%_mandir/man1/makecert.1%ext_man
%_mandir/man1/mkbundle.1%ext_man
%_mandir/man1/monodis.1%ext_man
%_mandir/man1/monop.1%ext_man
%_mandir/man1/mono-shlib-cop.1%ext_man
%_mandir/man1/permview.1%ext_man
%_mandir/man1/prj2make.1%ext_man
%_mandir/man1/secutil.1%ext_man
%_mandir/man1/sgen.1%ext_man
%_mandir/man1/signcode.1%ext_man
%_mandir/man1/al.1%ext_man
%_mandir/man1/mono-xmltool.1%ext_man
%_mandir/man1/vbnc.1%ext_man
%_mandir/man1/resgen.1%ext_man
# Shell wrappers
%_bindir/al
%_bindir/al1
%_bindir/al2
%_bindir/caspol
%_bindir/cert2spc
%_bindir/dtd2xsd
%_bindir/dtd2rng
%_bindir/genxs
%_bindir/genxs1
%_bindir/genxs2
%_bindir/httpcfg
%_bindir/ilasm
%_bindir/ilasm1
%_bindir/ilasm2
%_bindir/installvst
%_bindir/macpack
%_bindir/makecert
%_bindir/mkbundle
%_bindir/mkbundle1
%_bindir/mkbundle2
%_bindir/monodis
%_bindir/monolinker
%_bindir/monop
%_bindir/monop1
%_bindir/monop2
%_bindir/mono-api-diff
%_bindir/mono-api-info
%_bindir/mono-api-info1
%_bindir/mono-api-info2
%_bindir/mono-cil-strip
%_bindir/mono-find-provides
%_bindir/mono-find-requires
%_bindir/mono-shlib-cop
%_bindir/mono-xmltool
%_bindir/pedump
%_bindir/permview
%_bindir/prj2make
%_bindir/resgen
%_bindir/resgen1
%_bindir/resgen2
%_bindir/secutil
%_bindir/sgen
%_bindir/signcode
%_bindir/xbuild
%_mandir/man1/monolinker.1%ext_man
%_prefix/lib/mono/gac/PEAPI
%_prefix/lib/mono/1.0/PEAPI.dll
%_prefix/lib/mono/1.0/monolinker.*
%_prefix/lib/mono/2.0/PEAPI.dll
%_prefix/lib/mono/gac/Microsoft.Build.Tasks
%_prefix/lib/mono/2.0/Microsoft.Build.Tasks.dll
%_prefix/lib/mono/gac/Microsoft.Build.Framework
%_prefix/lib/mono/2.0/Microsoft.Build.Framework.dll
%_prefix/lib/mono/gac/Microsoft.Build.Utilities
%_prefix/lib/mono/2.0/Microsoft.Build.Utilities.dll
%_prefix/lib/mono/gac/Microsoft.Build.Engine
%_prefix/lib/mono/2.0/Microsoft.Build.Engine.dll
%_prefix/lib/mono/gac/Mono.Cecil
%_prefix/lib/mono/gac/Mono.Cecil.Mdb
%_bindir/monograph
%_prefix/include/mono-1.0
%_libdir/libmono-profiler-cov.*
%_libdir/libmono-profiler-aot.*
%_libdir/libmono-profiler-logging.*
%_libdir/pkgconfig/mono.pc
%_libdir/pkgconfig/dotnet.pc
%_libdir/pkgconfig/dotnet35.pc
%_libdir/pkgconfig/mono-cairo.pc
%_libdir/pkgconfig/mono-options.pc
%_libdir/pkgconfig/cecil.pc
%_mandir/man1/monoburg.*
%_prefix/share/mono-1.0/mono/cil/cil-opcodes.xml
# dirs
%dir %_prefix/share/mono-1.0
%dir %_prefix/share/mono-1.0/mono
%dir %_prefix/share/mono-1.0/mono/cil
# Reminder: when removing man pages in this list, they are not 
#  yet gzipped

%package -n mono-complete
License:        LGPL v2.1 or later
Summary:        A .NET Runtime Environment
Group:          Development/Languages/Mono
Requires:       bytefx-data-mysql = %version-%release
Requires:       ibm-data-db2 = %version-%release
Requires:       mono-core = %version-%release
Requires:       mono-data = %version-%release
Requires:       mono-data-firebird = %version-%release
Requires:       mono-data-oracle = %version-%release
Requires:       mono-data-postgresql = %version-%release
Requires:       mono-data-sqlite = %version-%release
Requires:       mono-data-sybase = %version-%release
Requires:       mono-devel = %version-%release
Requires:       mono-extras = %version-%release
Requires:       mono-jscript = %version-%release
Requires:       mono-locale-extras = %version-%release
Requires:       mono-nunit = %version-%release
Requires:       mono-web = %version-%release
Requires:       mono-wcf = %version-%release
Requires:       mono-winforms = %version-%release

%description -n mono-complete
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files -n mono-complete
%defattr(-, root, root)
# Directories
# Put dir files here so we don't have an empty package
%dir %_prefix/lib/mono/compat-1.0
%dir %_prefix/lib/mono/compat-2.0

%prep
%setup -q -n mono-%{version}

%build
# These are only needed if there are patches to the runtime
#rm -f libgc/libtool.m4
#autoreconf --force --install
#autoreconf --force --install libgc
export CFLAGS=" $RPM_OPT_FLAGS -DKDE_ASSEMBLIES='\"/opt/kde3/%{_lib}\"' -fno-strict-aliasing"
# distro specific configure options
%{?configure_options}
%configure \
  --with-jit=yes \
  --with-ikvm=yes \
  --with-moonlight=yes
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
# Remove unused files
rm $RPM_BUILD_ROOT%_libdir/libMonoPosixHelper.a
rm $RPM_BUILD_ROOT%_libdir/libMonoPosixHelper.la
rm -f $RPM_BUILD_ROOT%_libdir/libikvm-native.a
rm -f $RPM_BUILD_ROOT%_libdir/libikvm-native.la
rm -fr $RPM_BUILD_ROOT%_prefix/lib/mono/gac/Mono.Security.Win32/[12]*
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/Mono.Security.Win32.dll
rm $RPM_BUILD_ROOT%_prefix/lib/mono/2.0/Mono.Security.Win32.dll
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.DGUX386
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.Mac
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.MacOSX
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.OS2
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.amiga
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.arm.cross
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.autoconf
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.changes
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.contributors
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.cords
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.darwin
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.dj
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.environment
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.ews4800
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.hp
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.linux
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.macros
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.rs6000
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.sgi
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.solaris2
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.uts
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/README.win32
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/barrett_diagram
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/debugging.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gc.man
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gcdescr.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/gcinterface.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/leak.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/scale.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/simple_example.html
rm $RPM_BUILD_ROOT%_datadir/libgc-mono/tree.html
rm $RPM_BUILD_ROOT%_mandir/man1/cilc.1
rm $RPM_BUILD_ROOT%_mandir/man1/monostyle.1
rm $RPM_BUILD_ROOT%_mandir/man1/oldmono.1
rm $RPM_BUILD_ROOT%_mandir/man1/mint.1
# Things we don't ship.
# cilc
rm $RPM_BUILD_ROOT%_bindir/cilc
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/cilc*
# jay
rm $RPM_BUILD_ROOT%_bindir/jay
rm -R $RPM_BUILD_ROOT%_datadir/jay
rm $RPM_BUILD_ROOT%_mandir/man1/jay.1
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/CorCompare.exe
rm $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/browsercaps-updater.exe*
# New files to delete in 1.1.9.2
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.a
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.la
rm -f $RPM_BUILD_ROOT%_libdir/libMonoSupportW.so
# 1.1.17 updates:
# This file moved to mono-basic
rm -f $RPM_BUILD_ROOT%_bindir/mbas
# 1.2.4 changes
rm -f $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/culevel.exe*
# Post 1.2.5
rm -f $RPM_BUILD_ROOT%_prefix/lib/mono/1.0/transform.exe
# brp-compress doesn't search _mandir
# so we cheat it
ln -s . %buildroot%_prefix/usr
RPM_BUILD_ROOT=%buildroot%_prefix /usr/lib/rpm/brp-compress
rm %buildroot%_prefix/usr
%find_lang mcs

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
* Tue Aug 26 2008 ajorgensen@novell.com
- Update to 2.0 (preview 2)
  * Runtime: Performance
  * The performance of operations on decimals has significally improved.
  * The performance of locking (Monitor.Enter/Monitor.Exit) is significally improved.
  * The memory usage of the runtime is reduced, especially when using generics.
  * Many race conditions and threading problems were fixed, improving reliability.
  * Math.Min/Math.Max and some forms of Interlocked.CompareExhange (CAS) are now implemented using fast inline code on x86/amd64.
  * There is now a MONO_DEBUG=dont-free-domains option that improves the performance of ASP.NET-based applications.
  * Runtime: Features
  * Some progress has been made on the Winx64 port [Bill Holmes, Jonathan Chambers]
  * The runtime is now built using the dolt libtool replacement (http://dolt.freedesktop.org/) this speeds up runtime compilations by about 30%%.
  * The runtime build process is now less verbose on some platforms, similar to the way the linux kernel is built. To turn it off, use the --enable-quiet-build=no argument to configure, or pass the V=1 argument to make.
  * There is now a --debug=casts command line option to the runtime which turns on the reporting of better InvalidCastException message details.
  * The mono_method_get_unmanaged_thunk () function has been implemented for developers embedding Mono which simplifies calling managed methods from unmanaged code.
  * C# Compiler
  * The compiler now support expression trees (turning expressions into an AST at compile time when the type of a parameter is a System.Query.Expression). This completes the C# 3.0 support.
  * Over 60 reported bugs in the compiler were fixed and many of the internals have been cleaned up. Extensive refactoring and hardening of the C# 2.0 and 3.0 support are now better integrated.
  * A major rewrite of the anonymous method/lambda support in the internals of the compiler now optimizes the resulting code, and fixes several bugs in this area.
  * The compiler is now dual licensed under the MIT X11 and the GNU GPL version 2 (only).
  * The compiler now supports #pragma checksum for use with ASP.NET debugging and #line hidden, as well as flagging more compiler-generated code properly (to avoid the debugger single-stepping into those bits).
  * LINQ
  * LINQ and LINQ to XML are now complete, support for expression trees is now available as well as the backend to support expression tree compilation.
  * LINQ to Dataset has also been implemented.
  * Performance Counters Implementation
  * Mono now has a performance counters implementation that can be used to monitor various statistics of Mono processes. To access this API you use the System.Diagnostics.PerformanceCounter classes.
  * Big Arrays
  * Mono now supports 64-bit indexed arrays on 64-bit systems. Although this is permitted by the ECMA standard, this today is a unique feature of Mono as .NET on Windows does not support 64-bit array indexes. This code was developed by Luis Ortiz at Interactive Supercomputing and integrated by Rodrigo Kumpera.
  * This feature is useful for developers that needs to manipulate very large data sets with C# arrays.
  * To use this feature, you must configure Mono with --enable-big-arrays.
* Mon May 26 2008 crrodriguez@suse.de
- add missing zlib-devel BuildRequires this made mono to
  use a bundled copy a zlib.
* Mon May 12 2008 aj@suse.de
- Do not return random data in function.
* Tue May 06 2008 schwab@suse.de
- Don't use libtool before it is created.
* Fri Apr 25 2008 wberrier@suse.de
- Make sure x11 headers/libs are installed so that
  /etc/mono/config has correct link to libX11.so.6.
  Fixes (bnc#339712)
* Tue Apr 22 2008 wberrier@suse.de
- Update to 1.9.1 (bugfix release)
 -G_DECL fixes
 -Microsoft.CSharp: Emit bodyless getters and setters for abstract
  properties
 -ASP.NET: Don't output a date header from System.Web
 -Fix an issue with Groupwise WSDL
 -Mono.Mozilla: Support more than one browser widget per
  application Windows.Forms
 -Winforms:
  -Finish implementation for EventsTab and PropertiesTab
  -Fix keyboard layout issue
  -MenuAPI fixes
 -System.Design: Cache editor widget instead of creating it each
  time
 -System.Text: Fix possible integer overflow
 -System.Net.Mail: Fix filename handling
* Fri Apr 11 2008 schwab@suse.de
- Work around broken configure script.
* Fri Apr 11 2008 aj@suse.de
- glibc does not define ARG_MAX anymore, use sysconf (_SC_ARG_MAX)
  instead.
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Tue Mar 25 2008 wberrier@suse.de
- Filelist changes for System.Xml.Linq and Mono.Web
- Call ldconfig directly instead of invoking a shell
- Update to 1.9
 -More than 80 bugs closed/fixed in the runtime
 -Reflection bug fix
 -C# compiler defaults to 3.0
 -Silverlight support enabled by default
 -Generics code sharing
 -AOT support for ARM
 -Verifier improvements
 -Updated Core Linq api
 -Now includes System.Xml.Linq
 -mcs/gmcs parser code base has been unified
 -ASP.Net:
  -Batch Compilation
  -Mapping configuration
 -Winforms:
  -more support for browser events
  -Several fixes to RichTextBox
  -Major improvements to PropertyGridControl
  -Over 100 fixed bugs
 -System.Design implementation
 -DLR support
 -Mono.Posix:
  -Stdlib.signal() has been deprecated.  Replaced with:
   -Mono.Unix.Native.Stdlib.SetSignalAction
   -Mono.Unix.UnixSignal
* Thu Feb 14 2008 dmueller@suse.de
- only require valgrind for archs that provide it
* Wed Jan 23 2008 wberrier@suse.de
- mono-93665_find_requires_ignore_missing.patch: warn on missing
  files found in .config files instead of generating invalid deps.
* Wed Jan 16 2008 wberrier@suse.de
- libgdiplus -> libgdiplus0 rename
- add libgluezilla0 to recommends
* Mon Jan 14 2008 wberrier@suse.de
- Update to 1.2.6
 -Support for the ASP.NET AJAX APIs and controls
 -Support for FastCGI deployments
 -Windows.Forms WebControl for Windows and Linux using Mozilla
 -Reduced memory usage in the runtime for 2.0 apps
 -Updated verifier
 -Implementation of CoreCLR security
 -More C# compiler 3.0 completion
 -Mono 1.2.6 can now be used as an SDK for creating Silverlight
  1.1 applications on all platforms.
 -Support for the PE32+ assembly file format
 -Managed allocations support
 -SslStream support
 -System.Net.Mail improvements
 -Fixed SSL/TLS thread-synchronization
  (for LDAPS over multiple threads)
 -Novell.Directory.Ldap synchronized with the Novell's CSHARP
  LDAP SDK (version 2.1.8)
* Tue Oct 23 2007 wberrier@suse.de
- mono-boo_ia64_fix.patch: fix boo build on ia64.
* Wed Sep 19 2007 wberrier@suse.de
- BigInteger Security fix: bnc #310044
 -MaintenanceTracker-13335
* Thu Aug 30 2007 wberrier@suse.de
- Regressions found in 1.2.5:
 -Bug #82428: crypto buffer length fix
 -Bug #82481: StatusStrip focus regression fix
 -Bug #82499: GlobalReAlloc fix
- System.Web regression fixes:
 -Bug #82193: System.Web regression fixes
 -Bug #82392: SessionState fix for asp.net regression
* Fri Aug 17 2007 wberrier@suse.de
- Fix some COM and Winforms regressions in 1.2.5 p3
 -fixes bxc: 82433, 82344, 82405, 82406, #82187, 82348
- Threading fix for bxc #82145 when using LDAP and TLS
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -Fixes for IronPython and Dynamic Language Runtime
 -More C# 3.0 compiler features
 -2.0 support for AOT assemblies
 -Several performance improvements when running IronPython
 -Reduced virtual table sizes
 -Optimized double to int conversions using SSE2 on x86
 -Proper caching of generic methods
 -IL verifier implemented
 -HttpWebRequest can now be used with X.509 client certificates
 -Added support X.509 Client Certificate Chains for SSL/TLS
 -Fixed SSL/TLS not to require exportable private keys for
  client certificates
 -Implemented import and export of DSA keys CryptoAPI-compatible
  BLOB (2.0)
 -Added SafeBag handling to Mono.Security's PKCS#12
 -Regioninfo support
 -Optimized dictionary type
 -New TimeZone implementation
 -new 2.0 Winform controls: MaskedTextBox, ToolStripPainter,
  ToolStripSystemRenderer
 -Mono Cairo API has been updated, it will now expose Cairo
  1.2 API entry points.
- Don't use 64bit libs on ppc64 in find-requires (runtime is 32bit,
  must use 32bit libraries)
* Mon Jul 30 2007 ro@suse.de
- try to use 64bit libs on ppc64 as well in find-requires
* Tue Jul 10 2007 wberrier@novell.com
- Build against valgrind for 10.3 and above
* Thu Jul 05 2007 wberrier@novell.com
- mono-find-requires fixes for ia64 (bnc #282877)
* Wed Jun 20 2007 ro@suse.de
- removed requires on specific release in mono-complete for
  mono-basic (not a subpackage of mono-core anymore)
* Fri Jun 15 2007 wberrier@novell.com
- mono-config_rpm_requires.patch: revert back to using package
  requirements for the .config dep scanning.  This is because
  noarch packages can be built on either 32 or 64 bit machines,
  and then otherwise will depend on a 32 or 64 bit library, which
  is wrong.
* Tue Jun 05 2007 wberrier@novell.com
- Fix relevant rpmlint errors/warnings:
 -also 'provides' for each 'obsoletes'
 -run ldconfig in post/un for mono-core and mono-devel
- Update filelists
- Update to 1.2.4
 -680 new methods implemented.
 -290 stubs that used to throw NotImplemented exceptions have been
  implemented.
 -43 methods flagged with "to-do" have been implemented.
 -Fixed HandleRef support
 -Ability to disable shared mem support
 -Mostly complete ASP 2.0 support (webparts is missing)
  -asp.net 2.0 performance tripled
 -C# 3.0 compiler support
 -Mono.DataConvert: fixed implementation of the broken
  System.BitConverter
 -System.Windows.Forms
  -150 bugfixes
  -performance fixes
  -2.0 profile additions: ToolStrip, Baloon tips, and hundreds of
  new methods in various controls
 -System.Drawing
  -Initial support for metafiles (wmf & emf)
  -performance improvements and fixes
  -Many printing fixes
 -2.0 ADO.Net updates
 -Support for amd64 on Solaris
 -Security and Crypto:
  -Path.GetTempFileName now returns a file with 600 perms
  -Fixed HMACSHA384 and HMACSHA512 to use a 128 bits block size
  -Signcode tool now support password-protected PVK files
  -CryptoStream.Write is now closer to MS behaviour and requires
  less memory
  -Fixed endian issue in RIPEMD160
 -installvst: new tool to install VisualStudio source packages
 -New additional sqlite binding: Mono.Data.Sqlite
  -better maintained (http://sqlite-dotnet2.sourceforge.net/)
  -sqlite3 only (no sqlite2, would need to dump/reload db)
 -COM Interop now supports COM Callable Wrappers
 -Many of the new 2.0 socket methods are now available
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 04 2007 wberrier@novell.com
- Adapt for build service
* Mon Mar 05 2007 wberrier@suse.de
- atomic fixes from Michael Matz for for s390 and s390x
  ( bnc #237611 and bxc #80892 )
* Wed Feb 28 2007 wberrier@suse.de
- Turn off sigaltstack, as it's not safe (Requested by Paolo)
- Remove obsolete patches
- Update to 1.2.3.1 (Various runtime and winforms crashers
  as well as a zmd crasher)
- 1.2.3 Changes:
 - 1,933 missing methods were implemented.
 - 164 methods with pending implementations were fixed.
 - Improved Winforms 2.0 Support, with additional controls, and
  reduced memory usage
 - API complete ASP.NET 2.0 implementation (except for WebParts).
 - System.Media implementation
 - Supports SOAP 1.2 as well as the WS-BasicProfile 1.1 checker
 - Many fixes to the XmlSerializer as well to support the new features
 - The mkbundle tool now allows the machine.config file to be embedded
  as well
 - HttpListener now also support HTTPS, to configure the certificates
  use the httpcfg tool
 - Completed the support for the 2.0 updates to the API in
  System.Net.Sockets
 - System.Drawing.SystemIcons are now implemented
 - Authenticode: Signcode now generates valid signature on PE
  files with extra data (e.g. debug information, installers)
  and for file length that aren't multiple of eight
 - SSL/TLS: Fix negotiation cache and added configurable cache
  timeout using the MONO_TLS_SESSION_CACHE_TIMEOUT environment variable
 - XML Signature and XML Encryption: several bug fixes, it now it
  support exclusive canonicalization (needed for ongoing Olive work)
 - Support for inherited key parameters in DSA certificates
 - Support for DSA certificates in PKCS#12 files
 - Better support for X.509 CRL (including stores & certmgr support)
 - xbuild improvements
 - Sqlite 2.0 API support
 - Array and multi-array access optimizations
 - Versioned header files
* Sat Jan 20 2007 wberrier@suse.de
- Move libgdiplus requirement from mono-winforms to mono-core
  since System.Drawing (in mono-core) is useless without it
  (Won't affect mono-winforms, since it depends on mono-core)
* Tue Jan 09 2007 wberrier@suse.de
- Move mono-find-provides/requires to mono-devel since they depend
  on monodis, which is in mono-devel
- Patch mono-rpm_deps_error_handling_r70445.patch to error out
  when running the find scripts
- Fixes bnc #227362
* Fri Dec 01 2006 wberrier@suse.de
- Update to 1.2.2 (Fate #301111)
 -Serious bug fix in compiler (anonymous methods)
 -Additional 2.0 APIs implemented for Windows.Forms
 -Removal of many incorrect MonoTODOs and implemented many methods
  that were throwing not implemented exceptions
- Changes in 1.2.1
 -Thread.Interrupt is implemented
 -Generics support in Web Services
 -Web Services update for 2.0 api
 -ASP.Net 2.0 updates
 -Several Winforms blockers fixed
 -ADO.Net 2.0 updates
 -Support for more type converters
 -Process launching supports supports open special files in addition
  to launch programs (ie: xdg-open, gnome-open, or kfmclient)
 -System.Drawing UTF8 to UCS2 conversion fixed
 -2.0 api updates to X.509 related classes
- Changes in 1.2
 -Serialization Callbacks
 -Machine-level settings now available in registry
 -Winforms completion
* Thu Nov 30 2006 wberrier@suse.de
- Thread safety fixes for rug/zmd (bnc #221277)
- System.Web Source fix (bnc #225179)
* Tue Nov 14 2006 meissner@suse.de
- Disable executable stack option. #65536
* Fri Oct 20 2006 wberrier@suse.de
- Remove glib2-devel from mono-nunit, not sure why it was ever there
  (bnc #210224)
- Updated to 1.1.18.1
 -removed upstream patches
 -C# Generics fixes
 -IO Layer changes to ease windows porting migration
 -Security updates: major speed improvements
 -Lots of Winforms fixes and updates
 -Merged source for mcs and gmcs
 -Performance tuning
* Thu Sep 28 2006 wberrier@suse.de
- Security fix for bnc #205084 VUL-0
- TempFileCollection.cs: Create files in a temporary subdirectory,
  for security reasons.
- CodeCompiler.cs: Let TempFileCollection choose the temp dir.
* Fri Sep 01 2006 wberrier@suse.de
- Update to 1.1.17.1 - Minor bugfix update
- Fix HttpListener, it was failing with a few post operations
- mono-service is now installed into the GAC, the recent changes
  broke applications that created new AppDomains
- Fix a race condition on array new
* Tue Aug 29 2006 wberrier@suse.de
- add s390 backchain patch
- s390 warnings patch
- remove mono-basic package
- update filelist for CustomMarshalers
- Update to 1.1.17
 - Windows.Forms: Printing is now supported.
 - Basic COM support has been integrated.
 - FileSystem will now use inotify directly on systems that
  support it without having to go through an external library like
  FAM or Gamin [Gonzalo Paniagua]
 - 2.0 support for asynchronous reads and writes from the
  Process class is now supported [Gonzalo]
 - Fxied Loading as a Shared Library
 - Mono.Cairo bindings now supports a DirectFB surface now [Alp Toker]
 - Process now support the async io handling [Gonzalo Paniagua]
 - String.Normalize is included [Atsushi Enomoto]
 - ADO.NET 2.0 updates, included an implementation for
  SqlConnection.GetSchema (Nagappan, Nagappan).
 - Registry Updated to the 2.0 API. [Miguel de Icaza]
 - Support for splitting the registry across user and system level
  settings. [Gert Driesen]
 - Support for X.509 client certificates
  [Hubert Fongarnand, Sebastien Pouliot]
 - SN accepts password-protected PKCS#12/PFX files to strongname
  assemblies. This feature is enabled in both 1.x and 2.0 profiles
  [Sebastien Pouliot]
 - CodeDOM JScriptCodeProvider code JavaScript code is now
  included [Akiramei]
 - An EventLog implementation is available on both Unix and
  Windows by setting MONO_EVENTLOG_TYPE
 - COM Interop: Basic support for Runtime Callable Wrappers
  (RCWs) [Jon Chambers]
 - Sqlite now exposes a Version property to detect which underlying
  database is available (2.x or 3.x) [Joshua Tauberer]
 - Mono.Posix now features an abstract Unix end point in addition
  to Unix End Points [Alp Toker].
 - Fixed XmlSchemaSet and XmlSchemaCollection problem across
  multiple namespaces [Atsushi Enomoto]
 - Important Bug fixs:
  - Dynamic linking of Mono is now possible in applications
  that were using the TLS (open office) [Zoltan Varga]
  - Newly created AppDomains no longer inherit the list of
  loaded assemblies from the main domain [Lluis Sánchez]
  - A number of missing pieces of System.IO.Ports have been
  implemented (ReadChar, ReadLine, BytesToRead, BytesToWrite,
  ReadTo, return USB tty devices) [Miguel de Icaza]
  - ASP.NET Cache will now check dependencies (79002)
  [Gonzalo Paniagua]
  - Updated the Posgress data bindings to RC3
  [Francisco Figueiredo].
- --------
- Satisfy some compiler warnings with more warnings patches
- Update filelists
- Add sigaltstack configure option for performance
- Update to 1.1.16.1
- Sending the QUIT signal to a running Mono process will produce
  a stack trace of each thread
- Updated Boehm garbage collector
- Large file uploads are now supported
- Updated Master Pages, nested pages and System.Configuration
- Improved performance for XML
- Added support for abbreviated handshakes
- Fixed some possible deadlocks while negotiating
- basic implementation of System.Transactions
- implemented assembly unloading when an appdomain is released
- C# Compiler bug fixes:
 - #78020, #77916, #77961, #78048, #77966
 - Improved the generated output for array initialization
 - #77958, #77929, #77954
 - #77002
- XMLSerialization implemented for XmlSchemas
- improved performance of Int32.ToString()
- major updates to System.Windows.Forms and System.Drawing
- inline optimization enabled by default
- Long standing debugging line numbers bug fixed
* Thu Jun 15 2006 wberrier@suse.de
  Changes from Neale Ferguson <neale@sinenomine.net> from trunk in order
  to fix bnc #179080 (zmd issue on s390x)
- * atomic.h: Fix atomic operations for s390x (not really broken
  but changed to use full 64-bit opcodes).
- * atomic.h: Fix atomic exchange pointer operations for s390x - these
  were broken as they used 32-bit instructions rather than their 64-bit
  versions.
- * s390x-codegen.h: Fix immediate checks.
* Mon May 15 2006 wberrier@suse.de
- Revert change to mono-find-provides (59882) so that Mono apps will
  not have to depend on being able to find dependent assemblies in
  the gac.
* Wed May 10 2006 wberrier@suse.de
-Add provides for mono-core for assemblies not in the gac, which
  other packages depend on.
-Update to 1.1.13.8 from stable branch
-Assembler:
 -Fix assembler bug that tried to sign netmodules.
 -Assembler will now report a bug if two identical labels are declared
  on the same methods
 -On 2.0, support the "property" directive.
-ASP.NET:
 -Make sure application start event is run before the request is
  processed.
 -Dont reset query string in Execute (78177).
 -Make sure that we can read a file before trasmitting it (fixes
  crash).
 -Added two tests (Bug 78101, DataSourceID).
 -Do not fail on events that do not derive from EventHandler,
  patch from Matthew Metnetsky.
 -Render some attributes inside span, not div tags (71251).
 -Fix searching of control by DataSourceID.
-System.NET:
 -Allow posts of size zero (#78316)
 -Fix for proxy authentication over HTTPS, for Zen team (78150).
-Core:
 -Do not capture compressed stack, this feature is not yet
  supported, fixes a crasher bug in ExecutionContext.
 -Add FileOptions, necessary for IronPython.
 -Fix incorrect buffer reading from console (78218).
-Mono.Security:
 -Enable abbreviated handshake for SSL3 (Zen)
 -Deal with emtpy master secrets (78085)
-Tools:
 -Fix mono-find-provides, to not list private copies of
  assemblies (fixes conflict of MonoDevelop and third party
  rpms).
-Runtime:
 -Fix for 78035.
 -Avoids a null dereferences in metadata, IPHostEntry
 -x86-64: Fix handling of MONO_INST_GENERICINST
 -Memory leak fix, when shutting down threads, clean the TLS:
  77470.
 -Handle multiple leave statements in a try/catch, 78024.
-Compilers:
 -Flag VB as unsupported.
* Mon Apr 24 2006 wberrier@suse.de
- Bug fixes for Zenworks (78089, 78150, amd64 signal crash, and proxy fix in System.Net)
* Mon Apr 10 2006 wberrier@suse.de
- Branch update for iFolder issues.  Also includes some semaphore
  updates, as well as SWF updates. (77931,01234,77931,01234,77991,
  77556,77811,77350,75609,78028,77971,78033,77242,76191,41943,77890,
  78067,78067,78067,77514,77839,77393)
* Mon Apr 10 2006 cthiel@suse.de
- remove redundant Conflicts lines (#159340)
* Mon Mar 27 2006 aj@suse.de
- Apply patch from Dick Porter to Break out of a loop if the
  shared file is smaller than expected - this fixes some build
  issues.
* Sat Mar 25 2006 wberrier@suse.de
-Update to 1.1.13.5 (No crypto changes)
 -C# compiler bug fixes for Bugzilla.ximian.com bugs: 77767,
  77642, 77583, 77674, 77642 as well as fixing a number of
  nullable bugs (gtest-254, gtest-251, gtest-250) fixed
  compilation bugs for C5 library.
 -Sqlite bindings now has a way of specifying the default
  encoding and defaults to UTF-8 instead of using ANSI.
  Versions between Jan 20 and this release stored data always in
  ANSI format which could not be read back.
 -System.Web: invoke validation callbacks in HttpCachePolicy
  (77825); fixes OutputCache's VaryByParam="*" (77757); fix
  Cache-Control header handling (77825); Fix POST filename
  encodings (77714);  Allows setting custom Cache-Control
  headers (77775).
 -System.Web/HtmlControls fixes from Mainsoft: fixed
  Anchor.RenderAttributes, Form.Method fixed to include "post"
  if needed; InputImage fixed to cope with SetAtt.
 -System.Web's SessionState: session state will retry
  reconnecting to the database if the connection is lost
  (77785).   Dispose the data reader to avoid leaks (77698);
 -System.Web Javascript, hide validators view (77261).
 -System.Web's/WebControls: Use naming container instead of
  pages to locate controls (77793);   Fixes rendering of
  ListBoxes (77740);
 -System.XML.Schema: fix return value on the XML Schema
  (77685).
 -XmlSerialization: consider subtypes (77447), ignore element
  namespaces when using Unqualified mode (75019).
 -IO-Layer: close redirected pipes on errors (77514), Shell
  Execute, avoid crash (77393);  Delete semaphores on last exit
  (City of Largo request, problem happens in clusters, direct
  communication, no bug#).
 -WebConnectionStream: avoid async calls when writing zero
  bytes (iFolder CPU consumption issue).
 -HttpWebRequest: fix close semantics (77753)
 -UpdClient: fix IPV6 family check (77689).
 -System.Data fixes: Fixed 77557, 77776 and enabled tests
  that were previously disables, add new tests.
 -System.Data: Fixed endianess bugs reported on PPC and
  SPARC.
 -Runtime: Updates for LocalDataStoreSlot to prevent the
  Beagle leak from happening; Fixed crasher bug in class
  libraries (77772).  Fixes 77504 in generic libraries; Fix
  Stream bug 77863; Reflection fix for 74937; Stat-usage fixes
  (77759, 76966); public-key-token casing (77898); Codebase
  return fix (77877); fix two ia64 crashes (77774, 77787);
  Handle null in Equals (77700); backport memory corruption fix
  (no bug number);
 -Tracing: Fix crash in StringBuilders when tracing (77848);
  disable output always 77706.
 -S390x: Use long-displacement if the CPU supports it.
 -Patch from Tambet at ZenWorks team to reduce memory
  consumption in remoting, shaves a few megabytes on RPC calls.
 -System.Drawing/Windows.Forms: Bring code from trunk (these
  are unsupported libraries).
 -Mono.Security: several fixes to the async stream handling
  in SSL: implement a ClientSessionCache, redo the async
  processing of requests as they were previously hanging iFolder
  (77663, 67711).  There were no changes to the crypto code.
 -Upgraded C5 test suite to 1.0 release from upstream.
 -Updated debugger API.
 -Added tests for bugs fixed.
 -Fix: s390 and s390x will enable the JIT without special
  flags (before we needed --enable-jit).
 -Prj2Info escapes now characters in filenames that contain
  special shell characters.
* Wed Mar 01 2006 aj@suse.de
- Remove echo in %%post.
* Tue Feb 28 2006 wberrier@suse.de
- Update to 1.1.13.4
 -Fixes the following bugs: 77524 77581 75479 77637 77613 77446 77433 77398 77397 77315 75436 75479 77521 77536 77572 77468 77371 77273 77309 74932 77442.... too many to list here.
* Sat Feb 18 2006 ro@suse.de
- use wildcards in filelist (.mdb files moved to debuginfo package)
* Thu Feb 16 2006 wberrier@suse.de
- have winforms rpm depend on libgdiplus (Novell Bug #150858)
* Thu Jan 26 2006 ro@suse.de
- warn if installing on s390/G5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 20 2006 wberrier@suse.de
- Update to 1.1.13.2 (no crypto updates)
* Thu Jan 12 2006 wberrier@suse.de
- Update to 1.1.13.1 (no crypto updates)
  Fix for CASA
* Fri Jan 06 2006 wberrier@suse.de
- Update to 1.1.13 (No crypto updates)
  FireBird 2.0 gac file was disabled
  Added nunit-console to filelist
* Fri Dec 23 2005 wberrier@suse.de
- Add some of Zoltan's ia64 fixes to fix the runtime (no crypto updates)
* Thu Dec 22 2005 wberrier@suse.de
- Update to 1.1.12.1 (ziplib fix, no crypto updates)
* Wed Dec 21 2005 wberrier@suse.de
- Add patches fro Neale's s390 checkins (No crypto updates)
* Wed Dec 21 2005 wberrier@suse.de
- Fix mono-cairo.pc for gtk-sharp2 build on x86_64
* Mon Dec 19 2005 wberrier@suse.de
- Update to 1.1.12, monoburg warning patch
* Fri Dec 16 2005 ro@suse.de
- add an explicit cast on ppc for InterlockedCompareExchangePointer
* Thu Dec 15 2005 wberrier@suse.de
- Update to 1.1.11, add files for 1.1.11, and enable some files (libmono.l?a)
* Mon Dec 12 2005 sbrabec@suse.cz
- Added "Obsoletes: mono" to mono-core.
* Fri Nov 11 2005 wberrier@suse.de
- Fix build (supportw.c)
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10.  Add profiler-aot, mozroots
* Thu Oct 20 2005 ro@suse.de
- try to fix req/prov scripts
- remove AC_DISABLE_FAST_INSTALL to fix installed binaries
- do not build as root
* Wed Oct 12 2005 ro@suse.de
- take fix for gacutil problem from SVN
- remove workaround hack from specfile
* Wed Oct 12 2005 ro@suse.de
- fix some lib64 issues
* Tue Oct 11 2005 wberrier@suse.de
- Update to 1.1.9.2, restructure packages to match upstream
* Mon Sep 26 2005 ro@suse.de
- fix build on x86_64
- move mono-nunit.pc to mono-nunit package
* Thu Sep 22 2005 wberrier@suse.de
- Reenable 2.0 preview (bug #118530)
* Fri Sep 16 2005 wberrier@suse.de
- Nasty work around hack for libtool in order to not include wrappers (#116245)
* Thu Sep 08 2005 ro@suse.de
- fix build on 9.1+
* Tue Aug 23 2005 wberrier@suse.de
- Add the mono-nunit subpackage (needed for mono-tools)
* Mon Aug 01 2005 ro@suse.de
- update to 1.1.8.3
* Thu Jul 14 2005 wberrier@novell.com
- Update %%file directives for SymbolWriter
* Sun Jun 26 2005 ro@suse.de
- use ldscript only for "libmono" but not for "mono"
* Wed Jun 22 2005 ro@suse.de
- fix more warnings on ppc
* Tue Jun 21 2005 ro@suse.de
- update to 1.1.8.1
* Tue Jun 21 2005 ro@suse.de
- revisit execstack : pass with "-Wl" as linker flag
* Tue Jun 07 2005 uli@suse.de
- s390: moved __attribute__((packed)) where it is not ignored by
  the compiler (fixes SIGILLs/SIGSEGVs in several packages)
* Sat May 14 2005 aj@suse.de
- mono-data-* needs mono-data.  Require it explicitely.
* Fri May 13 2005 ro@suse.de
- fix assembliesdir in libexecdir patch again
* Thu May 12 2005 uli@suse.de
- update -> 1.1.7
- disabled s390x (port is broken and unmaintained)
* Mon Mar 21 2005 mmj@suse.de
- Add dependency for mono-devel on glib2-devel [#74161]
* Tue Mar 15 2005 gekker@suse.de
- Add mono-sys-web.patch and mono-leak-fix.patch for mono team
* Fri Mar 11 2005 gekker@suse.de
- Add mono-libgc-finalizer-fix.diff for the mono team
* Fri Mar 11 2005 uli@suse.de
- s390* workaround (build with -O1)
- fixed a bunch of (harmless) warnings to appease autobuild
* Thu Mar 10 2005 gekker@suse.de
- add mono-sqlite2-config.patch (71844).
* Mon Mar 07 2005 gekker@suse.de
- add mono-mini-threadfix.diff, to fix random crashes in mcs
* Tue Mar 01 2005 gekker@suse.de
- remove sqlite2-devel crack from requires for mono-data-sqlite
* Mon Feb 21 2005 clahey@suse.de
- Update to 1.1.4.
* Sun Feb 20 2005 ro@suse.de
- expand configure macro (not always correct for old distributions)
- more hacks to java path
* Sun Feb 20 2005 ro@suse.de
- changed java path
* Sat Feb 19 2005 ro@suse.de
- fix build for older distributions (without jni)
* Thu Feb 17 2005 gekker@suse.de
- Add requires to mono-data-sqlite for sqlite2 and sqlite2-devel
* Tue Feb 15 2005 gekker@suse.de
- add -z execstack to LDFLAGS (50536)
* Sun Feb 06 2005 ro@suse.de
- fix mono with exec stack protection
* Tue Feb 01 2005 ro@suse.de
- fix mono-provides
* Mon Jan 31 2005 gekker@suse.de
- fix a directory ownership problem
* Mon Jan 31 2005 ro@suse.de
- fix build on lib64 (again ...)
* Mon Jan 31 2005 ro@suse.de
- fix setup line in spec file
* Mon Jan 31 2005 clahey@suse.de
- Split into separate packages.
* Wed Jan 12 2005 ro@suse.de
- update to 1.1.3
* Sun Nov 28 2004 ro@suse.de
- THREAD_LOCAL_ALLOC is not possible on ppc, don't force it
- extended 64bit-warning patch some more
- configure "with-jit=yes" as in sles9
* Fri Nov 12 2004 ro@suse.de
- update to 1.1.2 devel branch
- added hacks to use libexecdir (always /usr/lib/mono)
  (but mcs still doesn't use it)
* Wed Sep 15 2004 ro@suse.de
- updated to 1.0.1 bugfix release
* Fri Jul 02 2004 ro@suse.de
- updated 64bit-warning patch (from clahey)
* Fri Jul 02 2004 ro@suse.de
- update to 1.0 version
* Mon Jun 28 2004 mls@suse.de
- use find-requires and find-provides from rpm
* Mon Jun 21 2004 clahey@suse.de
- Updated to 0.96.
- Added find-requires.mono and find-provides.mono.
* Wed Jun 09 2004 clahey@suse.de
- Don't include wine stuff.
* Wed May 26 2004 clahey@suse.de
- Require icu and libiuc26.
* Tue May 25 2004 clahey@suse.de
- make clean before make to remove incorrectly disted file.
- As long as we're conflicting with pnet-compiler, we shouldn't
  move ilasm to milasm as that messes things up for mono and isn't
  necessary.
* Tue May 25 2004 adrian@suse.de
- fix permissions of -devel package
  (Requires base mono package and conflicts with pnet-compiler)
* Mon May 24 2004 clahey@suse.de
- Don't try to include wine files on non x86 platforms.
* Fri May 21 2004 clahey@suse.de
- Updated to 0.91.
* Tue Apr 20 2004 uli@suse.de
- ditch JIT runtime on PPC as it does not work properly yet
- add winelib on x86 to allow use of Win32 APIs as provided by WINE
- require libgdiplus
* Mon Apr 19 2004 uli@suse.de
- update -> 0.31 as reqd by gp
* Wed Feb 18 2004 uli@suse.de
- update -> 0.30.1 as reqd by gp
* Mon Feb 09 2004 uli@suse.de
- fixed to build on s390
* Thu Feb 05 2004 uli@suse.de
- update -> 0.30 (proper fix for Write/WriteLine problem,
  obsoletes several patches)
- build libgc/finalize.c with -fno-strict-aliasing
* Wed Feb 04 2004 uli@suse.de
- renamed ilasm to milasm to avoid conflict with Portable.NET
* Fri Jan 30 2004 uli@suse.de
- removed incompatible System.Console.Write/WriteLine methods to
  make mcs-compiled binaries work with Portable.NET and MS.NET
* Wed Jan 28 2004 uli@suse.de
- disable exception tables, do not work with glibc 2.3 yet
- build class libs and tools from source (not on PPC, fails with
  null pointer exception)
- compat link for archs without JIT
* Mon Jan 26 2004 uli@suse.de
- initial package
