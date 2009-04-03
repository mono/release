Name:     	monodevelop-debugger-gdb
Version:	2.0
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

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%_prefix
make

%install
%{?env_options}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%changelog
