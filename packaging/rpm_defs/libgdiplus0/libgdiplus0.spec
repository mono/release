
# norootforbuild

%define real_name libgdiplus

Name:           libgdiplus0
Version:	1.2.6
Release:	0
Vendor:         Novell, Inc.
License:        GPL
URL:            http:/www.go-mono.com
Source0:        %{real_name}-%{version}.tar.bz2
Summary:        libgdiplus: An Open Source implementation of the GDI+ API.
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      libgdiplus-devel
Provides:	libgdiplus-devel
Obsoletes:      libgdiplus
Provides:	libgdiplus

####  suse  ####
%if 0%{?suse_version}

# Common requires for suse distros
BuildRequires: libjpeg-devel libtiff-devel libpng-devel glib2-devel fontconfig-devel freetype2-devel libexif

%if %suse_version >= 1030
BuildRequires:  giflib-devel xorg-x11-libXrender-devel xorg-x11-libSM-devel libexif-devel
%endif

%if %suse_version == 1020
BuildRequires:  giflib-devel xorg-x11-libXrender-devel xorg-x11-libSM-devel
%endif

%if %sles_version == 10
BuildRequires:  giflib-devel xorg-x11-devel
%endif

%if %suse_version == 1010
BuildRequires:  giflib-devel xorg-x11-devel
%endif

%if %sles_version == 9
BuildRequires:  libungif XFree86-devel pkgconfig
%endif

%endif


####  fedora  ####
%if 0%{?fedora_version}

# All fedora distros have the same names, requirements
BuildRequires: libungif-devel libjpeg-devel libtiff-devel libpng-devel glib2-devel fontconfig-devel libXrender-devel libXt-devel libexif-devel

%endif

%if 0%{?rhel_version}
BuildRequires: libungif-devel libjpeg-devel libtiff-devel libpng-devel glib2-devel fontconfig-devel libexif-devel
%endif


%description
libgdiplus: An Open Source implementation of the GDI+ API, it is part of the Mono Project

%files
%defattr(-, root, root)
%_libdir/libgdiplus.so*
%_libdir/pkgconfig/libgdiplus.pc
%doc AUTHORS COPYING ChangeLog* NEWS README

%debug_package
%prep
%setup -q -n %{real_name}-%{version}

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
rm -f $RPM_BUILD_ROOT/usr/%_lib/libgdiplus.a
rm -f $RPM_BUILD_ROOT/usr/%_lib/libgdiplus.la

# Remove generic non-usefull INSTALL file... (appeases
#  suse rpmlint checks, saves 3kb)
find . -name INSTALL | xargs rm -f

%clean
rm -rf "$RPM_BUILD_ROOT"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
