Name:           nant
Version:        0.90
Release:        30
License:        GPL v2 or later; LGPL v2.1 or later
BuildArch:      noarch
Url:            http://nant.sourceforge.net
Source0:        %{name}-%{version}-src.tar.bz2
Summary:        Ant for .NET
Group:          Development/Tools/Building
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  mono-data
BuildRequires:  mono-devel

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%files
%defattr(-, root, root)
%{_bindir}/%{name}
%{_datadir}/NAnt
%{_datadir}/pkgconfig/%{name}.pc

%prep
%setup -q

%build
make

%install
make install prefix=%{_prefix} DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/lib/pkgconfig %{buildroot}%{_datadir}/

%clean
rm -rf %{buildroot}

%changelog
