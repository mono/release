#
# norootforbuild
#

%define with_cairo embedded

Name:           moonlight
ExclusiveArch:  %ix86 x86_64
License:        LGPL v2.0 only
Group:          Productivity/Multimedia/Other
Summary:        Novell Moonlight
Url:            http://go-mono.com/moonlight/
Version:        1.9.6.99
Release:        1
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        moonlight-%{version}.tar.bz2
Source1:	mono-139349.tar.bz2
#Patch0:		libmoon_libdir_fix.patch
BuildRequires:  alsa-devel
BuildRequires:  bison
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  gtk-sharp2
BuildRequires:  gtk2-devel
BuildRequires:  mono-devel
BuildRequires:  monodoc-core
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


%package tools
License:        LGPL v2.0 only; X11/MIT
Summary:        Various tools for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description tools
Various tools for Novell Moonlight development.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.


Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%package sharp
License:        X11/MIT
Summary:        Mono bindings for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 == %{version}

%description sharp
Mono bindings for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.


Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>

%package plugin
License:        LGPL v2.0 only; X11/MIT
Summary:        Browser plugin for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description plugin
Browser plugin for Novell Moonlight.

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.


Authors:
--------
    Moonlight Project <moonlight-list@lists.ximian.com>


#%package examples
#License:        LGPL v2.0 only; X11/MIT
#Summary:        Example applications for Novell Moonlight
#Group:          Productivity/Multimedia/Other
#Requires:       libmoon0 = %{version}
#
#%description examples
#Example applications for Novell Moonlight (including desklets).
#
#Moonlight is an open source implementation of Microsoft Silverlight for
#Unix systems.
#
#
#Authors:
#--------
#    Moonlight Project <moonlight-list@lists.ximian.com>

%package devel
License:        LGPL v2.0 only; X11/MIT
Summary:        Example applications for Novell Moonlight
Group:          Productivity/Multimedia/Other
Requires:       libmoon0 = %{version}

%description devel
Example applications for Novell Moonlight (including desklets).

Moonlight is an open source implementation of Microsoft Silverlight for
Unix systems.


%prep
%setup -q
%setup -b 1
#%patch0 -p 0
cd ../mono-*
%configure
make PROFILE=net_2_1_raw
cd ../moonlight*
mv ../mono-*/mcs .
rm -rf ../mono-*

%build
%{?env_options}
%{?configure_options}
autoreconf -f -i
%configure --with-cairo=%{with_cairo} \
			--with-mcspath=./mcs \
			--without-examples \
			--without-testing \
			--without-performance
%{__make} %{?jobs:-j%jobs}

%install
%{?env_options}
%makeinstall
find %{buildroot} -type f -name "*.la" -delete -print

%post -n libmoon0 -p /sbin/ldconfig

%postun -n libmoon0 -p /sbin/ldconfig


%files tools
%defattr(-, root, root)
#%dir %{_libdir}/lib/moon
%{_bindir}/mopen
%{_bindir}/mopen1
%{_bindir}/munxap
%{_bindir}/mxap
%{_bindir}/respack
%{_bindir}/sockpol
%{_bindir}/unrespack
%{_bindir}/xaml2html
%{_bindir}/xamlg
%{_libdir}/moonlight/mopen.exe
%{_libdir}/moonlight/mopen.exe.config
%{_libdir}/moonlight/mopen.exe.mdb
%{_libdir}/moonlight/munxap.exe
%{_libdir}/moonlight/mxap.exe
%{_libdir}/moonlight/respack.exe
%{_libdir}/moonlight/sockpol.exe
%{_libdir}/moonlight/xaml2html.exe
%{_libdir}/moonlight/xamlg.exe
%{_mandir}/man1/mopen.1.gz
%{_mandir}/man1/mxap.1.gz
%{_mandir}/man1/respack.1.gz
%{_mandir}/man1/sockpol.1.gz
%{_mandir}/man1/svg2xaml.1.gz
%{_mandir}/man1/xamlg.1.gz

%files sharp
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO NEWS
%dir %{_prefix}/lib/mono/2.1
%{_prefix}/lib/mono/gac/Moonlight.Gtk
%{_prefix}/lib/mono/gac/System.Windows
%{_prefix}/lib/mono/gac/System.Windows.Browser
%{_prefix}/lib/mono/gac/System.Windows.Controls
%{_prefix}/lib/mono/gac/System.Windows.Controls.Data
%{_prefix}/lib/mono/moonlight
%{_bindir}/smcs
%{_prefix}/lib/mono/2.1/smcs.exe*
%{_prefix}/lib/mono/gac/Moonlight.Gtk/0.0.0.0__976ad8f3443f9a4d/Moonlight.Gtk.dll*
%{_prefix}/lib/mono/gac/System.Windows.Browser/3.0.0.0__0738eb9f132ed756/System.Windows.Browser.dll*
%{_prefix}/lib/mono/gac/System.Windows.Controls.Data/2.0.5.0__0738eb9f132ed756/System.Windows.Controls.Data.dll*
%{_prefix}/lib/mono/gac/System.Windows.Controls/2.0.5.0__0738eb9f132ed756/System.Windows.Controls.dll*
%{_prefix}/lib/mono/gac/System.Windows/3.0.0.0__0738eb9f132ed756/System.Windows.dll*
%{_prefix}/lib/mono/moonlight/Moonlight.Gtk.dll
%{_prefix}/lib/mono/moonlight/System.Windows.Browser.dll
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.Data.dll
%{_prefix}/lib/mono/moonlight/System.Windows.Controls.dll
%{_prefix}/lib/mono/moonlight/System.Windows.dll
%{_prefix}/lib/monodoc/sources/moonlight-gtk.source
%{_prefix}/lib/monodoc/sources/moonlight-gtk.tree
%{_prefix}/lib/monodoc/sources/moonlight-gtk.zip

%files plugin
%defattr(-, root, root)
%dir %{_libdir}/moonlight
%dir %{_libdir}/moonlight/plugin
#%{_libdir}/moonlight/plugin/libmoonloader.so.*
#%{_libdir}/moonlight/plugin/libmoonplugin.so
#%{_libdir}/moonlight/plugin/libmoonplugin-*bridge.so.*
%{_libdir}/moonlight/plugin/Mono.CompilerServices.SymbolWriter.dll*
%{_libdir}/moonlight/plugin/System.Core.dll*
%{_libdir}/moonlight/plugin/System.Net.dll*
%{_libdir}/moonlight/plugin/System.Runtime.Serialization.dll*
%{_libdir}/moonlight/plugin/System.ServiceModel.Web.dll*
%{_libdir}/moonlight/plugin/System.ServiceModel.dll*
%{_libdir}/moonlight/plugin/System.Windows.Browser.dll*
%{_libdir}/moonlight/plugin/System.Windows.dll*
%{_libdir}/moonlight/plugin/System.Xml.Linq.dll*
%{_libdir}/moonlight/plugin/System.Xml.dll*
%{_libdir}/moonlight/plugin/System.dll*
%{_libdir}/moonlight/plugin/mscorlib.dll*


#%if 0%{?suse_version}
#%{_libdir}/browser-plugins/libmoonloader.so
#%endif

%files -n libmoon0
%defattr(-, root, root)
%{_libdir}/libmoon.so.*

#%files examples
#%defattr(-, root, root)
#%{_bindir}/example-*
#%dir %{_libdir}/desklets
#%{_libdir}/desklets/example-*

%files devel
%defattr(-, root, root)
%{_libdir}/libmoon.so
%{_libdir}/moonlight/plugin/libmoonloader.so
%{_libdir}/moonlight/plugin/libmoonplugin.so
%{_libdir}/moonlight/plugin/libmoonplugin-ff3bridge.so
%{_prefix}/lib/pkgconfig/moonlight-gtk.pc
%{_libdir}/pkgconfig/moon.pc
%{_prefix}/lib/pkgconfig/moon-browser-redist-assemblies.pc
%{_prefix}/lib/pkgconfig/silver.pc
%{_prefix}/lib/pkgconfig/silverdesktop.pc



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
