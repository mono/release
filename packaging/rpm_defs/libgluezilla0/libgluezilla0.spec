%define real_name gluezilla

Name:           libgluezilla0
Version:        2.4
Release:        0
License:        GPL v2 only
Url:            http://www.mono-project.com
Source0:        %{real_name}-%{version}.tar.bz2
Summary:        Glue library for Winforms Web Control
Group:          Development/Languages/Mono
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++ gtk2-devel
####  suse  ####
%if 0%{?suse_version}
%if %suse_version >= 1100
BuildRequires:  mozilla-xulrunner190-devel
%endif
%if %suse_version == 1030
BuildRequires:  mozilla-nspr-devel mozilla-xulrunner181-devel
%endif
%if %suse_version == 1020
BuildRequires:  mozilla-nspr-devel mozilla-xulrunner181-devel
%endif
%if %sles_version == 10
BuildRequires:  gecko-sdk mozilla-nspr-devel mozilla-xulrunner
%endif
%if %sles_version == 9
# Broken: missing nsEmbedCID.h
# mozilla-devel-1.7.8-5.13
BuildRequires:  mozilla-devel pkgconfig
%endif
%endif
####  fedora  ####
%if 0%{?fedora_version}
%if %{fedora_version} == 7
# works if xpcomglue link flag is removed
BuildRequires:  firefox-devel
%endif
%if %{fedora_version} == 6
# Broken: missing nsEmbedAPI.h
# firefox-devel-1.5.0.7-7.fc6
BuildRequires:  firefox-devel
%endif
%if %{fedora_version} == 5
# End of life?
# Broken: missing nsEmbedCID.h
# mozilla-devel-1.7.12-5
BuildRequires:  mozilla-devel
%endif
%endif
%if 0%{?rhel_version}
BuildRequires:  firefox-devel
%endif

%description
A simple library to embed Gecko (xulrunner) for the Mono Winforms
WebControl.



Authors:
--------
    Andreia Gaita <avidigal@novell.com>
    Zac Bowling <zac@zacbowling.com>

%files
%defattr(-, root, root)
%_libdir/libgluezilla.so*
%doc AUTHORS COPYING ChangeLog* INSTALL README TODO

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
rm -f $RPM_BUILD_ROOT/usr/%_lib/libgluezilla.la

%clean
rm -rf "$RPM_BUILD_ROOT"

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
