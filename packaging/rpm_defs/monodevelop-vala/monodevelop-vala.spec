Name:     	monodevelop-vala
Version:	1.9.1
Release:	0
Vendor:		Novell, Inc.
License:	MIT/X11
Autoreqprov:    on
BuildArch:      noarch
URL:		http://www.monodevelop.com
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:	monodevelop = %{version} mono-devel
Requires:	vala
Summary:	Monodevelop Vala Addin
Group:		Development/Tools

%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Vala language support for MonoDevelop.

%files
%defattr(-, root, root)
%_prefix/lib/monodevelop/AddIns/BackendBindings/MonoDevelop.ValaBinding.dll

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%_prefix
make

%install
%{?env_options}
make install DESTDIR=${RPM_BUILD_ROOT}

%clean
rm -rf "$RPM_BUILD_ROOT"

%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog