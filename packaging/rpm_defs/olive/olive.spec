
# norootforbuild

Name:     	olive
Version: 	81875
Release:	1.novell
Vendor:		Novell, Inc.
Distribution:	Novell Packages for SuSE Linux 10.0 / i586
License:	LGPL
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
%_prefix/bin/svcutil
%_prefix/lib/mono/3.0/svcutil.exe*
%_prefix/bin/client-proxy-gen
%_prefix/lib/mono/3.0/client-proxy-gen.exe*
%_prefix/bin/sts
%_prefix/lib/mono/3.0/sts.exe*
%_prefix/bin/xamlc
%_prefix/lib/mono/3.0/xamlc.exe*
%_prefix/lib/mono/gac/PresentationFramework
%_prefix/lib/mono/3.0/PresentationFramework.dll*
%_prefix/lib/mono/gac/WindowsBase
%_prefix/lib/mono/3.0/WindowsBase.dll*
%_prefix/lib/mono/gac/System.IdentityModel
%_prefix/lib/mono/3.0/System.IdentityModel.dll*
%_prefix/lib/mono/gac/System.IdentityModel.Selectors
%_prefix/lib/mono/3.0/System.IdentityModel.Selectors.dll*
%_prefix/lib/mono/gac/System.Workflow.Runtime
%_prefix/lib/mono/3.0/System.Workflow.Runtime.dll*
%_prefix/lib/mono/gac/System.Runtime.Serialization
%_prefix/lib/mono/3.0/System.Runtime.Serialization.dll*
%_prefix/lib/mono/gac/System.ServiceModel
%_prefix/lib/mono/3.0/System.ServiceModel.dll*
%_prefix/lib/mono/gac/System.Workflow.Activities
%_prefix/lib/mono/3.0/System.Workflow.Activities.dll*
%_prefix/lib/mono/gac/System.Workflow.ComponentModel
%_prefix/lib/mono/3.0/System.Workflow.ComponentModel.dll*
%_prefix/lib/mono/gac/System.Xml.Linq
%_prefix/lib/mono/gac/System.Data.Linq
%_prefix/lib/mono/gac/System.ServiceModel.Web
%_prefix/lib/mono/gac/PresentationCore
%_prefix/lib/mono/3.0/PresentationCore*
%_prefix/lib/mono/gac/System.SilverLight
%_prefix/lib/mono/3.0/System.SilverLight*
%_prefix/lib/mono/gac/agmono
%_prefix/lib/mono/3.0/agmono*
%_prefix/lib/mono/gac/agclr
%_prefix/lib/mono/3.0/agclr*
%_prefix/lib/pkgconfig/*.pc


%prep
%setup -q

%build
./configure --prefix=%_prefix
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}

%clean
# We need to keep the buildroot in tact so we can generate status pages
#  Or, we can pick the dlls out of the build tree instead of destdir in the step
#rm -rf "$RPM_BUILD_ROOT"

%changelog
