Name:           webkit-sharp
Url:            http://www.go-mono.org/
BuildRequires:  gtk-sharp2 gtk-sharp2-gapi libwebkit-devel mono-devel monodoc-core
License:        X11/MIT
Group:          Development/Languages/Mono
Summary:        WebKit bindings for Mono
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Version:        0.2
Release:        2
BuildArch:      noarch
Source:         %{name}-%{version}.tar.bz2
Patch0:         %{name}-pkgconfigdir.patch
Requires:       libwebkit-1_0-1

%description
WebKit is a web content engine, derived from KHTML and KJS from KDE,
and used primarily in Apple's Safari browser. It is made to be embedded
in other applications, such as mail readers, or web browsers.

This package provides Mono bindings for WebKit libraries.



Authors:
--------
    Everaldo Canuto <ecanuto@novell.com>

%prep
%setup -q
%patch0

%build
autoreconf
./configure --prefix=%{_prefix} --libdir=%{_prefix}/lib
make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README
%{_prefix}/lib/mono/gac/webkit-sharp
%{_prefix}/lib/mono/webkit-sharp
%{_prefix}/lib/monodoc/sources/webkit-sharp-docs*
%{_datadir}/pkgconfig/webkit-sharp-1.0.pc

%changelog
