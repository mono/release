
# norootforbuild

Name:           last-exit
Version:        4
Release:        3
License:        GNU General Public License (GPL)
URL:            http://www.o-hand.com/~iain/last-exit/
Source0:        last-exit-%{version}.tar.bz2
BuildRequires:  dbus-1-devel dbus-1-glib-devel gconf-sharp2 gconf2-devel glade-sharp2 glib-sharp2 gnome-sharp2 gstreamer010-devel gstreamer010-plugins-base-devel gtk-sharp2 gtk2-devel mono-data mono-devel perl-XML-Parser update-desktop-files
Summary:        Last Exit is a player for Last.fm written for gtk# and Mono
Group:          Productivity/Multimedia/Sound/Players
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%gconf_schemas_prereq

%description
Listen with Last.fm and fuel the social music revolution. It´s easy.
What are *you* listening to?



Authors:
--------
    Iain * <iain@gnome.org>

%debug_package
%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=/usr \
	--libdir=/usr/%_lib \
	--sysconfdir=/etc
make

%install
make install DESTDIR=${RPM_BUILD_ROOT}
%suse_update_desktop_file last-exit AudioVideo Player
%find_gconf_schemas
#Include -f for list of schema files

%files -f %{name}.schemas_list
%defattr(-, root, root)
/usr/bin/last-exit
/usr/%_lib/last-exit
/usr/share/applications/last-exit.desktop
/usr/share/icons/hicolor/*/actions/show-info.*
/usr/share/icons/hicolor/*/actions/tag-new.*
/usr/share/icons/hicolor/*/apps/last-exit.*

%pre -f %{name}.schemas_pre

%preun -f %{name}.schemas_preun

%posttrans -f %{name}.schemas_posttrans

%changelog
