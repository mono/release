
# norootforbuild

Name:           gnome-sharp2
Version:	2.16.0
%define _name gnome-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
URL:            http://gtk-sharp.sf.net
License:        GNU General Public License (GPL), GNU Library General Public License v. 2.0 and 2.1 (LGPL)
Group:          System/GUI/GNOME
Release:        52
Summary:        .Net Language Bindings for Gnome
Patch0:         gnome-sharp-optflags.patch
Patch2:         gnome-sharp-find_gtkhtml_ver.patch
Source:         %{_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:	gtk-sharp2 glade-sharp2 gtk-sharp2-gapi

#####  suse  ####
%if 0%{?suse_version}

# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2

%define new_suse_buildrequires libgnomedb-devel librsvg-devel mono-devel vte-devel gnome-panel-devel  monodoc-core update-desktop-files
BuildRequires:	%{new_suse_buildrequires} gtkhtml2-devel

%endif
#################

####  fedora  ####
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

# All fedora distros (5 and 6) have the same names, requirements
BuildRequires: libgnomedb-devel librsvg2-devel mono-devel vte-devel libgnomeprintui22-devel gtkhtml3-devel gnome-panel-devel monodoc-core
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2

%endif
#################

%description
This package contains Mono bindings for Gnome.

%package -n gnome-sharp2-complete
Group:          System/GUI/GNOME
Summary:        GTK+ and GNOME bindings for Mono (virtual package)
Requires:       art-sharp2 = %{version}-%{release}
Requires:       gconf-sharp2 = %{version}-%{release}
Requires:       gnome-sharp2 = %{version}-%{release}
Requires:       gnome-vfs-sharp2 = %{version}-%{release}
Requires:       gtkhtml-sharp2 = %{version}-%{release}
Requires:       rsvg-sharp2 = %{version}-%{release}
Requires:       vte-sharp2 = %{version}-%{release}

%description -n gnome-sharp2-complete
Gtk# is a library that allows you to build fully native graphical GNOME
applications using Mono. Gtk# is a binding to GTK+, the cross platform
user interface toolkit used in GNOME. It includes bindings for Gtk,
Atk, Pango, Gdk, libgnome, libgnomeui and libgnomecanvas.  (Virtual
package which depends on all gtk-sharp2 subpackages)

%package -n rsvg-sharp2
Summary:        Mono bindings for rsvg
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       librsvg

%description -n rsvg-sharp2
This package contains Mono bindings for librsvg.

%package -n gtkhtml-sharp2
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       %gtkhtml_requires

%description -n gtkhtml-sharp2
This package contains Mono bindings for gtkhtml.


%package -n gnome-vfs-sharp2
Summary:        Mono bindings for gnomevfs
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       gnome-vfs2

%description -n gnome-vfs-sharp2
This package contains Mono bindings gnomevfs.


%package -n art-sharp2
Summary:        Mono bindings for libart
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       libart_lgpl

%description -n art-sharp2
This package contains Mono bindings for libart.

%package -n vte-sharp2
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte
# Not needed with rpm .config dep search
#Requires:       vte

%description -n vte-sharp2
This package contains Mono bindings for vte.

%package -n gconf-sharp2
Summary:        Mono bindings for gconf
Group:          System/GUI/GNOME

%description -n gconf-sharp2
This package contains Mono bindings for gconf and gconf peditors.


%debug_package
%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1
%patch2

%build
%{?env_options}
autoreconf -f -i
# FIXME: windowmanager.c:*: warning: dereferencing type-punned pointer will break strict-aliasing rules
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure\
	--libexecdir=%{_prefix}/lib\
	--enable-debug
make

%install
%{?env_options}
%makeinstall
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files -n gnome-sharp2-complete
%defattr(-, root, root)
## This is the 'base' package so we put the common dirs of all in this package
# Otherwise, this package doesn't get created!
%dir %{_prefix}/lib/mono/gtk-sharp-2.0
%dir %{_prefix}/lib/gtk-sharp-2.0

%files -n gnome-sharp2
%defattr(-,root,root)
%{_libdir}/libgnomesharpglue-2.so
%{_libdir}/pkgconfig/gnome-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gnome-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gnome-sharp.dll
%{_prefix}/share/gapi-2.0/gnome-api.xml

%files -n rsvg-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/rsvg-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*rsvg-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*rsvg-sharp.dll
%{_prefix}/share/gapi-2.0/rsvg-api.xml

%files -n gtkhtml-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/gtkhtml-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gtkhtml-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gtkhtml-sharp.dll
%{_prefix}/share/gapi-2.0/gtkhtml-api.xml

%files -n gnome-vfs-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/gnome-vfs-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gnome-vfs-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gnome-vfs-sharp.dll
%{_prefix}/share/gapi-2.0/gnome-vfs-api.xml

%files -n art-sharp2
%defattr(-,root,root)
%{_libdir}/pkgconfig/art-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*art-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*art-sharp.dll
%{_prefix}/share/gapi-2.0/art-api.xml

%files -n vte-sharp2
%defattr(-, root, root)
%{_libdir}/libvtesharpglue-2.so
%{_libdir}/pkgconfig/vte-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*vte-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*vte-sharp.dll
%{_prefix}/share/gapi-2.0/vte-api.xml

%files -n gconf-sharp2
%defattr(-, root, root)
%{_bindir}/gconfsharp2-schemagen
%{_libdir}/pkgconfig/gconf-sharp-2.0.pc
%{_prefix}/lib/gtk-sharp-2.0/gconfsharp-schemagen.exe
%{_prefix}/lib/mono/gac/*gconf-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp.dll
# Other distros place these in gnome-sharp2??
%{_prefix}/lib/mono/gac/*gconf-sharp-peditors
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp-peditors.dll

%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog
