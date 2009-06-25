# rootforbuild


%define with_cairo embedded
%define mono_version 2.5
%define gtk_version 2.13.90

Name:           moonlight
ExclusiveArch:  %ix86 x86_64
License:        LGPL v2.0 only
Group:          Productivity/Multimedia/Other
Summary:        Novell Moonlight
Url:            http://go-mono.com/moonlight/
Version:        1.9.3.99
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        moonlight-%{version}.tar.bz2
BuildRequires:  alsa-devel
BuildRequires:  bison
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  gtk-sharp2
BuildRequires:  gtk2-devel
BuildRequires:  mono-devel
BuildRequires:  monodoc-core
BuildRequires:  mono-core-moon
BuildRequires:  rsvg2-sharp
BuildRequires:  zip
BuildRequires:  zlib-devel
%if 0%{?suse_version} >= 1100
BuildRequires:  libpulse-devel
BuildRequires:  libexpat-devel
BuildRequires:  mozilla-xulrunner190-devel
%else
BuildRequires:  mozilla-xulrunner181-devel
%endif
%if 0%{?sles_version} == 10
BuildRequires:  -mozilla-xulrunner181-devel
BuildRequires:  -rsvg2-sharp
BuildRequires:  gecko-sdk
BuildRequires:  rsvg-sharp2
%endif
%define debug_package_requires libmoon0 = %{version}-%{release}
#### suse options ###
%if 0%{?suse_version}
%if %{suse_version} > 1100
%define with_cairo system
%endif
# For SLES9
%if %sles_version == 9
%endif
%endif
# Fedora options
%if 0%{?fedora_version}
%endif

%description
Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

#%package -n mono-core
#License:        LGPL v2.1 only
#Summary:        A .NET Runtime Environment
#Group:          Development/Languages/Mono
#Version:        2.5

#Source:         mono-%{version}.tar.bz2


%package -n libmoon0
License:        LGPL v2.0 only; X11/MIT
Summary:        Novell Moonlight
Group:          Productivity/Multimedia/Other

%description -n libmoon0
Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%files -n libmoon0
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO NEWS
%{_libdir}/libmoon.so.*

%post -n libmoon0 -p /sbin/ldconfig

%postun -n libmoon0 -p /sbin/ldconfig

%package -n moonlight-tools
License:        LGPL v2.0 only; X11/MIT
Summary:        Various tools for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description -n moonlight-tools
Various tools for Novell Moonlight development.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%files -n moonlight-tools
%defattr(-, root, root)
%{_bindir}/mopen1
%dir %{_prefix}/lib/moon
%{_bindir}/mopen
%{_prefix}/lib/moon/mopen.exe*
%{_mandir}/man1/mopen.1.gz
%{_bindir}/xamlg
%{_prefix}/lib/moon/xamlg.exe
%{_mandir}/man1/xamlg.1.gz
%{_bindir}/xaml2html
%{_prefix}/lib/moon/xaml2html.exe
%{_bindir}/mxap
%{_prefix}/lib/moon/mxap.exe
%{_mandir}/man1/mxap.1.gz
%{_bindir}/respack
%{_prefix}/lib/moon/respack.exe
%{_mandir}/man1/respack.1.gz
#%{_bindir}/svg2xaml
#%{_prefix}/lib/moon/svg2xaml.exe
%{_mandir}/man1/svg2xaml.1.gz

%package -n moonlight-sharp
License:        X11/MIT
Summary:        Mono bindings for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description -n moonlight-sharp
Mono bindings for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%files -n moonlight-sharp
%defattr(-, root, root)
%dir %{_prefix}/lib/mono/3.0
%dir %{_prefix}/lib/mono/gac/Mono.Moonlight
%dir %{_prefix}/lib/mono/gac/System.Windows
%dir %{_prefix}/lib/mono/gac/System.Windows.Browser
%dir %{_prefix}/lib/mono/gac/gtksilver
%dir %{_prefix}/lib/mono/moon
%{_prefix}/lib/pkgconfig/gtksilver.pc
%{_prefix}/lib/mono/gac/gtksilver/*
%{_prefix}/lib/mono/moon/gtksilver.dll
%{_prefix}/lib/monodoc/sources/gtksilver.source
%{_prefix}/lib/monodoc/sources/gtksilver.tree
%{_prefix}/lib/monodoc/sources/gtksilver.zip
%{_prefix}/lib/mono/3.0/*
%{_prefix}/lib/mono/gac/Mono.Moonlight/3.*
%{_prefix}/lib/mono/gac/System.Windows/3.*
%{_prefix}/lib/mono/gac/System.Windows.Browser/3.*
%{_prefix}/lib/pkgconfig/agmono.pc
%{_prefix}/lib/pkgconfig/silver.pc
%{_prefix}/lib/pkgconfig/silverdesktop.pc

%package -n moonlight-plugin
License:        LGPL v2.0 only; X11/MIT
Summary:        Browser plugin for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description -n moonlight-plugin
Browser plugin for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%files -n moonlight-plugin
%defattr(-, root, root)
%dir %{_libdir}/moonlight
%dir %{_libdir}/moonlight/plugin
%{_libdir}/moonlight/plugin/README
%{_libdir}/moonlight/plugin/libmoonloader.so
%{_libdir}/moonlight/plugin/libmoonplugin.so
%{_libdir}/moonlight/plugin/libmoonplugin-*bridge.so*
%{_libdir}/moonlight/plugin/moonlight.exe
%{_prefix}/lib/mono/2.1/*
%{_prefix}/lib/mono/gac/Mono.Moonlight/2.*
%{_prefix}/lib/mono/gac/System.Windows/2.*
%{_prefix}/lib/mono/gac/System.Windows.Browser/2.*
%dir %{_prefix}/lib/mono/gac/Mono.Moonlight
%dir %{_prefix}/lib/mono/gac/System.Windows
%dir %{_prefix}/lib/mono/gac/System.Windows.Browser
%if 0%{?suse_version}
%{_libdir}/browser-plugins/libmoonloader.so
%endif

%package -n moonlight-examples
License:        LGPL v2.0 only; X11/MIT
Summary:        Example applications for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description -n moonlight-examples
Example applications for Novell Moonlight (including desklets).

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%files -n moonlight-examples
%defattr(-, root, root)
%{_bindir}/example-*
%dir %{_libdir}/desklets
%{_libdir}/desklets/example-*

%prep

%setup -q -n moonlight-%{version}


%build
%{?env_options}
%{?configure_options}
autoreconf -f -i
./configure --with-cairo=%{with_cairo} \
			--with-mcspath=/usr/lib/mono/lib/moonlight/mcs \
			--without-examples \
			--without-testing \
			--without-performance
%{__make} %{?jobs:-j%jobs}

%install
%{?env_options}
%makeinstall
rm -f %{buildroot}%{_libdir}/libmoon.la
rm -f %{buildroot}%{_libdir}/libmoon.so
rm -f %{buildroot}%{_libdir}/moonlight/plugin/*.la
rm -rf %{buildroot}%{_libdir}/pkgconfig

%if 0%{?suse_version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moonlight/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonloader.so

rm -rf %{buildroot}/mono

%endif

%clean
rm -rf ${RPM_BUILD_ROOT}
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
rm -rf %{buildroot}/mono

%changelog
