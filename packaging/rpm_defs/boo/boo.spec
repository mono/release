Name:           boo
Version:        0.9.2.3383
Release:        1
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
# gtksourceview is required so that we can put the sourceview lang definitions
# in the right location
# On older versions of suse, this was defined as /opt/gnome... make it cross distro
%define gtksourceview_prefix %(pkg-config --variable=prefix gtksourceview-1.0)
%define mime_info_prefix %(pkg-config --variable=prefix shared-mime-info)

%description
Boo is a new object-oriented statically-typed programming language for
the common language infrastructure with a Python-inspired syntax and a
special focus on language and compiler extensibility.

%package devel
License:        X11/MIT
Summary:        A CLI Scripting Language
Group:          Development/Languages/Other
Requires:       boo = %{version}

%description devel
Boo is a new object-oriented statically-typed programming language for
the common language infrastructure with a Python-inspired syntax and a
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
%{_prefix}/lib/mono/boo
%{_prefix}/lib/mono/gac/Boo.Lang*

%files devel
%defattr(-, root, root)
%{_bindir}/boo*
%{_datadir}/pkgconfig/boo*.pc
%{_prefix}/lib/boo
%{_datadir}/mime/packages/boo-mime-info.xml

%post
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi

%postun
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi

%changelog
