
# norootforbuild

Name:           libmoon
License:        GNU General Public License (GPL), X11/MIT
Group:          Development/Languages/Other
Summary:        Moonlight
URL:            http://www.mono-project.com/Moonlight
Version:        0.1
Release:        0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        moon-%{version}.tar.bz2
ExclusiveArch: %ix86 x86_64
Requires:       mono-core

#### suse options ###
%if 0%{?suse_version}
%if %{suse_version} > 1020
%endif

# For SLES9
%if %sles_version == 9
%endif
%endif

# Fedora options
%if 0%{?fedora_version}
%endif

%description
Silverlight 1.1 (http://silverlight.net) is a new development technology for
the Web created by Microsoft based on the CLR that augments it with a 2D
retained graphics system and media playback engine and ships a subset of the
standard .NET libraries. Currently the Moonlight project supports both
Silverlight 1.0 (canvas + browser-based scripting) as well as 1.1 applications
(canvas + ECMA CLI powered execution engine).

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO NEWS
%{_libdir}/libmoon.so.*

%debug_package

%package devel
Summary:        Moonlight libmoon
Group:          Development/Languages/Other
Requires:       libmoon = %{version}

%description devel
libmoon development files

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/moon.pc
%{_libdir}/libmoon.la
%{_libdir}/libmoon.so

%package tools
Summary:        Moonlight tools
Group:          Development/Languages/Other
Requires:       libmoon = %{version}

%description tools
Moonlight library tools (mopen, xamlg, svg2xaml)

%files tools
%defattr(-, root, root)
%{_prefix}/bin/mopen
%{_prefix}/bin/svg2xaml
%{_prefix}/bin/svg2xaml-gui
%{_prefix}/bin/xamlg
%{_prefix}/lib/moon/mopen.exe
%{_prefix}/lib/moon/mopen.exe.config
%{_prefix}/lib/moon/svg2xaml-gui.exe
%{_prefix}/lib/moon/svg2xaml.exe
%{_prefix}/lib/moon/xamlg.exe
%{_mandir}/man1/mopen.1.gz
%{_mandir}/man1/svg2xaml.1.gz
%{_mandir}/man1/xamlg.1.gz

%package sharp
Summary:        Moonlight gtksilver
Group:          Development/Languages/Other
Requires:       libmoon = %{version}

%description sharp
gtksilver provides a gtk-sharp object that can be used to embed a moonlight surface in a desktop application

%files sharp
%defattr(-, root, root)
%{_prefix}/lib/pkgconfig/gtksilver.pc
%{_prefix}/lib/mono/gac/gtksilver/*
%{_prefix}/lib/mono/moon/gtksilver.dll
%{_prefix}/lib/monodoc/sources/gtksilver.source
%{_prefix}/lib/monodoc/sources/gtksilver.tree
%{_prefix}/lib/monodoc/sources/gtksilver.zip

%package -n moonlight-plugin
Summary:        Moonlight browser plugin
Group:          Productivity/Networking/Web/Browsers
Requires:       libmoon = %{version}

%description -n moonlight-plugin
Browser plugin for Moonlight

%files -n moonlight-plugin
%defattr(-, root, root)
%{_libdir}/moon/plugin/README
%{_libdir}/moon/plugin/libmoonloader.la
%{_libdir}/moon/plugin/libmoonloader.so
%{_libdir}/moon/plugin/libmoonplugin.la
%{_libdir}/moon/plugin/libmoonplugin.so
%{_libdir}/moon/plugin/moonlight.exe
%{_libdir}/browser-plugins/libmoonplugin.so

%prep
%setup  -q -n moon-%{version}
#%patch0

%build
%{?env_options}
%{?configure_options}
%configure
make

%install
%{?env_options}
make DESTDIR="$RPM_BUILD_ROOT" install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moon/plugin/libmoonplugin.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonplugin.so

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
#/sbin/ldconfig

%postun
#/sbin/ldconfig


%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
