%define boo_version %(rpm -q boo-devel --queryformat '%{VERSION}')

Name:           monodevelop-boo
Version:        1.9.1
Release:        96
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.monodevelop.com
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  boo-devel mono-devel monodevelop
Summary:        Monodevelop Boo Addin
Group:          Development/Languages/Mono
# Boo's assemblies are always version at 1.0.0.0.  Force built against or newer.
Requires:       boo-devel >= %boo_version
BuildRequires:  gtksourceview-sharp2 monodoc-core
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
Boo language integration with Mono develop.  Supports syntax
highlighting and code completion.



%files -f %{name}.lang
%defattr(-, root, root)
%_prefix/share/pkgconfig/monodevelop-boo.pc
%_prefix/lib/monodevelop/AddIns/BooBinding/BooShell.dll*
%_prefix/lib/monodevelop/AddIns/BooBinding/BooBinding.dll*
%dir %_prefix/lib/monodevelop/AddIns/BooBinding
%dir %_prefix/lib/monodevelop/AddIns/BooBinding/locale

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%_prefix
make

%install
%{?env_options}
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%_prefix/share/pkgconfig
mv $RPM_BUILD_ROOT%_prefix/lib/pkgconfig/*.pc $RPM_BUILD_ROOT%_prefix/share/pkgconfig
%find_lang %{name}

%clean
rm -rf "$RPM_BUILD_ROOT"
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
