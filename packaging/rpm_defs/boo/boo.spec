Name:           boo
Version:        0.9.3.3457
Release:        30
%define _version 2_0_9_3
%define _version_short 0.9.3
License:        X11/MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        boo-%{version}.tar.bz2
Patch1:         boo-pkgconfig_path_fix.patch
Group:          Development/Languages/Other
Summary:        A CLI Scripting Language
BuildArch:      noarch
Url:            http://boo.codehaus.org/Home
BuildRequires:  mono-devel
BuildRequires:  gtksourceview18-devel
BuildRequires:  shared-mime-info
Requires:       %{name}-%{_version} = %{version}
# gtksourceview is required so that we can put the sourceview lang definitions
# in the right location
# On older versions of suse, this was defined as /opt/gnome... make it cross distro
%define gtksourceview_prefix %(pkg-config --variable=prefix gtksourceview-1.0)
%define mime_info_prefix %(pkg-config --variable=prefix shared-mime-info)

%description
Boo is a new object oriented statically typed programming language for
the Common Language Infrastructure with a python inspired syntax and a
special focus on language and compiler extensibility.

%prep
%setup -q
%patch1

%build
%configure --libdir=%{_prefix}/lib
make

%install
make install DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib/pkgconfig %{buildroot}%{_datadir}/
# boo.lang is provided by gtksourceview
rm -rf %{buildroot}%{_datadir}/gtksourceview-1.0

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%dir %{_prefix}/lib/mono/gac/Boo.Lang*
%{_bindir}/boo*
%{_datadir}/mime/packages/boo-mime-info.xml
%{_datadir}/pkgconfig/boo*.pc
%{_prefix}/lib/boo
%{_prefix}/lib/mono/boo
%{_prefix}/lib/mono/gac/Boo.Lang*/2.%{_version_short}*

%post
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi

%postun
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi

%changelog
