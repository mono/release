Name:           xsp
Url:            http://go-mono.com/
License:        X11/MIT
Group:          Productivity/Networking/Web/Servers
AutoReqProv:    on
Version:        2.10
Release:        20
Summary:        Small Web Server Hosting ASP.NET
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  mono-devel mono-web mono-data-oracle mono-data-sqlite mono-nunit pkgconfig sqlite monodoc-core

%description
The XSP server is a small Web server that hosts the Mono System.Web
classes for running what is commonly known as ASP.NET.

%prep
%setup -q
#%patch0

%build
#autoreconf -f -i -Wnone
# Cannot use the configure macro because noarch-redhat-linux is not recognized by the auto tools in the tarball
./configure --prefix=%{_prefix} \
	    --libexecdir=%{_prefix}/lib \
	    --libdir=%{_prefix}/lib \
	    --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_prefix}/lib/xsp/unittests
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/lib/pkgconfig %{buildroot}%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/pkgconfig/*
%{_prefix}/lib/mono/2.0/Mono.WebServer2.dll
%{_prefix}/lib/mono/2.0/fastcgi-mono-server2.exe
%{_prefix}/lib/mono/2.0/mod-mono-server2.exe
%{_prefix}/lib/mono/2.0/xsp2.exe
%{_prefix}/lib/mono/4.0/Mono.WebServer2.dll
%{_prefix}/lib/mono/4.0/fastcgi-mono-server4.exe
%{_prefix}/lib/mono/4.0/mod-mono-server4.exe
%{_prefix}/lib/mono/4.0/xsp4.exe
%{_prefix}/lib/mono/gac/Mono.WebServer2
%{_prefix}/lib/mono/gac/fastcgi-mono-server2
%{_prefix}/lib/mono/gac/fastcgi-mono-server4
%{_prefix}/lib/mono/gac/mod-mono-server2
%{_prefix}/lib/mono/gac/mod-mono-server4
%{_prefix}/lib/mono/gac/xsp2
%{_prefix}/lib/mono/gac/xsp4
%{_prefix}/lib/monodoc/sources/Mono.WebServer.*
%{_prefix}/lib/monodoc/sources/Mono.FastCGI.*
%{_prefix}/lib/xsp
%{_prefix}/share/man/*/*
%doc NEWS README

%changelog
