Name:           gnome-desktop-sharp2
%define _name gnome-desktop-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
Url:            http://mono-project.com
License:        LGPL v2.1 only
Group:          System/GUI/GNOME
Summary:        Mono bindings for libgnome-desktop
BuildRequires:  gnome-sharp2 gtk-sharp2-gapi
%define _version 2.20.1
#####  suse  ####
%if 0%{?suse_version}
%if %{suse_version} > 1100
%define gnome_version 224
%else
%define gnome_version 220
%endif
BuildRequires:  gtkhtml2-devel gtksourceview-devel librsvg-devel libwnck-devel mono-devel monodoc-core nautilus-cd-burner-devel update-desktop-files vte-devel
%endif
#################
####  fedora  ####
%if 0%{?fedora_version}
%if %{fedora_version} >= 10
%define gnome_version 224
%else
%define gnome_version 220
%endif
%define env_options export MONO_SHARED_DIR=/tmp
# All fedora distros (5 and 6) have the same names, requirements
BuildRequires:  gtkhtml3-devel gtksourceview-devel librsvg2-devel libwnck-devel mono-devel monodoc-core nautilus-cd-burner-devel vte-devel
%endif
#################
%if %{gnome_version} >= 224
%define _version 2.24.0
BuildRequires:  gnome-panel-devel
%endif
Version:        %_version
Release:        2
Source:         %{_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Mono bindings for libgnome-desktop



Authors:
--------
    Mike Kestner <mkestner@novell.com

%package -n gtksourceview2-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for gtksourceview2
Group:          System/GUI/GNOME
Requires:       libgtksourceview2sharpglue-2.so
Provides:       libgtksourceview2sharpglue-2.so

%description -n gtksourceview2-sharp
Mono bindings for gtksourceview2



Authors:
--------
    Mike Kestner <mkestner@novell.com>

%package -n rsvg2-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for rsvg
Group:          System/GUI/GNOME

%description -n rsvg2-sharp
This package contains Mono bindings for librsvg.



%package -n gtkhtml314-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME
Requires:       libgtkhtmlsharpglue-2.so
Provides:       libgtkhtmlsharpglue-2.so

%description -n gtkhtml314-sharp
This package contains Mono bindings for gtkhtml.



%package -n wnck-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for wnck
Group:          System/GUI/GNOME
Requires:       libwncksharpglue-2.so
Provides:       libwncksharpglue-2.so

%description -n wnck-sharp
Mono bindings for wnck



Authors:
--------
    Mike Kestner <mkestner@novell.com>

%package -n vte016-sharp
License:        GPL v2 only; LGPL v2.1 only
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte
Requires:       libvtesharpglue-2.so
Provides:       libvtesharpglue-2.so

%description -n vte016-sharp
This package contains Mono bindings for vte.



%package -n nautilusburn-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for nautilusburn
Group:          System/GUI/GNOME
Requires:       libnautilusburnsharpglue-2.so
Provides:       libnautilusburnsharpglue-2.so

%description -n nautilusburn-sharp
Mono bindings for nautilusburn



Authors:
--------
    Mike Kestner <mkestner@novell.com>

%if %{gnome_version} >= 224

%package -n gnome-panel-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for gnome-panel
Group:          System/GUI/GNOME
Requires:       libgnomepanelsharpglue-2.so
Provides:       libgnomepanelsharpglue-2.so

%description -n gnome-panel-sharp
Mono bindings for gnome-panel



Authors:
--------
    Mike Kestner <mkestner@novell.com

%package -n gnome-print-sharp
License:        LGPL v2.1 only
Summary:        Mono bindings for gnome-print
Group:          System/GUI/GNOME

%description -n gnome-print-sharp
Mono bindings for gnome-print



Authors:
--------
    Mike Kestner <mkestner@novell.com

%endif

%prep
%setup -q -n %{_name}-%{version}

%build
%{?env_options}
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

%files
%defattr(-,root,root)
%{_libdir}/pkgconfig/gnome-desktop-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*gnomedesktop-sharp
%{_prefix}/lib/mono/gnomedesktop-sharp-2.20
%dir %{_prefix}/share/gnomedesktop-sharp
%{_prefix}/share/gnomedesktop-sharp/2.20

%files -n gtksourceview2-sharp
%defattr(-,root,root)
%{_libdir}/pkgconfig/gtksourceview2-sharp.pc
%{_prefix}/lib/mono/gac/*gtksourceview2-sharp
%{_prefix}/lib/mono/gtksourceview2-sharp-2.0
%dir %{_prefix}/share/gtksourceview2-sharp
%{_prefix}/share/gtksourceview2-sharp/2.0
%if %{gnome_version} >= 224
%{_libdir}/libgtksourceview2sharpglue-2.so
%endif

%files -n rsvg2-sharp
%defattr(-,root,root)
%{_libdir}/pkgconfig/rsvg2-sharp-2.0.pc
%{_prefix}/lib/mono/gac/*rsvg2-sharp
%{_prefix}/lib/mono/rsvg2-sharp-2.0
%dir %{_prefix}/share/rsvg2-sharp
%{_prefix}/share/rsvg2-sharp/2.0

%files -n gtkhtml314-sharp
%defattr(-,root,root)
%{_libdir}/pkgconfig/gtkhtml-sharp-3.14.pc
%{_prefix}/lib/mono/gac/*gtkhtml-sharp
%{_prefix}/lib/mono/gtkhtml-sharp-3.14
%dir %{_prefix}/share/gtkhtml-sharp
%{_prefix}/share/gtkhtml-sharp/3.14
%if %{gnome_version} >= 224
%{_libdir}/libgtkhtmlsharpglue-2.so
%endif

%files -n nautilusburn-sharp
%defattr(-,root,root)
%{_libdir}/pkgconfig/nautilusburn-sharp.pc
%{_prefix}/lib/mono/gac/*nautilusburn-sharp
%{_prefix}/lib/mono/nautilusburn-sharp-2.20
%dir %{_prefix}/share/nautilusburn-sharp
%{_prefix}/share/nautilusburn-sharp/2.20
%if %{gnome_version} >= 224
%{_libdir}/libnautilusburnsharpglue-2.so
%endif

%files -n vte016-sharp
%defattr(-, root, root)
%{_libdir}/libvtesharpglue-2.so
%{_libdir}/pkgconfig/vte-sharp-0.16.pc
%{_prefix}/lib/mono/gac/*vte-sharp
%{_prefix}/lib/mono/vte-sharp-0.16
%dir %{_prefix}/share/vte-sharp
%{_prefix}/share/vte-sharp/0.16

%files -n wnck-sharp
%defattr(-, root, root)
%{_libdir}/pkgconfig/wnck-sharp-1.0.pc
%{_prefix}/lib/mono/gac/*wnck-sharp
%{_prefix}/lib/mono/wnck-sharp-2.20
%dir %{_prefix}/share/wnck-sharp
%{_prefix}/share/wnck-sharp/2.20
%if %{gnome_version} >= 224
%{_libdir}/libwncksharpglue-2.so
%endif
%if %{gnome_version} >= 224

%files -n gnome-panel-sharp
%defattr(-, root, root)
%{_libdir}/pkgconfig/gnome-panel-sharp-2.24.pc
%{_prefix}/lib/mono/gac/gnome-panel-sharp
%{_prefix}/lib/mono/gnome-panel-sharp-2.24
%dir %{_prefix}/share/gnome-panel-sharp
%{_prefix}/share/gnome-panel-sharp/2.24
%{_libdir}/libgnomepanelsharpglue-2.so

%files -n gnome-print-sharp
%defattr(-, root, root)
%{_libdir}/pkgconfig/gnome-print-sharp-2.18.pc
%{_prefix}/lib/mono/gac/gnome-print-sharp
%{_prefix}/lib/mono/gnome-print-sharp-2.18
%dir %{_prefix}/share/gnome-print-sharp
%{_prefix}/share/gnome-print-sharp/2.18
%endif
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
