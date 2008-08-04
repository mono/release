Name:           webkit-sharp
Url:            http://www.go-mono.org/
BuildRequires:  gtk-sharp2 gtk-sharp2-gapi libwebkit-1_0-1-devel mono-devel monodoc-core
Requires:       libwebkit-1_0-1 => 1.0.r31376 gtk-sharp2
License:        LGPL v2.0 only; LGPL v2.0 or later
Group:          Development/Libraries/Other
Summary:        WebKit bindings for Mono
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Version:        0.2
Release:        3
BuildArch:      noarch
Source:         webkit-sharp-%{version}.tar.bz2

%description
WebKit is a web content engine, derived from KHTML and KJS from KDE, and used
primarily in Apple's Safari browser. It is made to be embedded in other
applications, such as mail readers, or web browsers.

This package provides Mono bindings for WebKit libraries.

%prep
%setup -q -n webkit-sharp-%{version} -q

%build
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README
%{_prefix}/lib/mono/gac/webkit-sharp
%{_prefix}/lib/mono/webkit-sharp
%{_prefix}/lib/monodoc/sources/webkit-sharp-docs*
%{_prefix}/lib/pkgconfig/webkit-sharp-1.0.pc

%changelog
* Mon May 12 2008 ecanuto@novell.com
- Initial package

