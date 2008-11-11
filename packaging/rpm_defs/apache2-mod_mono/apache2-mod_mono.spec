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
