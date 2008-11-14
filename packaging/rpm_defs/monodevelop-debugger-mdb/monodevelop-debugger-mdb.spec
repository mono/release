Name:     	monodevelop-debugger-mdb
Version:	1.9.1
Release:	0
Vendor:		Novell, Inc.
License:	MIT/X11
Autoreqprov:    on
BuildArch:      noarch
URL:		http://www.monodevelop.com
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:	monodevelop = %{version} mono-devel mono-debugger
Requires:       mono-debugger
Summary:	MonoDevelop Debugger
Group:		Development/Tools

%description
Mono Debugger Addin for MonoDevelop.

%files
%defattr(-, root, root)
%{_prefix}/lib/monodevelop/AddIns/MonoDevelop.Debugger/DebuggerClient.dll*
%{_prefix}/lib/monodevelop/AddIns/MonoDevelop.Debugger/DebuggerServer.exe*
%{_datadir}/pkgconfig/mono.debugging.backend.mdb.pc

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/*.pc %{buildroot}%{_datadir}/pkgconfig/

%clean
rm -rf %{buildroot}

%changelog
