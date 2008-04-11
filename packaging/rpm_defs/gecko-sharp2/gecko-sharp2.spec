
# norootforbuild

Name:           gecko-sharp2
BuildRequires:  gtk-sharp2 gtk-sharp2-gapi gtk2-devel mono-devel monodoc-core
Version:        0.13
Release:        0
License:        LGPL v2.1 or later; MOZILLA PUBLIC LICENSE (MPL/NPL)
BuildArch:      noarch
URL:            http://www.monodevelop.com
Source0:        gecko-sharp-2.0-%{version}.tar.bz2
Summary:        Gecko bindings for Mono
Group:          Development/Libraries/Other
Provides:       gecko-sharp-2_0 gecko-sharp2-docs gecko-sharp-2.0
Obsoletes:      gecko-sharp-2_0 gecko-sharp2-docs gecko-sharp-2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqprov:  on

# To share the rpms in monobuild, ignore the .config from scanning
%define requires_list cat
%if 0%{?monobuild} == 01
%define requires_list grep -v gecko-sharp.dll.config
%endif

%define xulrunner_version 181

%if 0%{?suse_version}

%if %suse_version >= 1020
BuildRequires:       mozilla-xulrunner%{xulrunner_version}
# not needed with the .config scanning
#Requires:       mozilla-xulrunner%{xulrunner_version}
%endif

%if %suse_version == 1010
BuildRequires:       mozilla-xulrunner
# not needed with the .config scanning
#  Turns out it is needed, otherwise build system doesn't know whether satisfy the dep with
#  xulrunner or seamonkey.
# For monobuild, we can't depend on a package since we share rpms across distros. Disable.
#Requires:       mozilla-xulrunner
%endif

%if %suse_version <= 1000
# needed in order to resolve .config scanning
BuildRequires:       mozilla
%endif

%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
# Only needed to resolve libgtkembedmoz.so at mono-find-requires time
%if %fedora_version <= 5
BuildRequires:  mozilla
%endif

%if %fedora_version >= 6
BuildRequires:  firefox
%endif

%endif

%if 0%{?rhel_version}
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%define env_options export MONO_SHARED_DIR=/tmp
# Doesn't seem to matter...
#BuildRequires:  firefox
%endif

%description
This package provides Mono bindings for the Gecko engine, through an
easy-to-use widget that will allow you to embed a Mozilla browser
window into your Gtk# application.



Authors:
--------
    John Luke <jluke@cfl.rr.com>
    Mark Crichton <crichton@gimp.org>
    Mike Kestner <mkestner@ximian.com>
    Todd Berman <tberman@sevenl.net>
    Geoff Norton <gnorton@customerdna.com>
    Raja R Harinath <rharinath@novell.com>
    Zac Bowling <zac@zacbowling.com>
    Christian Hergert <christian.hergert@gmail.com>
    Alp Toker <alp@atoker.com>
    Ben Maurer <bmaurer@ximian.com>

%prep
%setup  -q -n gecko-sharp-2.0-%{version}

%build
%{?env_options}
./configure --prefix=/usr --libdir=/usr/lib --sysconfdir=/etc --mandir=/usr/share/man --infodir=/usr/share/info --localstatedir=/var

%install
%{?env_options}
make install DESTDIR=%{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/share/pkgconfig

%clean
rm -rf "%{buildroot}"

%files
%defattr(-, root, root)
/usr/lib/mono/gecko-sharp-2.0
/usr/lib/mono/gac/gecko-sharp
/usr/share/pkgconfig/*.pc
/usr/lib/monodoc/sources/*

%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(%requires_list)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
