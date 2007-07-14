
# norootforbuild

Name:     	olive
Version: 	81875
Release:	1.novell
Vendor:		Novell, Inc.
Distribution:	Novell Packages for SuSE Linux 10.0 / i586
Copyright:	LGPL
BuildRoot:	/var/tmp/%{name}-%{version}-root

BuildArch:      noarch
URL:		http://www.go-mono.com
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	mono-devel
Summary:	Mono Olive
Group:		Development/Tools

%description
Some Linq and other various .NET 3.0 bits.
	  

%files
%defattr(-, root, root)
%doc README
/usr/bin/svcutil
/usr/lib/mono/3.0/svcutil.exe*
/usr/bin/client-proxy-gen
/usr/lib/mono/3.0/client-proxy-gen.exe*
/usr/bin/sts
/usr/lib/mono/3.0/sts.exe*
/usr/bin/xamlc
/usr/lib/mono/3.0/xamlc.exe*
/usr/lib/mono/gac/PresentationFramework
/usr/lib/mono/3.0/PresentationFramework.dll*
/usr/lib/mono/gac/WindowsBase
/usr/lib/mono/3.0/WindowsBase.dll*
/usr/lib/mono/gac/System.IdentityModel
/usr/lib/mono/3.0/System.IdentityModel.dll*
/usr/lib/mono/gac/System.IdentityModel.Selectors
/usr/lib/mono/3.0/System.IdentityModel.Selectors.dll*
/usr/lib/mono/gac/System.Workflow.Runtime
/usr/lib/mono/3.0/System.Workflow.Runtime.dll*
/usr/lib/mono/gac/System.Runtime.Serialization
/usr/lib/mono/3.0/System.Runtime.Serialization.dll*
/usr/lib/mono/gac/System.ServiceModel
/usr/lib/mono/3.0/System.ServiceModel.dll*
/usr/lib/mono/gac/System.Workflow.Activities
/usr/lib/mono/3.0/System.Workflow.Activities.dll*
/usr/lib/mono/gac/System.Workflow.ComponentModel
/usr/lib/mono/3.0/System.Workflow.ComponentModel.dll*
/usr/lib/mono/gac/System.Xml.Linq
/usr/lib/mono/3.0/System.Xml.Linq.dll*
/usr/lib/mono/gac/System.ServiceModel.Web
/usr/lib/mono/3.0/System.ServiceModel.Web*
/usr/lib/mono/gac/PresentationCore
/usr/lib/mono/3.0/PresentationCore*
/usr/lib/mono/gac/System.SilverLight
/usr/lib/mono/3.0/System.SilverLight*
/usr/lib/mono/gac/agmono
/usr/lib/mono/3.0/agmono*
/usr/lib/mono/gac/agclr
/usr/lib/mono/3.0/agclr*
/usr/lib/pkgconfig/*.pc


%prep
%setup -q

%build
./configure --prefix=/usr
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%clean
# We need to keep the buildroot in tact so we can generate status pages
#  Or, we can pick the dlls out of the build tree instead of destdir in the step
#rm -rf "$RPM_BUILD_ROOT"

%changelog
