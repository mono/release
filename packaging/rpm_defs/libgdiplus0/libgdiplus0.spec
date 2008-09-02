#
# spec file for package libgdiplus0 (Version 2.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

%define real_name libgdiplus

Name:           libgdiplus0
Version:        2.0
Release:        1
License:        X11/MIT
Url:            http://go-mono.org/
Source0:        %{real_name}-%{version}.tar.bz2
Summary:        Open Source Implementation of the GDI+ API
Group:          Development/Libraries/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      libgdiplus-devel
Provides:       libgdiplus-devel
Obsoletes:      libgdiplus
Provides:       libgdiplus
####  suse  ####
%if 0%{?suse_version}
# Common requires for suse distros
BuildRequires:  fontconfig-devel freetype2-devel glib2-devel libexif libjpeg-devel libpng-devel libtiff-devel
%if %suse_version >= 1030
BuildRequires:  giflib-devel libexif-devel xorg-x11-libSM-devel xorg-x11-libXrender-devel
%endif
%if %suse_version == 1020
BuildRequires:  giflib-devel xorg-x11-libSM-devel xorg-x11-libXrender-devel
%endif
%if %sles_version == 10
BuildRequires:  giflib-devel xorg-x11-devel
%endif
%if %suse_version == 1010
BuildRequires:  giflib-devel xorg-x11-devel
%endif
%if %sles_version == 9
BuildRequires:  XFree86-devel libungif pkgconfig
%endif
%endif
####  fedora  ####
%if 0%{?fedora_version}
# All fedora distros have the same names, requirements
BuildRequires:  fontconfig-devel glib2-devel libXrender-devel libXt-devel libexif-devel libjpeg-devel libpng-devel libtiff-devel libungif-devel
%endif
%if 0%{?rhel_version}
BuildRequires:  fontconfig-devel glib2-devel libexif-devel libjpeg-devel libpng-devel libtiff-devel libungif-devel
%if %{rhel_version} >= 500
BuildRequires:  libXrender-devel libXt-devel
%endif
%endif

%description
This is part of the Mono project. It is required when using
Windows.Forms.



Authors:
--------
    Alexandre Pigolkine
    Duncan Mak
    Jordi Mas
    Miguel de Icaza
    Ravindra Kumar

%files
%defattr(-, root, root)
%_libdir/libgdiplus.so*
%_libdir/pkgconfig/libgdiplus.pc
%doc AUTHORS COPYING ChangeLog* NEWS README

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
* Fri Aug 22 2008 ajorgensen@novell.com
- Update to 2.0 (preview 2)
  * Fixes bnc#402613, lp#246376, bnc#409672, bnc#410124, bnc#413461,
  bnc#410466, bnc#410459, bnc#411454
* Tue Mar 25 2008 wberrier@suse.de
- Update to 1.9.1
 - Fix screen re-draw artifacts in winforms (bnc#388520)
 - Support for limited color displays
- Update to 1.9
 -Disable internal cairo png support, since libgdiplus uses it's
  own.  Saves about 26kb of code size.
 -Fixes related to gdi+ on MacOS.
- Call ldconfig directly instead of invoking a shell.
* Mon Jan 14 2008 wberrier@suse.de
- Renamed package to libgdiplus0 to follow suse lib packaging
  standards
- Update to 1.2.6
 -Internal Cairo updated to 1.4.10
 -Special case for handling path/region excludes from infinity
 -Added GdipCloneFontFamily function
 -TextureBrush now supports transparent bitmaps
* Fri Aug 03 2007 wberrier@suse.de
- Update to 1.2.5
 -Internal Cairo updated to 1.4.6
 -header, types and enums names are now much closer to MS GDI+
 -support for 2bpp PNG and fixes for 4bpp PNG image palettes
 -support for interlaced GIF bitmaps
 -support for ColorMatrixFlag and Gray ColorMatrix in ImageAttributes
 -Implemented GdipDrawImagePointsRect[I] functions
 -Multiple printing fixes (e.g. text size/position)
- Add libexif buildrequires
* Thu Jul 05 2007 wberrier@suse.de
- Fix cairo build (new compiler?) withe ctype patch
  (http://bugs.freedesktop.org/show_bug.cgi?id=10989)
* Tue Jun 05 2007 wberrier@novell.com
- add ldconfig for post/postun
- minor spec file cleanups
- fPIC is already enabled by default, and glitz is disabled
  by default, don't bother adding options for these.
- also provides libgdiplus-devel
- update to 1.2.4
 -update internal cairo to 1.4.2, which offers better performance
 -symbols exports have been cleaned.
  This removes the possible mixup between gtk+/cairo and
  libgdiplus/cairo in newer distros
 -Initial Metafile support (emf & wmf)
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Mar 28 2007 wberrier@novell.com
- Adapt for suse build service
* Thu Mar 01 2007 wberrier@suse.de
- Update to 1.2.3
 -Alpha values for ColorMatrix are now correctly applied and 40%% faster
 -PNG images with alpha channel are now displayed correctly
 -New ICON format decoder (as transparent images)
 -15/16bpp bitmaps are now supported by the BMP decoder
* Sat Dec 02 2006 wberrier@suse.de
- Update to 1.2.2 (Fate #301111)
 -upgrade internal cairo to 1.2.6
* Fri Oct 20 2006 wberrier@suse.de
- Update to 1.1.18
 -Update to cairo 1.2.4
 -fixed to pass S.D. unit tests on big endian archs
 -lots of rendering and parameter bug fixes
* Wed Aug 30 2006 wberrier@suse.de
- Update to 1.1.17
 - upgraded Cairo stack (from 1.0 to 1.2)
 - Windows.Forms: Printing is now supported.
* Mon Jul 31 2006 wberrier@suse.de
- Update to 1.1.16.1.
- update internal cairo to 1.2
- Region operations: Added GdipCombineRegionPath function to allow
  using binary operations (union, intersection, complement,
  exclude and xor) on non-rectangular regions
- Added GdipFlattenPath function (to convert curves into lines)
- Added support for region serialization (i.e. GdipGetRegionData,
  GdipGetRegionDataSize and GdipCreateRegionRgnData functions)
- Better, but still not perfect, clipping support
- TextureBrush is now working again
- Bug Fixes: 75063,76193,76907,77129,77247,77829,77976,78159,78179,
  78181,78185,78213,78237,78284,78336,78383,78478,78721,78742
* Sat Mar 25 2006 wberrier@suse.de
-Update to 1.1.13.5 (Bug fix update from trunk)
 -Avoid drawing zero length strings, fixes
  crash (77699);
 -image.c: Correct rendering of patterns (77438), cleanup all
  resources after being disposed to avoid double frees.
-Fixes without bug numbers (ongoing bug fixing of third
  party commercial components to run on Mono):
 -Gradient brush fixes.
 -font.c: Proper disposing of fonts to avoid leaks.
 -lineargradientbrush.c: fix semantics to match GDI+.
 -Memory leak fixes from running valgrind on the code.
 -Added parameter validation everywhere to avoid crashes from
  missuses: raises an error instead of a segfault.
 -pngcodec.c: Handle saving 8:8:8 files without an alpha channel.
* Tue Feb 28 2006 wberrier@suse.de
- Update to 1.1.13.4.  Fixes bugs (as well as several other updates):
 -144798 (Novell Bugzilla) undefined C code
 -77408
 -77428
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 wberrier@suse.de
- Update to 1.1.13.2
* Fri Jan 06 2006 wberrier@suse.de
- Update to 1.1.13
* Mon Dec 19 2005 wberrier@suse.de
- Obsolete libgdiplus-devel (since it was merged back in) (Bug #131839)
* Thu Dec 15 2005 wberrier@suse.de
- Update to 1.1.11
* Mon Nov 21 2005 wberrier@suse.de
- Cleaned up package deps and patched for new gcc4 which broke cairo
* Thu Nov 10 2005 wberrier@suse.de
- Update to 1.1.10, removed patches that made it upstream
* Fri Oct 07 2005 wberrier@suse.de
- Update to 1.1.9.2, added patch for printf statements
* Wed Sep 21 2005 wberrier@suse.de
- Remove .a, and .la from package [116295 reopened]
* Fri Sep 16 2005 wberrier@suse.de
- remove -devel package [bugzilla#116295]
* Mon Aug 01 2005 ro@suse.de
- update to 1.1.8
* Tue Apr 19 2005 ro@suse.de
- fix sentinel warnings
* Mon Feb 21 2005 clahey@suse.de
- Update to 1.1.4.
* Mon Jan 31 2005 ro@suse.de
- update to svn version for current cairo
* Mon Jan 31 2005 ro@suse.de
- use mono-devel-packages in neededforbuild
- use libgif instead of libungif
* Mon Jan 17 2005 ro@suse.de
- added c++ to neededforbuild (for libtiff)
* Mon Jan 10 2005 ro@suse.de
- update to 1.1.3
* Sun Nov 28 2004 ro@suse.de
- update to 1.1.2
* Sun Nov 28 2004 ro@suse.de
- run autoreconf to fix outdated libtool macros
* Wed Sep 15 2004 ro@suse.de
- update to 1.0.1 bugfix release
* Fri Jul 02 2004 ro@suse.de
- update to 1.0 version
* Mon Jun 21 2004 clahey@suse.de
- Updated to 0.9.
* Wed May 26 2004 ro@suse.de
- added libpng to neededforbuild
* Wed May 19 2004 clahey@suse.de
- Updated to 0.6.
* Tue Apr 20 2004 uli@suse.de
- initial package
