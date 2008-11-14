Name:     	monodevelop-debugger-gdb
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
Requires:	gdb
Summary:	GDB for MonoDevelop
Group:		Development/Tools

%description
GDB Debugger Addin for MonoDevelop.

%files
%defattr(-, root, root)
%{_prefix}/lib/monodevelop/AddIns/MonoDevelop.Debugger/MonoDevelop.Debugger.Gdb.dll*
%{_datadir}/pkgconfig/monodevelop.debugger.gdb.pc

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%_prefix
make

%install
%{?env_options}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_prefix}/share/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/*.pc %{buildroot}%{_prefix}/share/pkgconfig/

%clean
rm -rf %{buildroot}

%changelog
