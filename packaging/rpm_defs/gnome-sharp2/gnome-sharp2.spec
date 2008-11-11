Name:           gnome-sharp2
%define _name gnome-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
Url:            http://gtk-sharp.sf.net
License:        LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        Mono bindings for Gnome
Patch2:         gnome-sharp-find_gtkhtml_ver.patch
BuildRequires:  glade-sharp2 gtk-sharp2 gtk-sharp2-gapi
%define minimum_glib_sharp_version 2.10.3
%define two_sixteen_version 2.16.1
%define two_twenty_version 2.20.1
%define two_twentyfour_version 2.24.0
#####  suse  ####
%if 0%{?suse_version}
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2
# Only builds on 10.2 and 10.3
%if %suse_version <= 1020
%define _version %two_sixteen_version
%endif
%if %suse_version >= 1030
%define _version %two_twenty_version
%endif
%if %suse_version >= 1110
%define _version %two_twentyfour_version
%endif
%define new_suse_buildrequires libgnomedb-devel librsvg-devel mono-devel vte-devel gnome-panel-devel  monodoc-core update-desktop-files
BuildRequires:  %{new_suse_buildrequires} gtkhtml2-devel
%endif
#################
####  fedora  ####
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%if %fedora_version <= 7
%define _version %two_sixteen_version
%endif
%if %fedora_version >= 8
%define _version %two_twenty_version
%endif
%if %fedora_version >= 10
%define _version %two_twentyfour_version
%endif
# All fedora distros (5 and 6) have the same names, requirements
BuildRequires:  gnome-panel-devel gtkhtml3-devel libgnomedb-devel libgnomeprintui22-devel librsvg2-devel mono-devel monodoc-core vte-devel
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2
%endif
# RHEL
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gnome-panel-devel gtkhtml3-devel libgnomeprintui22-devel librsvg2-devel mono-devel monodoc-core vte-devel
%if %rhel_version >= 500
%define _version %two_sixteen_version
%endif
%endif
#################
##############
### Options that relate to a version of gnome#, not necessarily a distro
# Define true for 2.20
#  (Must do this inside of shell... rpm can't handle this expression)
%define two_twenty_split %(if test x%_version = x%two_twenty_version || test x%_version = x%two_twentyfour_version; then  echo "1" ; else echo "0" ; fi)
###
##############
# Need to put this stuff down here after Version: gets defined
Version:        %_version
Release:        14
Source:         %{_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package contains Mono bindings for Gnome.



%package -n gnome-sharp2-complete
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        GTK+ and GNOME bindings for Mono (virtual package)
Requires:       art-sharp2 = %{version}-%{release}
Requires:       gconf-sharp2 = %{version}-%{release}
Requires:       gnome-sharp2 = %{version}-%{release}
Requires:       gnome-vfs-sharp2 = %{version}-%{release}
Requires:       glib-sharp2 >= %minimum_glib_sharp_version
%if %two_twenty_split == 0
Requires:       gtkhtml-sharp2 = %{version}-%{release}
Requires:       rsvg-sharp2 = %{version}-%{release}
Requires:       vte-sharp2 = %{version}-%{release}
%endif

%description -n gnome-sharp2-complete
Gtk# is a library that allows you to build fully native graphical GNOME
applications using Mono. Gtk# is a binding to GTK+, the cross platform
user interface toolkit used in GNOME. It includes bindings for Gtk,
Atk, Pango, Gdk, libgnome, libgnomeui and libgnomecanvas.  (Virtual
package which depends on all gtk-sharp2 subpackages)



%package -n gnome-vfs-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gnomevfs
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       gnome-vfs2
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n gnome-vfs-sharp2
This package contains Mono bindings gnomevfs.



%package -n art-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for libart
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       libart_lgpl
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n art-sharp2
This package contains Mono bindings for libart.



%package -n gconf-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gconf
Group:          System/GUI/GNOME
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n gconf-sharp2
This package contains Mono bindings for gconf and gconf peditors.



%prep
%setup -q -n %{_name}-%{version}
if [ %version = %two_sixteen_version ] ; then
%patch2 -p1
fi

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
make install DESTDIR=%buildroot
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

%files -n gconf-sharp2
%defattr(-, root, root)
%{_bindir}/gconfsharp2-schemagen
%{_libdir}/pkgconfig/gconf-sharp-2.0.pc
%{_prefix}/lib/gtk-sharp-2.0/gconfsharp-schemagen.exe
%{_prefix}/lib/mono/gac/*gconf-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp.dll
# Other distros place these in gnome-sharp2??
%{_libdir}/pkgconfig/gconf-sharp-peditors-2.0.pc
%{_prefix}/lib/mono/gac/*gconf-sharp-peditors
%{_prefix}/lib/mono/gtk-sharp-2.0/*gconf-sharp-peditors.dll
##########################################################
# packages that don't exist in 2.20
%if %two_twenty_split == 0

%package -n rsvg-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for rsvg
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       librsvg
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n rsvg-sharp2
This package contains Mono bindings for librsvg.



%package -n gtkhtml-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       %gtkhtml_requires
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n gtkhtml-sharp2
This package contains Mono bindings for gtkhtml.



%package -n vte-sharp2
License:        GPL v2 or later; LGPL v2.1 or later
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte
# Not needed with rpm .config dep search
#Requires:       vte
Requires:       glib-sharp2 >= %minimum_glib_sharp_version

%description -n vte-sharp2
This package contains Mono bindings for vte.



%files -n vte-sharp2
%defattr(-, root, root)
%{_libdir}/libvtesharpglue-2.so
%{_libdir}/pkgconfig/vte-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*vte-sharp
%{_prefix}/lib/mono/gtk-sharp-2.0/*vte-sharp.dll
%{_prefix}/share/gapi-2.0/vte-api.xml

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
%endif
#
##########################################################
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
