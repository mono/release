
# norootforbuild

Name:           monodevelop
BuildRequires:  gconf-sharp2 gtk-sharp2-gapi gtksourceview-sharp2 intltool mono-basic mono-devel mono-nunit monodoc-core perl-XML-Parser vte-sharp2 xsp shared-mime-info mono-addins
URL:            http://www.go-mono.com/
License:        GNU General Public License (GPL)
Group:          Development/Languages/Other
Autoreqprov:    on
Version:	0.19
Release:	1
Summary:        A Full-Featured IDE for Mono and Gtk#
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:    noarch
Requires:       xsp
Requires:       mono-basic
Requires:	pkgconfig
PreReq:         shared-mime-info


%if 0%{?suse_version}
BuildRequires: desktop-file-utils update-desktop-files
%endif

# TODO: Add build requirements for xulrunner/mozilla, etc... md does some checks at build time for aspnetedit
#  (not currently enabled, but we'll need those checks when it is)


%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

# TODO: what to do here on fedora?
%define suse_update_desktop_file true

%endif


%description
MonoDevelop is intended to be a full-featured integrated development
environment (IDE) for mono and Gtk#. It was originally a port of
SharpDevelop 0.98. See http://monodevelop.com/ for more information.


%debug_package
%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%{_prefix} \
	    --enable-subversion \
	    --enable-monoextensions \
	    --enable-aspnet \
	    --disable-update-mimedb \
	    --disable-update-desktopdb
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT GACUTIL_FLAGS="/package monodevelop /root ${RPM_BUILD_ROOT}/usr/%_lib"
#
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/share/pkgconfig

%suse_update_desktop_file -N "Mono Development Environment" -G "Integrated Development Environment" -C "Develop software using Mono tools" %name "Application Development IDE"

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/applications/monodevelop.desktop
%{_prefix}/share/mime/packages/monodevelop.xml
%{_datadir}/icons/hicolor/*/apps/monodevelop.png
%{_datadir}/icons/hicolor/scalable/apps/monodevelop.svg
%{_prefix}/lib/monodevelop
%{_prefix}/share/pkgconfig/monodevelop.pc
%{_prefix}/share/pkgconfig/monodevelop-core-addins.pc
%{_mandir}/man1/mdtool.1.gz
%{_mandir}/man1/monodevelop.1.gz

%post
update-mime-database /usr/share/mime >/dev/null || :

%postun
update-mime-database /usr/share/mime >/dev/null || :

%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
