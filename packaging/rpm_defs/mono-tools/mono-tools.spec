
# norootforbuild

Name:           mono-tools
BuildRequires:  gconf-sharp2 gecko-sharp2 gtkhtml-sharp2 mono-devel mono-nunit monodoc-core
Version:        1.2.4
Release:        1
License:        GNU General Public License (GPL)
BuildArch:    noarch
URL:            http://go-mono.org/
Source0:        %{name}-%{version}.tar.bz2
Summary:        Collection of Tools and Utilities for Mono
Group:          Development/Tools/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%if 0%{?suse_version}
BuildRequires:	update-desktop-files

%if %suse_version <= 1000
# Doesn't work on 9.3 and 10.0...
%define suse_update_desktop_file true
%endif

%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

# Not sure of the equivalent for fedora...
%define suse_update_desktop_file true
%endif


%description
Mono Tools is a collection of development and testing programs and
utilities for use with Mono.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Duncan Mak <duncan@ximian.com>
    Joshua Tauberer <tauberer@for.net>
    Lee Malabone
    Philip Van Hoof
    Johannes Roith <johannes@jroith.de>
    Alp Toker <alp@atoker.com>
    Piers Haken
    John Luke <jluke@cfl.rr.com>
    Ben Maurer
    Duncan Mak <duncan@ximian.com>


%files
%defattr(-, root, root)
%_bindir/*
%_prefix/lib/monodoc
%_prefix/share/applications/monodoc.desktop
%_prefix/share/pixmaps/monodoc.png
%_prefix/lib/mono/1.0
%_prefix/lib/mono/2.0
%{_datadir}/locale/*/*/*
%_prefix/lib/create-native-map
%_prefix/share/create-native-map
%_prefix/share/pkgconfig/create-native-map.pc
%_mandir/man1/create-native-map*

%_prefix/share/applications/ilcontrast.desktop
%_prefix/lib/ilcontrast
%_prefix/share/pixmaps/ilcontrast.png

%prep
%setup  -q -n %{name}-%{version}

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
%suse_update_desktop_file -N "Mono Documentation" -G "Documentation Library" -C "Learn about using Mono" monodoc Development Documentation
%suse_update_desktop_file -N "Mono IL Contrast" -G "Development Tools" -C "Contrast Assemblies" ilcontrast Development Documentation
# Move create-native-map stuff out of lib into share
mkdir $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/create-native-map/MapAttribute.cs $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/pkgconfig $RPM_BUILD_ROOT/%_prefix/share

%clean
rm -Rf "$RPM_BUILD_ROOT"

%post
monodoc --make-index

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
