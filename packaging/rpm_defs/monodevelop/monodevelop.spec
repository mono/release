#
# spec file for package monodevelop (Version 1.0)
#
# Copyright (c) 2008 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           monodevelop
BuildRequires:  gconf-sharp2 gtk-sharp2-gapi gtksourceview-sharp2 intltool mono-addins mono-basic mono-devel mono-nunit monodoc-core perl-XML-Parser shared-mime-info xsp
Url:            http://www.go-mono.com/
License:        GPL v2 or later
Group:          Development/Languages/Mono
AutoReqProv:    on
Version:        1.0
Release:        9
Summary:        A Full-Featured IDE for Mono and Gtk#
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
Requires:       xsp
Requires:       mono-basic
Requires:       pkgconfig
PreReq:         shared-mime-info
%if 0%{?suse_version}
BuildRequires:  desktop-file-utils update-desktop-files
%endif
# TODO: Add build requirements for xulrunner/mozilla, etc... md does some checks at build time for aspnetedit
#  (not currently enabled, but we'll need those checks when it is)
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
# TODO: what to do here on fedora?
%define suse_update_desktop_file true
%define run_suseconfig true
%endif
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%define suse_update_desktop_file true
%define run_suseconfig true
%endif

%description
MonoDevelop is intended to be a full-featured integrated development
environment (IDE) for mono and Gtk#. It was originally a port of
SharpDevelop 0.98. See http://monodevelop.com/ for more information.



%prep
%setup -q

%build
%{?env_options}
./configure --prefix=%{_prefix} \
	    --enable-subversion \
	    --enable-monoextensions \
	    --enable-aspnet \
	    --disable-update-mimedb \
	    --disable-update-desktopdb \
	    --enable-tests
make

%install
%{?env_options}
make install DESTDIR=$RPM_BUILD_ROOT GACUTIL_FLAGS="/package monodevelop /root ${RPM_BUILD_ROOT}/usr/%_lib"
#
mkdir -p $RPM_BUILD_ROOT/usr/share/pkgconfig
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/* $RPM_BUILD_ROOT/usr/share/pkgconfig
%suse_update_desktop_file -N "Mono Development Environment" -G "Integrated Development Environment" -C "Develop software using Mono tools" %name "Application Development IDE"
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/share/applications/monodevelop.desktop
%{_prefix}/share/mime/packages/monodevelop.xml
%{_datadir}/icons/hicolor/*/apps/monodevelop.png
%{_datadir}/icons/hicolor/scalable/apps/monodevelop.svg
%{_prefix}/lib/monodevelop
%{_prefix}/share/pkgconfig/monodevelop.pc
%{_prefix}/share/pkgconfig/monodevelop-core-addins.pc
%{_mandir}/man1/mdtool.1.gz
%{_mandir}/man1/monodevelop.1.gz

%post
update-mime-database /usr/share/mime >/dev/null || :
%run_suseconfig -m gtk2

%postun
update-mime-database /usr/share/mime >/dev/null || :
%run_suseconfig -m gtk2
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Wed Apr 09 2008 wberrier@suse.de
- Remove vte-sharp2 from build requires.  It's not needed,
  and that package doesn't exist anymore.
* Wed Mar 26 2008 wberrier@suse.de
- Update to 1.0
 -Bug fixes:
  - MD Crashes when you drag a menu inside its own submenu
  (bnc#363865)
  - Monodevelop and stetic destroy forms (bnc#362596)
  - Problem with subclassing any container widget (bnc#361650)
  - Version Control doesn't behave propertly (bnc#363858)
  - Comment and uncomment function (bnc#325469)
  - Create Package fails on projects with translations (bnc#362567)
  - Exception with null arguments or nonexistant paths when
  compiling/cleaning C project (bnc#361045)
  - MonoDevelop crashes when creating/opening C++ Console Project
  (bnc#359567)
  - Build Output autohide button missing (bnc#368436)
  - Have to hit esc twice to close the file/new file dialog
  (bnc#358361)
- Changes in 0.19 (1.0 RC1)
 -Will use 2.0 runtime as default
 -Icons have been tango-ified
 -More than 85 bugs fixed
* Mon Jan 14 2008 wberrier@suse.de
- Fixed .desktop file to adhear to standards
- Fix naming of Slovenian translation
- Update to 0.18
 -packaging split (database, boo, and java in separate packages)
 -Improved Dock Manager
 -Circa 75 bugfixes
- Update to 0.17
 -Deployment of ASP.NET projects
 -Support for VS 2005 Web Application projects
 -ASP.NET Codebehind Generation Improvements
 -Generation of Satellite Assemblies
 -Makefile generation improvements
 -Various other IDE enhancements
 -Circa 90 bugfixes
* Wed Oct 10 2007 wberrier@suse.de
- Don't use fdupes afterall (fails build)
* Tue Oct 09 2007 wberrier@suse.de
- Update to 0.16
 -C/C++ Support
 -New Database Add-in
 -Text editor improvements
 -On-the-fly error underlining
 -Auto-generation of XML comment tags
 -New ASP.NET features
 -Multiple GTK# versions
 -ChangeLog add-in
 -More than 100 bugs fixed
* Mon Sep 24 2007 wberrier@suse.de
- monodevelop-fix_kde_crash_r86138.patch: fix #309204
* Fri Aug 03 2007 maw@suse.de
- Use %%fdupes.
* Fri Aug 03 2007 wberrier@suse.de
- Remove upstream monodevelop-rename_ja_JP.patch
- Update to 0.15
 -Configurable keybindings
 -Output pad pinning
 -Makefile integration
 -Standard header support for source files
 -Localization add-in preview
 -Text editor improvements
 -Updated gtk# designer (support for gtk# 2.8 and 2.10 widgets)
 -Assembly signing
 -Message log for internal messages
 -More than 60 bugs fixed
* Thu Jun 14 2007 wberrier@novell.com
- Put ja_JP locale files in valid location
  (monodevelop-rename_ja_JP.patch)
- Update to 0.14
 -Improved Toolbox and Properties pad
 -Subversion add-in updates
  -auth prompts
  -supports newer versions of subversion
 -New refactory operations:
  -rename
  -implement interface
  -encapsulate field
 -Search by filename or classname in Open Solution File Dialog
 -New class and member selector when browsing source
 -Improved smart indenting for C#
 -Project export/conversion
 -Packaging features: automatic bundling of an app
 -Desktop integration: automatically generate  shell wrappers,
  .desktop and .pc files
 -Improved New Project dialog
 -New Navigation Toolbar
 -Gtk# Designer updates:
  -better widget defaults
  -supports internal and custom widgets
  -images assigned to widgets are automatically added to project
 -Can add file to project while creating them
 -Improved VS2005 support and VS integration
 -VB.Net support utilizes new vbnc compiler
 -Close to 100 bugs fixed
* Wed May 16 2007 wberrier@novell.com
- Remove gtkhtml2-devel from BuildRequires (not needed, allows
  building on sle10)
* Tue Apr 24 2007 wberrier@novell.com
- Depend on version of boo found at build time
* Fri Apr 13 2007 wberrier@novell.com
- add %%debug_package so debug packages get created
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Thu Apr 05 2007 wberrier@suse.de
- Update to 0.13.1:
 -Bugfix release to fix some asp.net compilation issues
- Adapt for buildservice
- Clean up unnecessary BuildRequires
* Thu Mar 01 2007 wberrier@suse.de
- Update to 0.13:
 -More than 70 bugs fixed
 -Revamped VersionControl addin
 -New task view features (TODO type lists)
 -Code completion improvements and fixes
 -Native support for VisualStudio 2005 Project files
 -Custom commands in projects
 -Makefile integration
 -New Generic Project Type
 -New Deployment infrastruction
 -Automatic project reloading when changes in files detected
  while the project is open
 -Gtk# designer improvements (Undo/Redo support)
 -Context sensitive help for classes when F1 is pressed
 -Support for Win32Icon and Win32Resource options in C# projects
 -New Layout toolbar which includes a combobox for fast layout
  switching
 -Support for files outside of a project directory
 -Editor wrap mode selector
 -File viewer selector (possible to have multiple viewers for
  a filetype)
 -Improvements in ASP.NET support:
  -added a new option that can be used to disable compilation-time
  CodeBehind verification for different configurations
  -Several important stability fixes in AspNetEdit
  -Improvements to toolbox, now includes default items with icons
 -New Go to Type dialog, for easily jumping to a class defined
  in a project
* Mon Jan 22 2007 ro@suse.de
- drop requires for gnome-filesystem
* Wed Jan 03 2007 wberrier@suse.de
- handle mime files properly
 -spec file fixes from Andreas Hanke to fix bnc #225812
* Thu Oct 19 2006 ro@suse.de
- added mono-devel to buildrequires
* Tue Sep 05 2006 wberrier@suse.de
- Update to 0.12
 -Better code completion support, supports C# 2.0
 -Class information is shown using the syntax of the current
  language
 -New "Open With" Menu
 -stetic menu designer
 -autotools project support
 -additional addin management features
 -Support for multiple text file encodings
 -ASP.NET Support
 -Lots of bug fixes and better stability
* Wed Aug 30 2006 wberrier@suse.de
- Add mono-nunit to BuildRequires
* Mon Jul 31 2006 wberrier@suse.de
- Update to 0.11
- Lots of new features and fixes, too many to list here.  One big
  addition is the stetic gui designer integration
- 2.4.0 -> 2.8.0 hack now unnecessary
* Sun Mar 26 2006 ro@suse.de
- removed ifarch from noarch package
* Fri Mar 24 2006 wberrier@suse.de
- Require mono-basic so that vbnet templates will compile
* Wed Mar 15 2006 wberrier@suse.de
- Update references for gtk# 2.4 to 2.8 in template files
  ** Otherwise all the gtk#2 template projects will fail to compile **
* Mon Mar 13 2006 wberrier@suse.de
- Remove mime.cache and quote update_desktop args
* Fri Feb 17 2006 gekker@suse.de
- fixup desktop file for UI team
* Wed Feb 01 2006 aj@suse.de
- Fix Requires and BuildRequires to build again.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 13 2006 gekker@suse.de
- Fixup nfb and Requires for new gtk-sharp2 packaging
* Mon Jan 09 2006 gekker@suse.de
- Fix to build against new mono version 1.1.13
* Mon Dec 12 2005 wberrier@suse.de
- Convert to noarch package, and clean up build deps
* Tue Nov 29 2005 wberrier@suse.de
- Update to 0.9 (which obsoletes the version control patch)
* Fri Nov 18 2005 wberrier@suse.de
- Patch VersionControl AddIn to compile with mcs 1.1.10
* Mon Nov 07 2005 sbrabec@suse.cz
- Renamed rename *-sharp-2_0 to *-sharp2 in Requires (#132436).
* Tue Oct 25 2005 ro@suse.de
- remove mono-debugger from nfb for the moment
* Thu Oct 20 2005 ro@suse.de
- rename gecko-sharp-2_0 and gtksourceview-sharp-2_0 in nfb
* Thu Oct 13 2005 wberrier@suse.de
- Update to 0.8 and add configure options (--enable-nunit --enable-versioncontrol --enable-monoextensions)
* Thu Sep 22 2005 ro@suse.de
- remove libgdiplus-devel from nfb (dropped)
* Tue Sep 13 2005 gekker@suse.de
- Disable boo support so monodevelop will run (113802)
* Sun Sep 04 2005 aj@suse.de
- Update check-build.sh.
* Tue Aug 30 2005 ro@suse.de
- do not require mono-debugger on ppc (can not build there)
* Fri Aug 26 2005 ro@suse.de
- nfb: monodoc -> monodoc-core
* Thu Aug 18 2005 gekker@suse.de
- Fix desktop category for menus.
* Tue Aug 16 2005 aj@suse.de
- Add check-build script.
* Tue Aug 09 2005 gekker@suse.de
- Fix requirements
- Remove files that conflict with shared-mime-info
- Verify that bugs #71734 and #71735 are fixed
* Sun Aug 07 2005 ro@suse.de
- rename nfb and deps for gtksourceview-sharp and gecko-sharp
* Thu Aug 04 2005 gekker@suse.de
- Update to version 0.7
- Remove upstreamed patches
* Wed May 18 2005 gekker@suse.de
- fix to build with mono-1.1.7
* Tue Mar 01 2005 gekker@suse.de
- fix requires (66770).
* Tue Feb 15 2005 ro@suse.de
- fix build on x86_64
* Tue Feb 08 2005 gekker@suse.de
- Add patches to fix namespacing issues.
- Add suse_update_desktop_config
* Mon Dec 13 2004 clahey@suse.de
- New package.
