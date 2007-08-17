
# norootforbuild

# fedora uses a different package name
#  (Is this going to cause grief later... ?)
%if 0%{?fedora_version} || 0%{?rhel_version}
Name:		mod_mono
%else
Name:           apache2-mod_mono
Obsoletes:	mod_mono
Provides:	mod_mono
# TODO: suse needs mod_mono.conf in /etc/apache2/conf.d !!
%endif

%define modname mod_mono
%define apxs /usr/sbin/apxs2
%define apache2_sysconfdir %(%{apxs} -q SYSCONFDIR)
%define apache2_libexecdir %(%{apxs} -q LIBEXECDIR)
%define apache_mmn        %(MMN=$(%{apxs} -q LIBEXECDIR)_MMN; test -x $MMN && $MMN)

URL:            http://go-mono.com/
License:        The Apache Software License
Group:          Productivity/Networking/Web/Servers
Autoreqprov:    on
Version:        1.2.5
Release:        14
Summary:        Run ASP.NET Pages on Unix with Apache and Mono
Source:         %{modname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       mod_mono = %{version}-%{release}
Requires:       xsp


############### Suse based options
%if 0%{?suse_version}
BuildRequires:  apache2-devel mono-devel
Requires:       apache2 %{apache_mmn} 

%if %{suse_version} >= 1010
BuildRequires:  libapr-util1-devel
%endif

%if %{sles_version} == 9
BuildRequires: pkgconfig
%endif

%endif

############### redhat based options
%if 0%{?fedora_version} || 0%{?rhel_version}
BuildRequires:  httpd-devel pkgconfig
Requires:       httpd
%endif


%description
mod_mono is a module that interfaces Apache with Mono and allows
running ASP.NET pages on Unix and Unix-like systems.

To load the module into Apache, run the command "a2enmod mono" as root.



%debug_package
%prep
%setup -n %{modname}-%{version} -q

%build
%configure

make

%install
make install DESTDIR=$RPM_BUILD_ROOT APXS_SYSCONFDIR="%{apache2_sysconfdir}/conf.d"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{apache2_libexecdir}/*
%{apache2_sysconfdir}/conf.d/*
%{_mandir}/man8/mod_mono.8*

%changelog
