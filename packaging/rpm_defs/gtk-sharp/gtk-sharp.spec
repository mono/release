
# norootforbuild

Name:           gtk-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
URL:            http://gtk-sharp.sf.net
License:        LGPL
Group:          System/GUI/GNOME
Autoreqprov:    on
Requires:       gnome-filesystem
Version:        1.0.10
Release:        38
Summary:        Mono bindings for gtk+
Source:         %{name}-%{version}.tar.bz2
Patch2:		gtk-sharp-find_gtkhtml_ver.patch
Patch3:         gtk-sharp-makefile.patch
Patch4:		gtk-sharp-vte_config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define package_gtkhtml 1

#####  suse  ####
%if 0%{?suse_version}

# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml2
%define new_suse_buildrequires librsvg-devel mono-devel vte vte-devel
%define old_suse_buildrequires librsvg-devel mono-devel vte vte-devel pkgconfig pango-devel gtk2-devel libxml2-devel libart_lgpl-devel libgnomecanvas-devel libgnomeui libgnomeui-devel  libglade2-devel libxslt-devel libgsf-devel libgnomeprint-devel libgnomeprintui-devel popt-devel esound-devel freetype2-devel libbonoboui libgnome gnome-vfs2 libgnomeprint libgnomeprintui

%if %suse_version >= 1020
BuildRequires: %{new_suse_buildrequires} gtkhtml2-devel
%endif

# Wow, gtkhtml2-devel wasn't shipped in sles10, but it's in sled10... what to do?  Just build on 10.1, and that's it?
#  10.1's support will run out before sle10... at that point, drop 10.1, and package sled10 and sles10 separately
%if %sles_version == 10
%define package_gtkhtml 0
BuildRequires: %{new_suse_buildrequires}
%endif

%if %suse_version == 1010
BuildRequires: %{new_suse_buildrequires} gtkhtml2-devel
%endif

%if %suse_version == 1000
BuildRequires: %{new_suse_buildrequires} gtkhtml2-devel
%endif

%if %sles_version == 9
# gtkhtml2 wasn't shipped with sles9...
%define package_gtkhtml 0
BuildRequires: %{old_suse_buildrequires}

# set PKG_CONFIG_PATH for sles9
%define env_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig

%endif
%endif
#################

####  fedora  ####
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

# All fedora distros (5 and 6) have the same names, requirements
BuildRequires: librsvg2-devel mono-devel vte-devel libgnomeprintui22-devel gtkhtml3-devel
# Not needed with rpm .config dep search
#%define gtkhtml_requires gtkhtml3

%endif
#################



%description
This package contains Mono bindings for gtk+, gdk, atk, and pango.



%package gapi
Group:          System/GUI/GNOME
Summary:        C Source Parser and C Generator
Requires:       perl-XML-LibXML-Common perl-XML-LibXML perl-XML-SAX

%description gapi
The gtk-sharp-gapi package includes the parser and code generator used
by the GTK if you want to bind GObject-based libraries, or need to
compile a project that uses it to bind such a library.


%debug_package
%prep
%setup -q
%patch2
%patch3
%patch4

%build
%{?env_options}
autoreconf -fi
%configure
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT GACUTIL_FLAGS="/package gtk-sharp /gacdir /usr/lib /root ${RPM_BUILD_ROOT}/usr/lib"
rm $RPM_BUILD_ROOT/%_libdir/*.*a

# mv .exe files out of /usr/bin, and update shell wrappers to reflect the change
mkdir $RPM_BUILD_ROOT/usr/lib/gtk-sharp
mv $RPM_BUILD_ROOT/usr/bin/*.exe $RPM_BUILD_ROOT/usr/lib/gtk-sharp

sed -i "s/\/usr\/bin\/gapi-fixup/\/usr\/lib\/gtk-sharp\/gapi-fixup/g" $RPM_BUILD_ROOT/usr/bin/gapi-fixup
sed -i "s/\/usr\/bin\/gapi_codegen/\/usr\/lib\/gtk-sharp\/gapi_codegen/g" $RPM_BUILD_ROOT/usr/bin/gapi-codegen

sed -i "s/\/usr\/bin\/gconfsharp-schemagen/\/usr\/lib\/gtk-sharp\/gconfsharp-schemagen/g" $RPM_BUILD_ROOT/usr/bin/gconfsharp-schemagen

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/atk-sharp
%{_prefix}/lib/mono/gtk-sharp/atk-sharp.dll
%{_prefix}/lib/mono/gac/gdk-sharp
%{_prefix}/lib/mono/gtk-sharp/gdk-sharp.dll
%{_prefix}/lib/mono/gac/gtk-sharp
%{_prefix}/lib/mono/gtk-sharp/gtk-sharp.dll
%{_prefix}/lib/mono/gac/pango-sharp
%{_prefix}/lib/mono/gtk-sharp/pango-sharp.dll
%{_libdir}/libgdksharpglue.so
%{_libdir}/libgtksharpglue.so
%{_libdir}/libpangosharpglue.so
%{_libdir}/pkgconfig/gtk-sharp.pc

%files gapi
%defattr(-, root, root)
%_prefix/bin/gapi*
%_libdir/pkgconfig/gapi.pc
%_prefix/share/gapi
%_prefix/lib/gtk-sharp/gapi*.exe
%package -n gnome-sharp
Summary:        Mono bindings for Gnome
Group:          System/GUI/GNOME

%description -n gnome-sharp
This package contains Mono bindings for gnome.




%files -n gnome-sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/gnome-sharp
%{_prefix}/lib/mono/gtk-sharp/gnome-sharp.dll
%{_libdir}/libgnomesharpglue.so
%{_libdir}/pkgconfig/gnome-sharp.pc
%package -n rsvg-sharp
Summary:        Mono bindings for various rsvg
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       librsvg

%description -n rsvg-sharp
This package contains Mono bindings for rsvg.




%files -n rsvg-sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/rsvg-sharp
%{_prefix}/lib/mono/gtk-sharp/rsvg-sharp.dll
%{_libdir}/pkgconfig/rsvg-sharp.pc


###############
# gtkhtml2-devel isn't always available
%if %{package_gtkhtml}

%package -n gtkhtml-sharp
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       %gtkhtml_requires

%description -n gtkhtml-sharp
This package contains Mono bindings for gtkhtml.


%files -n gtkhtml-sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/gtkhtml-sharp
%{_prefix}/lib/mono/gtk-sharp/gtkhtml-sharp.dll
%{_libdir}/pkgconfig/gtkhtml-sharp.pc

%endif
###############

%package -n art-sharp
Summary:        Mono bindings for libart
Group:          System/GUI/GNOME
# Not needed with rpm .config dep search
#Requires:       libart_lgpl

%description -n art-sharp
This package contains Mono bindings for libart




%files -n art-sharp
%defattr(-,root,root)
%{_prefix}/lib/mono/gac/art-sharp
%{_prefix}/lib/mono/gtk-sharp/art-sharp.dll
%{_libdir}/pkgconfig/art-sharp.pc
%package -n glib-sharp
Summary:        Mono bindings for glib
Group:          System/GUI/GNOME

%description -n glib-sharp
This package contains Mono bindings for glib.




%files -n glib-sharp
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/glib-sharp
%{_prefix}/lib/mono/gtk-sharp/glib-sharp.dll
%{_libdir}/libglibsharpglue.so
# Maybe a future version will have this
#%{_prefix}/%{_lib}/pkgconfig/glib-sharp.pc
%package -n glade-sharp
Group:          System/GUI/GNOME
Summary:        Mono bindings for glade

%description -n glade-sharp
This package contains Mono bindings for glade.




%files -n glade-sharp
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/glade-sharp
%{_prefix}/lib/mono/gtk-sharp/glade-sharp.dll
%{_libdir}/libgladesharpglue.so
%{_libdir}/pkgconfig/glade-sharp.pc
%package -n vte-sharp
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte
# TODO: Not required anymore, but the vte-sharp .config file needs updating, and needs to pick versions depending on vte version
#Requires:       vte

%description -n vte-sharp
This package contains Mono bindings for vte.




%files -n vte-sharp
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/vte-sharp
%{_prefix}/lib/mono/gtk-sharp/vte-sharp.dll
%{_libdir}/pkgconfig/vte-sharp.pc
%package -n gconf-sharp
Summary:        Mono bindings for gconf
Group:          System/GUI/GNOME

%description -n gconf-sharp
This package contains Mono bindings for gconf and gconf peditors.




%files -n gconf-sharp
%defattr(-, root, root)
%{_prefix}/bin/gconfsharp-schemagen
%{_prefix}/lib/mono/gac/gconf-sharp
%{_prefix}/lib/mono/gtk-sharp/gconf-sharp.dll
%{_prefix}/lib/mono/gac/gconf-sharp-peditors
%{_prefix}/lib/mono/gtk-sharp/gconf-sharp-peditors.dll
%{_libdir}/pkgconfig/gconf-sharp.pc
%{_prefix}/lib/gtk-sharp/gconfsharp-schemagen.exe
%package -n gtk-sharp-complete
Group:          System/GUI/GNOME
Summary:        GTK+ and GNOME bindings for Mono (virtual package)
Requires:       gconf-sharp = %version-%release
Requires:       glade-sharp = %version-%release
Requires:       glib-sharp = %version-%release
Requires:       gnome-sharp = %version-%release
Requires:       gtk-sharp = %version-%release
Requires:       gtk-sharp-gapi = %version-%release
Requires:       vte-sharp = %version-%release

%files -n gtk-sharp-complete
%defattr(-, root, root)
%dir %{_prefix}/lib/mono/gtk-sharp
%dir %{_prefix}/lib/gtk-sharp
%doc COPYING ChangeLog README

%description -n gtk-sharp-complete
This package provides a library that allows you to build fully native
graphical GNOME applications using Mono. Gtk# is a binding to GTK+, the
cross platform user interface toolkit used in GNOME. It includes
bindings for Gtk, Atk, Pango, Gdk, libgnome, libgnomeui and
libgnomecanvas. Gtk# 1.x binds GTK+ 2.2. (Virtual package which depends
on all gtk-sharp subpackages)


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
