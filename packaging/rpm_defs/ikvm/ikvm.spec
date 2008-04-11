
# norootforbuild

Name:           ikvm
BuildRequires:  dos2unix mono-devel unzip
Version:        0.36.0.5
Release:        1
License:        BSD 3-Clause
BuildArch:      noarch
Url:            http://www.ikvm.net
Source0:        ikvmbin-%{version}.zip
Summary:        A JVM Based on the Mono Runtime
Group:          Development/Tools/Other
Requires:       mono-ikvm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
####  fedora  ####
%if 0%{?fedora_version} || 0%{?rhel_version}
# All fedora distros (5 and 6) have the same names, requirements
# Needed to generate wrapper
BuildRequires:  which
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%define env_options export MONO_SHARED_DIR=/tmp
%endif
#################

%description
This package provides IKVM.NET, an open source Java compatibility layer
for Mono, which includes a Virtual Machine, a bytecode compiler, and
various class libraries for Java, as well as tools for Java and Mono
interoperability.



Authors:
--------
    Jeroen Frijters <jfrijters@users.sourceforge.net>

%prep
%setup -q
# For some reason this file is outside the source dir...
cp ../LICENSE .
# fix line endings for rpmlint
dos2unix LICENSE

%build
true

%install
%{?env_options}
# Create dirs
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/ikvm
mkdir -p ${RPM_BUILD_ROOT}/usr/share/pkgconfig
#Install binaries
#  (do iname for JVM.DLL)
find bin -iname "*\.dll" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
find bin -name "*\.exe" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
# Install some in gac (By request of Jeroen)
for i in IKVM.AWT.WinForms.dll IKVM.OpenJDK.ClassLibrary.dll IKVM.Runtime.dll ; do
	gacutil -i ${RPM_BUILD_ROOT}/usr/lib/ikvm/$i -package ikvm -root ${RPM_BUILD_ROOT}/usr/lib
	rm -f ${RPM_BUILD_ROOT}/usr/lib/ikvm/$i
done
# Generate wrapper scripts
for f in `find bin . -name "*\.exe"` ; do
        script_name=${RPM_BUILD_ROOT}/usr/bin/`basename $f .exe`
        cat <<EOF > $script_name
#!/bin/sh
exec `which mono` /usr/lib/ikvm/`basename $f` "\$@"
EOF
        chmod 755 $script_name
done
# Generate .pc file
%define prot_name Name
%define prot_version Version
cat <<EOF > ${RPM_BUILD_ROOT}/usr/share/pkgconfig/ikvm.pc
prefix=/usr
exec_prefix=\${prefix}
libdir=\${prefix}/lib
%prot_name: IKVM.NET
Description: An implementation of Java for Mono and the Microsoft .NET Framework.
%prot_version: %{version}
Libs: -r:\${libdir}/ikvm/IKVM.Runtime.dll -r:\${libdir}/ikvm/IKVM.GNU.Classpath.dll
EOF

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root)
%doc LICENSE
%_bindir/*
%_prefix/lib/ikvm
%_prefix/lib/mono/ikvm
%_prefix/lib/mono/gac/IKVM*
%_prefix/share/pkgconfig/ikvm.pc
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(grep -v SharpZipLib)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
