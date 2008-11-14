Name:           mono-tools
BuildRequires:  gconf-sharp2 mono-data-oracle mono-devel mono-jscript mono-nunit monodoc-core
Version:        2.2
Release:        6
License:        GPL v2 or later
BuildArch:      noarch
Url:            http://go-mono.org/
Source0:        %{name}-%{version}.tar.bz2
Summary:        Collection of Tools and Utilities for Mono
Group:          Development/Tools/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
%if %suse_version > 1100
BuildRequires:  webkit-sharp
%else
BuildRequires:  gecko-sharp2
%endif
%if %suse_version >= 1030
BuildRequires:  gtkhtml314-sharp
%else
BuildRequires:  gtkhtml-sharp2
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
# Not sure of the equivalent for fedora...
%define suse_update_desktop_file true
%if %fedora_version >= 8
BuildRequires:  gtkhtml314-sharp
%else
BuildRequires:  gtkhtml-sharp2
%endif
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%define suse_update_desktop_file true
BuildRequires:  gtkhtml-sharp2
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
    Sebastien Pouliot <sebastien@ximian.com>

%files -f %{name}.lang
%defattr(-, root, root)
%_bindir/*
%_datadir/applications/gendarme-wizard.desktop
%_datadir/applications/gsharp.desktop
%_datadir/applications/ilcontrast.desktop
%_datadir/applications/monodoc.desktop
%_datadir/applications/mprof-heap-viewer.desktop
%_datadir/create-native-map
%_datadir/pixmaps/gendarme.svg
%_datadir/pixmaps/ilcontrast.png
%_datadir/pixmaps/monodoc.png
%_datadir/pkgconfig/create-native-map.pc
%_datadir/pkgconfig/gendarme-framework.pc
%_mandir/man1/create-native-map*
%_mandir/man1/gendarme*
%_mandir/man1/mperfmon*
%_mandir/man1/mprof-decoder*
%_mandir/man1/mprof-heap-viewer*
%_prefix/lib/create-native-map
%_prefix/lib/gendarme
%_prefix/lib/gsharp
%_prefix/lib/gui-compare
%_prefix/lib/ilcontrast
%_prefix/lib/mono-tools
%_prefix/lib/mono/1.0
%_prefix/lib/mono/2.0
%_prefix/lib/monodoc
%_prefix/lib/mperfmon

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var --enable-monowebbrowser

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
%suse_update_desktop_file monodoc
%suse_update_desktop_file ilcontrast
%suse_update_desktop_file mprof-heap-viewer
%suse_update_desktop_file gendarme-wizard
%suse_update_desktop_file gsharp
# Move create-native-map stuff out of lib into share
mkdir $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/create-native-map/MapAttribute.cs $RPM_BUILD_ROOT/%_prefix/share/create-native-map
mv $RPM_BUILD_ROOT/%_prefix/lib/pkgconfig $RPM_BUILD_ROOT/%_prefix/share
%find_lang %{name}

%clean
rm -Rf "$RPM_BUILD_ROOT"

# Disabled because of bug in monodoc
#%post
#monodoc --make-index

%changelog
