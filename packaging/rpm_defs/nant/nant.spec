
# norootforbuild

Name:           nant
# We have to append a .0 to make sure the rpm upgrade versioning works.
#  nant's progression: 0.85-rc4, 0.85
#  working rpm upgrade path requires: 0.85-rc4, 0.85.0
Version:        0.85.0
Release:        26
License:        GNU General Public License (GPL), GNU Library General Public License v. 2.0 and 2.1 (LGPL)
BuildArch:      noarch
URL:            http://nant.sourceforge.net
Source0:        %{name}-0.85-src.tar.gz
Patch0:         nant-remove_pkgconfig_garbage.patch
Patch1:         nant-remove_overridden_obsolete.patch
Summary:        Ant for .NET
Group:          Development/Tools/Building
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# Only needed when building from prefer rpms (normally mono-devel depends on glib2-devel)
BuildRequires:  glib2-devel

BuildRequires:  mono-data mono-devel pkgconfig

####  suse  ####
%if 0%{?suse_version}

%define old_suse_buildrequires mono-winforms mono-web

%if %suse_version == 1000
BuildRequires:  %{old_suse_buildrequires}
%endif

%if %sles_version == 9
BuildRequires:  %{old_suse_buildrequires}
%define env_options export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
%endif
%endif

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif


%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.



Authors:
--------
    Gerry Shaw


%files
%defattr(-, root, root)
%{_prefix}/bin/nant
%{_prefix}/lib/NAnt
# What else to do about these?
%{_prefix}/lib/mono/gac/NDoc.Core
%{_prefix}/lib/mono/gac/NDoc.Documenter.Msdn
%{_prefix}/lib/mono/gac/NDoc.ExtendedUI
%{_prefix}/lib/mono/gac/nunit.core
%{_prefix}/lib/mono/gac/nunit.framework
%{_prefix}/lib/mono/gac/nunit.util
%prep
%setup  -q -n %{name}-0.85
%patch0
%patch1

%build
%{?env_options}
make

%install
%{?env_options}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}
cd ${RPM_BUILD_ROOT}
# .NET libs
rm -Rf .%{_prefix}/share/NAnt/bin/lib/net
# Put mono libs in the gac
find .%{_prefix}/share/NAnt/bin/lib/mono -name "*\.dll" -exec gacutil -root ${RPM_BUILD_ROOT}%{_prefix}/lib -i {} \;
# These are in the gac now, remove them
rm -Rf .%{_prefix}/share/NAnt/bin/lib/mono
# Rearrange things according to app guidelines
mkdir -p .%{_prefix}/lib
mv .%{_prefix}/share/NAnt/bin .%{_prefix}/lib/NAnt
mv .%{_prefix}/lib/NAnt/lib/*.dll .%{_prefix}/lib/NAnt
rmdir .%{_prefix}/lib/NAnt/lib
# Cleanup cruft
rm -Rf .%{_prefix}/share

# Fix script (doesn't properly support prefix)
cat <<EOF > .%{_prefix}/bin/nant
#!/bin/sh
exec %{_prefix}/bin/mono %{_prefix}/lib/NAnt/NAnt.exe "\$@"
EOF
chmod 755 .%{_prefix}/bin/nant

%clean
rm -rf "$RPM_BUILD_ROOT"

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
