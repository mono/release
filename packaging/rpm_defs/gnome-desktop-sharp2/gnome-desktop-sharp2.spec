
# norootforbuild

Name:           gnome-desktop-sharp2
Version:	2.20.1
%define _name gnome-desktop-sharp
%ifarch ppc64
BuildRequires:  mono-biarchcompat
%endif
URL:            http://gtk-sharp.sf.net
License:        GNU General Public License (GPL), GNU Library General Public License v. 2.0 and 2.1 (LGPL)
Group:          System/GUI/GNOME
Release:        1
Summary:        Mono bindings for libgnome-desktop
Source:         %{_name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:	gnome-sharp2 gtk-sharp2-gapi

#####  suse  ####
%if 0%{?suse_version}

BuildRequires: librsvg-devel libwnck-devel nautilus-cd-burner-devel gtksourceview-devel mono-devel vte-devel monodoc-core update-desktop-files gtkhtml2-devel

%endif
#################

####  fedora  ####
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

# All fedora distros (5 and 6) have the same names, requirements
BuildRequires: librsvg2-devel libwnck-devel nautilus-cd-burner-devel mono-devel vte-devel gtkhtml3-devel gtksourceview-devel monodoc-core

%endif
#################

%description
This package contains Mono bindings for libgnome-desktop.

%package -n gtksourceview2-sharp
Summary:        Mono bindings for gtksourceview2
Group:          System/GUI/GNOME

%description -n gtksourceview2-sharp
This package contains Mono bindings for libgtksourceview-2.0.

%package -n rsvg2-sharp
Summary:        Mono bindings for rsvg
Group:          System/GUI/GNOME

%description -n rsvg2-sharp
This package contains Mono bindings for librsvg.

%package -n gtkhtml314-sharp
Summary:        Mono bindings for gtkhtml
Group:          System/GUI/GNOME

%description -n gtkhtml314-sharp
This package contains Mono bindings for gtkhtml.

%package -n wnck-sharp
Summary:        Mono bindings for wnck
Group:          System/GUI/GNOME

%description -n wnck-sharp
This package contains Mono bindings wnck.


%package -n vte016-sharp
Group:          System/GUI/GNOME
Summary:        Mono bindings for vte

%description -n vte016-sharp
This package contains Mono bindings for vte.

%package -n nautilusburn-sharp
Summary:        Mono bindings for nautilusburn
Group:          System/GUI/GNOME

%description -n nautilusburn-sharp
This package contains Mono bindings for libnautilus-burn.


%debug_package
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
%makeinstall
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_prefix}/lib/mono/gnomedesktop-sharp-2.20
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

%files -n nautilusburn-sharp
%defattr(-,root,root)
%{_libdir}/pkgconfig/nautilusburn-sharp.pc
%{_prefix}/lib/mono/gac/*nautilusburn-sharp
%{_prefix}/lib/mono/nautilusburn-sharp-2.20
%dir %{_prefix}/share/nautilusburn-sharp
%{_prefix}/share/nautilusburn-sharp/2.20

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

%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
