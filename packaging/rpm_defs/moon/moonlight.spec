
# norootforbuild

Name:           moonlight
License:        GNU General Public License (GPL), X11/MIT
Group:          Development/Languages/Other
Summary:        Moonlight
URL:            http://www.mono-project.com/Moonlight
Version:        0.1
Release:        0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        moon-%{version}.tar.bz2
Provides:       moonlight = %{version}-%{release}
ExclusiveArch: %ix86 x86_64
Requires:       mono-core


BuildRequires:  cairo-devel 

#### suse options ###
%if 0%{?suse_version}
# factory needed this... ?
#  All distro versions need it, but it was installed by default up until 10.3
%if %{suse_version} > 1020
#BuildRequires:	ncurses-devel
%endif

# For SLES9
%if %sles_version == 9
#%define configure_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
#BuildRequires: pkgconfig
%endif
%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
#%define env_options export MONO_SHARED_DIR=/tmp

# Note: this fails to build on fedora5 x86_64 because of this bug:
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=189324
%endif


%description
Moonlight :-)
Silverlight 1.1 (http://silverlight.net) is a new development technology for
the Web created by Microsoft based on the CLR that augments it with a 2D
retained graphics system and media playback engine and ships a subset of the
standard .NET libraries. Currently the Moonlight project supports both
Silverlight 1.0 (canvas + browser-based scripting) as well as 1.1 applications
(canvas + ECMA CLI powered execution engine).

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO NEWS
%{_prefix}/bin/mopen
%{_prefix}/bin/svg2xaml
%{_prefix}/bin/svg2xaml-gui
%{_prefix}/bin/xamlg
%{_prefix}/lib/pkgconfig/gtksilver.pc
%{_prefix}/lib/pkgconfig/moon.pc
%{_prefix}/lib/mono/gac/gtksilver
%{_prefix}/lib/mono/moon/gtksilver.dll
%{_prefix}/lib/monodoc/sources/gtksilver.source
%{_prefix}/lib/monodoc/sources/gtksilver.tree
%{_prefix}/lib/monodoc/sources/gtksilver.zip
%{_prefix}/lib/moon/mopen.exe
%{_prefix}/lib/moon/mopen.exe.config
%{_prefix}/lib/moon/plugin/README
%{_prefix}/lib/moon/plugin/libmoonloader.la
%{_prefix}/lib/moon/plugin/libmoonloader.so
%{_prefix}/lib/moon/plugin/libmoonplugin.la
%{_prefix}/lib/moon/plugin/libmoonplugin.so
%{_prefix}/lib/moon/plugin/moonlight.exe
%{_prefix}/lib/moon/svg2xaml-gui.exe
%{_prefix}/lib/moon/svg2xaml.exe
%{_prefix}/lib/moon/xamlg.exe
%{_libdir}/libmoon.la
%{_libdir}/libmoon.so
%{_libdir}/libmoon.so.0
%{_libdir}/libmoon.so.0.0.0
%{_mandir}/man1/mopen.1.gz
%{_mandir}/man1/svg2xaml.1.gz
%{_mandir}/man1/xamlg.1.gz

%debug_package
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

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
#/sbin/ldconfig

%postun
#/sbin/ldconfig


# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog
