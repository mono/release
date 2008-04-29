
# norootforbuild

Name:           mono-zeroconf
AutoReqProv:    on
License:        X11/MIT
Group:          Development/Languages/Mono
Summary:        A cross platform Zero Configuration Networking library for Mono
Url:            http://mono-project.com/Mono.Zeroconf
Version:        0.7.6
Release:        1
Source0:        %{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  mono-devel
Requires:       mono-zeroconf-provider
%define assembly_version 2.0.0.76
## --- Build Configuration --- ##
%define build_avahi 1
%define build_mdnsr 1
%define build_docs 1
# openSUSE Configuration
%if 0%{?suse_version}
%if %{suse_version} >= 1030
%define build_avahi 1
%define build_mdnsr 0
BuildRequires:  avahi-mono
%endif
%if %{suse_version} >= 1020 && %{suse_version} < 1030
%define build_avahi 1
%define build_mdnsr 1
%define override_avahi_libs 1
BuildRequires:  avahi-mono
BuildRequires:  mDNSResponder-devel
%endif
%if %{suse_version} < 1020
%define build_avahi 0
%define build_mdnsr 1
BuildRequires:  mDNSResponder-devel
%endif
%endif
# Fedora Configuration
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%define build_docs 0
%define build_mdnsr 0
%define build_avahi 1
BuildRequires:  avahi-sharp
%endif
# Mandriva Configuration
%if 0%{?mandriva_version}
%define build_docs 0
%define build_avahi 1
%define build_mdnsr 0
BuildRequires:  avahi-sharp
%endif
%if 0%{?build_docs}
BuildRequires:  monodoc-core
%endif
## --- Base Package Information --- ##

%description
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET. It provides a unified API for performing the most
common zeroconf operations on a variety of platforms and subsystems:
all the operating systems supported by Mono and both the Avahi and
Bonjour/mDNSResponder transports.



Authors:
--------
    Aaron Bockover <abockover@novell.com>

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %_prefix/lib/mono-zeroconf
%dir %_prefix/lib/mono/mono-zeroconf
%dir %_prefix/lib/mono/gac/Mono.Zeroconf
%dir %_prefix/lib/mono/gac/Mono.Zeroconf/%{assembly_version}__e60c4f4a95e1099e
%dir %_prefix/lib/mono/gac/policy.1.0.Mono.Zeroconf
%dir %_prefix/lib/mono/gac/policy.1.0.Mono.Zeroconf/0.0.0.0__e60c4f4a95e1099e
%dir %_prefix/lib/mono/gac/policy.2.0.Mono.Zeroconf
%dir %_prefix/lib/mono/gac/policy.2.0.Mono.Zeroconf/0.0.0.0__e60c4f4a95e1099e
%_bindir/mzclient
%_prefix/share/pkgconfig/mono-zeroconf.pc
%_prefix/lib/mono/gac/Mono.Zeroconf/*/*.dll*
%_prefix/lib/mono/gac/policy.1.0.Mono.Zeroconf/*/*
%_prefix/lib/mono/gac/policy.2.0.Mono.Zeroconf/*/*
%_prefix/lib/mono/mono-zeroconf/Mono.Zeroconf.dll*
%_prefix/lib/mono-zeroconf/MZClient.exe*
## --- mDNSResponder Provider --- ##
%if %{build_mdnsr} == 1

%package provider-mDNSResponder
Summary:        A cross platform Zero Configuration Networking library for Mono
Group:          Development/Languages/Mono
BuildRequires:  mDNSResponder-devel
Requires:       mDNSResponder mono-zeroconf
Provides:       mono-zeroconf-provider

%description provider-mDNSResponder
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET. It provides a unified API for performing the most
common zeroconf operations on a variety of platforms and subsystems:
all the operating systems supported by Mono and both the Avahi and
Bonjour/mDNSResponder transports.



Authors:
--------
    Aaron Bockover <abockover@novell.com>

%files provider-mDNSResponder
%defattr(-, root, root)
%dir %_prefix/lib/mono-zeroconf
%_prefix/lib/mono-zeroconf/Mono.Zeroconf.Providers.Bonjour.dll*
%endif
## --- Avahi Provider --- ##
%if %{build_avahi} == 1

%package provider-avahi
Summary:        A cross platform Zero Configuration Networking library for Mono
Group:          Development/Languages/Mono
Requires:       mono-zeroconf
Provides:       mono-zeroconf-provider

%description provider-avahi
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET. It provides a unified API for performing the most
common zeroconf operations on a variety of platforms and subsystems:
all the operating systems supported by Mono and both the Avahi and
Bonjour/mDNSResponder transports.



Authors:
--------
    Aaron Bockover <abockover@novell.com>

%files provider-avahi
%defattr(-, root, root)
%dir %_prefix/lib/mono-zeroconf
%_prefix/lib/mono-zeroconf/Mono.Zeroconf.Providers.Avahi.dll*
%endif
## --- Monodoc Developer API Documentation --- ##
%if %{build_docs} == 1

%package doc
Summary:        A cross platform Zero Configuration Networking library for Mono
Group:          Development/Languages/Mono

%description doc
Mono.Zeroconf is a cross platform Zero Configuration Networking library
for Mono and .NET. It provides a unified API for performing the most
common zeroconf operations on a variety of platforms and subsystems:
all the operating systems supported by Mono and both the Avahi and
Bonjour/mDNSResponder transports.



Authors:
--------
    Aaron Bockover <abockover@novell.com>

%files doc
%defattr(-, root, root)
%dir %_prefix/lib/monodoc/sources/
%_prefix/lib/monodoc/sources/mono-zeroconf-docs*
%endif
## --- Build/Install --- #

%prep
%setup -q

%build
%{?env_options}
%if 0%{?override_avahi_libs}
export AVAHI_LIBS="-r:/usr/lib/mono/avahi-sharp/avahi-sharp.dll"
%endif
./configure --prefix=/usr \
%if %{build_docs} == 0
	--disable-docs \
%else
	--enable-docs \
%endif
%if %{build_avahi} == 0
	--disable-avahi \
%else
	--enable-avahi \
%endif
%if %{build_mdnsr} == 0
	--disable-mdnsresponder
%else
	--enable-mdnsresponder
%endif
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/share/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(grep -v SharpZipLib)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
