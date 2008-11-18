%define with_managed yes
%define with_ffmpeg no
%define with_cairo embedded

Name:           moonlight
License:        LGPL v2.0 only
Group:          Productivity/Multimedia/Other
Summary:        Novell Moonlight
Url:            http://go-mono.com/moonlight/
Version:        0.8.1
Release:        6
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         moon-%{version}.tar.bz2
%if %{with_managed} != no
BuildRequires:  gtk-sharp2 mono-devel monodoc-core rsvg2-sharp
%endif
%if %{with_ffmpeg} == yes
BuildRequires:  libffmpeg-devel
%endif
BuildRequires:  alsa-devel gcc-c++ gtk2-devel
%if 0%{?suse_version} >= 1100
BuildRequires:  libexpat-devel mozilla-xulrunner190-devel
%else
BuildRequires:  mozilla-xulrunner181-devel
%endif
%if 0%{?sles_version} == 10
BuildRequires:  -mozilla-xulrunner181-devel -rsvg2-sharp
BuildRequires:  gecko-sdk rsvg-sharp2
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
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%package -n libmoon0
License:        LGPL v2.0 only
Summary:        Novell Moonlight
Group:          Productivity/Multimedia/Other

%description -n libmoon0
Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%files -n libmoon0
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO NEWS
%{_libdir}/libmoon.so.*

%post -n libmoon0 -p /sbin/ldconfig

%postun -n libmoon0 -p /sbin/ldconfig

%package -n libmoon-devel
License:        LGPL v2.0 only
Summary:        Development files for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version} gtk2-devel

%description -n libmoon-devel
Development files for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%files -n libmoon-devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/moon.pc
%{_libdir}/libmoon.so
%dir %{_prefix}/include/libmoon
%{_prefix}/include/libmoon/*.h

%package -n moonlight-tools
License:        LGPL v2.0 only
Summary:        Various tools for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description -n moonlight-tools
Various tools for Novell Moonlight development.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%files -n moonlight-tools
%defattr(-, root, root)
%{_bindir}/mopen1
%if %{with_managed} == yes || %{with_managed} == desktop
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
%endif
%if %{with_managed} == yes || %{with_managed} == desktop

%package -n moonlight-sharp
License:        LGPL v2.0 only
Summary:        Mono bindings for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description -n moonlight-sharp
Mono bindings for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

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
%endif

%package -n moonlight-plugin
License:        LGPL v2.0 only
Summary:        Browser plugin for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description -n moonlight-plugin
Browser plugin for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%files -n moonlight-plugin
%defattr(-, root, root)
%dir %{_libdir}/moon
%dir %{_libdir}/moon/plugin
%{_libdir}/moon/plugin/README
%{_libdir}/moon/plugin/libmoonloader.so
%{_libdir}/moon/plugin/libmoonplugin.so
%{_libdir}/moon/plugin/libmoonplugin-*bridge.so*
%if %{with_managed} == yes || %{with_managed} == plugin
%{_libdir}/moon/plugin/moonlight.exe
%{_prefix}/lib/mono/2.1/*
%{_prefix}/lib/mono/gac/Mono.Moonlight/2.*
%{_prefix}/lib/mono/gac/System.Windows/2.*
%{_prefix}/lib/mono/gac/System.Windows.Browser/2.*
%endif
%if %{with_managed} == plugin
%dir %{_prefix}/lib/mono/gac/Mono.Moonlight
%dir %{_prefix}/lib/mono/gac/System.Windows
%dir %{_prefix}/lib/mono/gac/System.Windows.Browser
%endif
%if 0%{?suse_version}
%{_libdir}/browser-plugins/libmoonloader.so
%endif
%if %{with_managed} == yes || %{with_managed} == desktop

%package -n moonlight-examples
License:        LGPL v2.0 only
Summary:        Example applications for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description -n moonlight-examples
Example applications for Novell Moonlight (including desklets).

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>
    Miguel de Icaza <miguel@novell.com>
    Stephane Delcroix <sdelcroix@novell.com>
    Atsushi Enomoto <atsushi@ximian.com>
    Jb Evain <jbevain@novell.com>
    Larry Ewing <lewing@novell.com>
    Andreia Gaita <shana.ufie@gmail.com>
    Jackson Harper <jackson@ximian.com>
    Rodrigo Kumpera <rkumpera@novell.com>
    Rolf Bjarne Kvinge <RKvinge@novell.com>
    Sebastien Pouliot <sebastien@ximian.com>
    Dick Porter <dick@ximian.com>
    Jeffrey Stedfast <fejj@novell.com>
    Chris Toshok <toshok@ximian.com>
    Michael Dominic K. <mdk@mdk.am>

%files -n moonlight-examples
%defattr(-, root, root)
%{_bindir}/example-*
%dir %{_libdir}/desklets
%{_libdir}/desklets/example-*
%endif

%prep
%setup -q -n moon-%{version}

%build
%{?env_options}
%{?configure_options}
%configure --with-ffmpeg=%{with_ffmpeg} \
			--with-managed=%{with_managed} \
			 --with-cairo=%{with_cairo}
%{__make} %{?jobs:-j%jobs}

%install
%{?env_options}
%makeinstall
rm %{buildroot}%{_libdir}/libmoon.la
rm %{buildroot}%{_libdir}/moon/plugin/*.la
%if 0%{?suse_version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moon/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonloader.so
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
