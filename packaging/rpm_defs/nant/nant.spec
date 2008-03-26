
# norootforbuild

Name:           nant
# We have to append a .0 to make sure the rpm upgrade versioning works.
#  nant's progression: 0.85-rc4, 0.85
#  working rpm upgrade path requires: 0.85-rc4, 0.85.0
Version:        0.86_beta1
Release:        26
License:        GNU General Public License (GPL), GNU Library General Public License v. 2.0 and 2.1 (LGPL)
BuildArch:      noarch
URL:            http://nant.sourceforge.net
Source0:        %{name}-0.86-beta1-src.tar.gz
Patch0:		nant-useruntime_fix.patch
Summary:        Ant for .NET
Group:          Development/Tools/Building
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# Only needed when building from prefer rpms (normally mono-devel depends on glib2-devel)
BuildRequires:  glib2-devel

BuildRequires:  mono-data mono-devel pkgconfig

####  suse  ####
%if 0%{?suse_version}

%define old_suse_buildrequires mono-winforms mono-web

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
%{_bindir}/nant
%{_datadir}/NAnt
%prep
%setup  -q -n %{name}-0.86-beta1
%patch0 -p1

%build
%{?env_options}
make

%install
%{?env_options}
make install prefix=${RPM_BUILD_ROOT}%{_prefix}

# Fix script (doesn't properly support prefix)
cat <<EOF > $RPM_BUILD_ROOT%{_prefix}/bin/nant
#!/bin/sh
exec %{_prefix}/bin/mono %{_prefix}/share/NAnt/bin/NAnt.exe "\$@"
EOF
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/nant

%clean
rm -rf "$RPM_BUILD_ROOT"

%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
# ignore some bundled dlls
%define __find_provides env sh -c 'filelist=($(grep -v log4net.dll | grep -v scvs.exe | grep -v nunit | grep -v NDoc | grep -v neutral)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
