
# norootforbuild

Name:           gluezilla
Version:	0.1
Release:	0
Vendor:         Novell, Inc.
License:        GPL
URL:            http:/www.go-mono.com
Source0:        %{name}-%{version}.tar.bz2
Summary:        Glue library for Winforms Web Control
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

####  suse  ####
%if 0%{?suse_version}

# Common requires for suse distros
BuildRequires: gcc-c++ mozilla-nspr-devel mozilla-xulrunner181-devel

%if %suse_version >= 1030
#BuildRequires:  
%endif

%if %suse_version == 1020
#BuildRequires:  
%endif

%if %sles_version == 10
#BuildRequires:  
%endif

%if %suse_version == 1010
#BuildRequires:  
%endif

%if %suse_version == 1000
#BuildRequires:  
%endif

%if %sles_version == 9
#BuildRequires:  
%endif

%endif


####  fedora  ####
%if 0%{?fedora_version}

# All fedora distros have the same names, requirements
#BuildRequires: 

%endif

%if 0%{?rhel_version}
#BuildRequires: 
%endif


%description
Glue library for Winforms Web control

%files
%defattr(-, root, root)
%_libdir/libgluezilla.so*
#%_libdir/pkgconfig/libgdiplus.pc
%doc AUTHORS COPYING ChangeLog* INSTALL NEWS README TODO

%debug_package
%prep
%setup -q

%build
# Set PKG_CONFIG_PATH for sles9
%if 0%{?sles_version}
%if %sles_version == 9
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/opt/gnome/%_lib/pkgconfig
%endif
%endif

export CFLAGS="$RPM_OPT_FLAGS"
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Unwanted files:
rm -f $RPM_BUILD_ROOT/usr/%_lib/libgluezilla.la

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
