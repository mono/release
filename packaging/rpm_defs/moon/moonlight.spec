%define with_mono no
%define with_ffmpeg no
# norootforbuild

Name:           libmoon
License:        GNU General Public License (GPL), X11/MIT
Group:          Development/Languages/Other
Summary:        Moonlight
URL:            http://www.mono-project.com/Moonlight
Version:        0.6
Release:        0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        moon-%{version}.tar.bz2
ExclusiveArch: %ix86 x86_64 ppc
%if %{with_mono} == yes
#BuildRequires:  mono-devel gtk-sharp2 rsvg-sharp2 monodoc-core
%endif
%if %{with_ffmpeg} == yes
#BuildRequires:  libffmpeg-devel
%endif
#BuildRequires:  gtk2-devel gcc-c++ alsa-devel
#BuildRequires:  mozilla-xulrunner181-devel mozilla-nspr-devel gtk2-devel gcc-c++ alsa-devel

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
%if %{with_mono} == yes
%{_prefix}/lib/mono/2.1/*
%{_prefix}/lib/mono/3.0/*
%{_prefix}/lib/mono/gac/Mono.Moonlight/*
%{_prefix}/lib/mono/gac/System.Windows/*
%{_prefix}/lib/mono/gac/System.Windows.Browser/*
%endif

%debug_package

%package devel
Summary:        Moonlight libmoon
Group:          Development/Languages/Other
Requires:       libmoon = %{version}
AutoReqProv:    on

%description devel
libmoon development files

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/moon.pc
%{_libdir}/libmoon.la
%{_libdir}/libmoon.so
%if %{with_mono} == yes
%{_prefix}/lib/pkgconfig/agmono.pc
%{_prefix}/lib/pkgconfig/silver.pc
%{_prefix}/lib/pkgconfig/silverdesktop.pc
%endif
%{_prefix}/include/libmoon/*.h

%package tools
Summary:        Moonlight tools
Group:          Development/Languages/Other
Requires:       libmoon = %{version}

%description tools
Moonlight library tools (mopen, xamlg, svg2xaml, xaml2html)

%files tools
%defattr(-, root, root)
%{_prefix}/bin/mopen1
%if %{with_mono} == yes
%{_prefix}/bin/mopen
%{_prefix}/bin/svg2xaml
%{_prefix}/bin/svg2xaml-gui
%{_prefix}/bin/xamlg
%{_prefix}/bin/xaml2html
%{_prefix}/lib/moon/mopen.exe
%{_prefix}/lib/moon/mopen.exe.config
%{_prefix}/lib/moon/svg2xaml-gui.exe
%{_prefix}/lib/moon/svg2xaml.exe
%{_prefix}/lib/moon/xamlg.exe
%{_prefix}/lib/moon/xaml2html.exe
%{_mandir}/man1/mopen.1.gz
%{_mandir}/man1/svg2xaml.1.gz
%{_mandir}/man1/xamlg.1.gz
%endif

%if %{with_mono} == yes
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
%endif

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
%{_libdir}/moon/plugin/libmoonplugin-*bridge.la
%{_libdir}/moon/plugin/libmoonplugin-*bridge.so*
%if %{with_mono} == yes
%{_libdir}/moon/plugin/moonlight.exe
%endif
%{_libdir}/browser-plugins/libmoonloader.so

%if %{with_mono} == yes
%package examples
Summary:        Moonlight example programs
Group:          Development/Languages/Other
Requires:       libmoon = %{version}

%description examples
Example programs for Moonlight including desklets

%files examples
%defattr(-, root, root)
%{_bindir}/example-*
%{_libdir}/desklets/example-*
%endif

%prep
%setup  -q -n moon-%{version}
#%patch0 -p1

%build
%{?env_options}
%{?configure_options}
%configure --with-ffmpeg=%{with_ffmpeg} --with-mono=%{with_mono}
make

%install
%{?env_options}
make DESTDIR="$RPM_BUILD_ROOT" install
%if 0%{?suse_version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/browser-plugins
ln -s %{_libdir}/moon/plugin/libmoonloader.so $RPM_BUILD_ROOT%{_libdir}/browser-plugins/libmoonloader.so
%endif

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
