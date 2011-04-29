Name:           ikvm
BuildRequires:  dos2unix mono-devel unzip
Version:        0.42.0.6
Release:        3
License:        BSD 3-clause (or similar)
BuildArch:      noarch
Url:            http://www.ikvm.net
Source0:        ikvmbin-%{version}.zip
Summary:        A JVM Based on the Mono Runtime
Group:          Development/Tools/Other
Requires:       mono-ikvm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package provides IKVM.NET, an open source Java compatibility layer
for Mono, which includes a Virtual Machine, a bytecode compiler, and
various class libraries for Java, as well as tools for Java and Mono
interoperability.

%prep
%setup -q
# For some reason this file is outside the source dir...
cp ../LICENSE .
# fix line endings for rpmlint
dos2unix LICENSE

%build
true

%install
# Create dirs
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/ikvm
mkdir -p ${RPM_BUILD_ROOT}/usr/share/pkgconfig
# Don't install the PdbWriter
rm -f bin/*PdbWriter*
# Install binaries
#  (do iname for JVM.DLL)
find bin* -iname "*\.dll" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
find bin -name "*\.exe" -exec cp {} ${RPM_BUILD_ROOT}/usr/lib/ikvm  \;
# Install some in gac (By request of Jeroen)
OPENJDK=$(find bin -iname "IKVM.OpenJDK.*.dll" -exec basename '{}' ';')
for i in IKVM.AWT.WinForms.dll $OPENJDK IKVM.Runtime.dll ; do
	gacutil -i ${RPM_BUILD_ROOT}/usr/lib/ikvm/$i -package ikvm -root ${RPM_BUILD_ROOT}/usr/lib
	rm -f ${RPM_BUILD_ROOT}/usr/lib/ikvm/$i
done
# Generate wrapper scripts
for f in `find bin . -name "*\.exe"` ; do
        script_name=${RPM_BUILD_ROOT}/usr/bin/`basename $f .exe`
        cat <<EOF > $script_name
#!/bin/sh
exec mono /usr/lib/ikvm/`basename $f` "\$@"
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
Libs: -r:\${libdir}/mono/ikvm/IKVM.Runtime.dll -r:\${libdir}/mono/ikvm/IKVM.OpenJDK.ClassLibrary.dll
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

%changelog
