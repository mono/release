Name:           monodoc-core
License:        GPL v2 or later
Group:          Development/Tools/Other
Summary:        Monodoc--A Documentation Browser Written in C#
Url:            http://go-mono.org/
Version:        2.0
Release:        1
Source0:        monodoc-%version.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       monodoc
Obsoletes:      monodoc
BuildArch:      noarch
BuildRequires:  mono-devel unzip
#####  suse  ####
%if 0%{?suse_version}
%define old_suse_buildrequires mono-web
%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%endif
%endif
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Monodoc is a documentation browser for the Mono project. It is written
in C# using the GTK# libraries.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Duncan Mak <duncan@ximian.com>
    Joshua Tauberer <tauberer@for.net>
    Lee Malabone
    Philip Van Hoof
    Johannes Roith <johannes@jroith.de>
    Alp Toker <alp@atoker.com>
    Piers Haken
    John Luke <jluke@cfl.rr.com>
    Ben Maurer
    Duncan Mak <duncan@ximian.com>

%prep
%setup -n monodoc-%{version} -q

%build
%{?env_options}
./configure \
  --prefix=/usr \
  --libdir=%{_prefix}/lib \
  --libexecdir=%{_prefix}/lib \
  --localstatedir="%{_localstatedir}" \
  --mandir=%{_mandir} \
  --infodir=/usr/share/info \
  --sysconfdir=%{_sysconfdir}
make

%install
%{?env_options}
make DESTDIR="$RPM_BUILD_ROOT" install
install -d $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/%{_prefix}/lib/pkgconfig $RPM_BUILD_ROOT/usr/share
rm -f $RPM_BUILD_ROOT/usr/lib/monodoc/sources/gtk-sharp-docs.tree
rm -f $RPM_BUILD_ROOT/usr/lib/monodoc/sources/gtk-sharp-docs.zip

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%{_prefix}/lib/mono/gac/monodoc
%{_prefix}/lib/mono/monodoc
%{_bindir}/*
%{_prefix}/lib/monodoc
%{_prefix}/share/pkgconfig/monodoc.pc
%{_mandir}/man1/*
%{_mandir}/man5/*
# Should be in mono-tools now...?
#%{_prefix}/share/applications/monodoc.desktop
#%{_prefix}/share/pixmaps/monodoc.png
%doc AUTHORS ChangeLog NEWS README
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
