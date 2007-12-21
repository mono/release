
# norootforbuild

Name:           gtksourceview2-sharp
BuildRequires:  gnome-sharp2 gtk-sharp2-gapi mono-devel monodoc-core
BuildRequires:  gtksourceview-devel >= 2.0.0
Version:        0.11
Release:        1
License:        GNU General Public License (GPL)
BuildArch:      noarch
URL:            http://www.go-mono.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         %{name}-%{version}.tar.bz2
Summary:        GtkSourceView bindings for Mono
Group:          Development/Libraries/Other
AutoReqprov:  on

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
This package provides Mono bindings for GtkSourceView, a child of the
GTK+ text widget which implements syntax highlighting and other
features typical of a source editor.


Authors:
--------
    Michael Hutchinson <mhutchinson@novell.com>

%prep
%setup  -q

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/gtksourceview2-sharp.pc $RPM_BUILD_ROOT/usr/share/pkgconfig

%clean
rm -Rf ${DESTDIR}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README
%{_prefix}/lib/mono/gac/gtksourceview2-sharp
%{_prefix}/lib/mono/gtksourceview2-sharp
%{_prefix}/share/pkgconfig/gtksourceview2-sharp.pc
%{_prefix}/share/gapi-2.0/gtksourceview2-api.xml
%{_prefix}/lib/monodoc/sources/gtksourceview2-sharp-docs*

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
