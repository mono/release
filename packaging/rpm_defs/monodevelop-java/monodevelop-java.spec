Name:           monodevelop-java
Version:        1.9.1
Release:        1
License:        GPL v2 or later
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
AutoReqProv:    on
BuildArch:      noarch
Url:            http://www.monodevelop.com
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  ikvm mono-devel monodevelop
Requires:       ikvm
Summary:        Monodevelop Java Addin
Group:          Development/Languages/Mono

%description
Java language integration with MonoDevelop based on ikvm.

%files -f %{name}.lang
%defattr(-, root, root)
%{_datadir}/pkgconfig/monodevelop-java.pc
%{_prefix}/lib/monodevelop/AddIns/JavaBinding/JavaBinding.dll*
%dir %{_prefix}/lib/monodevelop/AddIns/JavaBinding
%dir %{_prefix}/lib/monodevelop/AddIns/JavaBinding/locale

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%{_prefix}
make

%install
%{?env_options}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/*.pc %{buildroot}%{_datadir}/pkgconfig
%find_lang %{name}

%clean
rm -rf %{buildroot}

%changelog
