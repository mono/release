#
# spec file for package boo (Version 0.8.2.2960)
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


Name:           boo
Version:        0.8.2.2960
Release:        1
License:        X11/MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        boo-%{version}-src.zip
Patch1:         boo-pkgconfig_path_fix.patch
Group:          Development/Languages/Other
Summary:        A CLI Scripting Language
BuildArch:      noarch
Url:            http://boo.codehaus.org/Home
BuildRequires:  mono-devel nant unzip
# gtksourceview is required so that we can put the sourceview lang definitions
# in the right location
# On older versions of suse, this was defined as /opt/gnome... make it cross distro
%define gtksourceview_prefix %(pkg-config --variable=prefix gtksourceview-1.0)
%define mime_info_prefix %(pkg-config --variable=prefix shared-mime-info)
# Newer distros include these files, so we don't need to package it in boo
%define include_boo_lang 1
%define include_legacy_mime_info 1
###  SuSE  ######
# Extra requires for old suse distros (which didn't have the expansion stuff)
%if 0%{?suse_version}
%define pre_expansion_requires mono-web gtksourceview-devel gtk2-devel libxml2-devel libgnomeprint-devel libart_lgpl-devel
# 10.3 and later doesn't use mime-info
%if %suse_version >= 1030
%define include_legacy_mime_info 0
%define include_boo_lang 0
BuildRequires:  gtksourceview18-devel shared-mime-info
%endif
# gtksourceview from 10.2 on has boo.lang
%if %suse_version == 1020
%define include_boo_lang 0
BuildRequires:  gtksourceview-devel shared-mime-info
%endif
%if %suse_version == 1010
BuildRequires:  gtksourceview-devel shared-mime-info
%endif
%if %{sles_version} == 9
BuildRequires:  %{pre_expansion_requires}
BuildRequires:  pkgconfig
# shared-mime-info package doesn't exist on sles9... must patch to build instead
%define mime_info_prefix /opt/gnome
%endif
%endif
###  Redhat  ######
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-devel shared-mime-info
%if %{fedora_version} == 5
BuildRequires:  mono-core
%endif
%if %{fedora_version} >= 6
%define include_boo_lang 0
%endif
%endif
# RHEL
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:  gtksourceview-devel shared-mime-info
%define include_boo_lang 0
%endif

%description
Boo is a new object-oriented statically-typed programming language for
the common language infrastructure with a Python-inspired syntax and a
special focus on language and compiler extensibility.



%package devel
License:        X11/MIT
Summary:        A CLI Scripting Language
Group:          Development/Languages/Other
Requires:       boo = %{version}

%description devel
Boo is a new object-oriented statically-typed programming language for
the common language infrastructure with a Python-inspired syntax and a
special focus on language and compiler extensibility.



%prep
# use '-c' because this tarball doesn't come with a top-level dir
%setup -q -c %name-%version
%patch1

%build
# Boo gets the mime info from pkg-config, and sles doesn't have shared-mime-info.pc, hack a hardcode
%if 0%{?sles_version} == 9
sed -i "s/\${pkg-config::get-variable('shared-mime-info','prefix')}/\/opt\/gnome/g" default.build
%endif
%{?env_options}
nant -D:install.prefix=%{_prefix} -D:skip.vs2005=True

%install
%{?env_options}
nant install -D:install.prefix=%{_prefix} -D:install.destdir=${RPM_BUILD_ROOT}
# Move noarch .pc file to /usr/share instead of /usr/lib
mkdir -p ${RPM_BUILD_ROOT}/usr/share
mv ${RPM_BUILD_ROOT}/usr/lib/pkgconfig ${RPM_BUILD_ROOT}/usr/share
# start file list for optional files
touch %name.files
# boo.lang filelist
%define boo_lang %{gtksourceview_prefix}/share/gtksourceview-1.0/language-specs/boo.lang
%if 0%{?include_boo_lang}
echo "%boo_lang" >> %name.files
%else
rm -f $RPM_BUILD_ROOT/%boo_lang
%endif
# mime-info filelist
%if 0%{?include_legacy_mime_info}
echo "%{mime_info_prefix}/share/mime-info/boo.mime" >> %name.files
echo "%{mime_info_prefix}/share/mime-info/boo.keys" >> %name.files
%else
rm -Rf $RPM_BUILD_ROOT/%{mime_info_prefix}/share/mime-info
%endif

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-, root, root)
%{_prefix}/lib/mono/boo
%{_prefix}/lib/mono/gac/Boo.Lang
%{_prefix}/lib/mono/gac/Boo.Lang.CodeDom
%{_prefix}/lib/mono/gac/Boo.Lang.Compiler
%{_prefix}/lib/mono/gac/Boo.Lang.Interpreter
%{_prefix}/lib/mono/gac/Boo.Lang.Parser
%{_prefix}/lib/mono/gac/Boo.Lang.Useful
%{_prefix}/lib/mono/gac/Boo.Lang.Extensions

%files devel -f %name.files
%defattr(-, root, root)
%{_bindir}/*
%{_datadir}/pkgconfig/*.pc
%{_prefix}/lib/boo
%{mime_info_prefix}/share/mime/packages/boo-mime-info.xml

%post
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi

%postun
if test -x usr/bin/update-mime-database ; then
  usr/bin/update-mime-database usr/share/mime >/dev/null
fi
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
* Tue Aug 12 2008 ajorgensen@novell.com
- Split into boo and boo-devel so as to not require nant
* Tue Jun 17 2008 wberrier@suse.de
- Update to 0.8.2.2960
 - (almost) complete nullable type support
 - shorthandsfor nullable types (T?) and enumerables
  (T* instead of IEnumerable[of T])
 - improved booish behavior with nicer colors
  (and it should work inside emacs now )
 - 'else' block for 'for' and 'while loops
 - fixes and improvement related to generic methods
  (overloads and interface declarations)
* Wed Feb 27 2008 wberrier@suse.de
- Update to 0.8.1.2865
 - a simpler way for writing macros
 - support for nested functions
 - generic methods overloading works
 - support for CLR 3.5 extension methods (moreover boo extension methods)
 - compile-time conditionals through ConditionalAttribute and the new -define SYMBOL booc option
 - AttributeUsageAttribute is now supported and enforced
 - a better interactive interpreter (previously known as booish2)
 - warnings about unused private members, unused namespaces, unreachable code
 - new error messages, including suggestions for misspelled members or types
 - exception filters, exception fault handlers
 - for loop IDisposeable.Dispose integration
* Fri Nov 02 2007 wberrier@suse.de
- Update to 0.8.0.2730
 -Fixed Bugs
  * [BOO-836] - WSA Boo "end" keyword required for some blocks and not others
  * [BOO-869] - wrong type inferred for null field initializer
  * [BOO-871] - booish fails to display dictionary that contains DynamicMethod
  * [BOO-874] - compiler doesn't generate debug information for duck typed call sites
  * [BOO-881] - compiler doesn't check for duplicate parameter names in constructor definitions
  * [BOO-883] - Internal error using regular expression in generator
  * [BOO-884] - compiler should prefer data preserving overloads
  * [BOO-885] - parser doesnt allow complex expressions inside closures
  * [BOO-887] - Wrong stack trace information for exception during assignment inside generator method
  * [BOO-891] - Boo.NAnt.Tasks is using an obsolete method (Assembly.LoadWithPartialName)
  * [BOO-893] - QuackInvoke intercepts calls to super() in class CTOR
  * [BOO-894] - Type inference failure for property used in object initializer
  * [BOO-898] - [MetaProgramming] Splicing operator is not recognized inside string expression interpolation
  -Improvements
  * [BOO-870] - parser should not require the 'L' suffix to parse long literals
  * [BOO-872] - better name for closure methods
  * [BOO-873] - extension methods should be preferred over non accessible members
  * [BOO-888] - Delay Sign parameter is ignored
  * [BOO-889] - BooPrinterVistor makes ugly elif chains
  * [BOO-892] - Test Cases use obsolete interfaces and throw warnings during compilation
  * [BOO-895] - [MetaProgramming] splicing for member references
  * [BOO-896] - [MetaProgramming] splicing for class and field names
  * [BOO-897] - [MetaProgramming] splicing for method names
  * [BOO-899] - bool equality comparisons are emitting unnecessary RuntimeServices.EqualityOperator calls
  * [BOO-900] - unreserve 'otherwise' keyword so it can be used by the 'match' macro
  * [BOO-901] - unreserve 'given' and 'when' keywords so they can be implemented as macros
  -New Features
  * [BOO-136] - generic given statement
  * [BOO-218] - duck typing - unary operators
* Wed Oct 10 2007 wberrier@suse.de
- Don't use -<package> notation in BuildRequires anymore.  Normal
  sles9 doesn't like it (obs must intervene here).
* Fri Sep 28 2007 wberrier@suse.de
- Update to 0.7.9.2659
 -boo-pkgconfig_path_fix.patch: fix broken paths in .pc file
* Thu Aug 16 2007 wberrier@suse.de
- Depend on gtksourceview18
* Fri Jul 06 2007 wberrier@novell.com
- Filelist changes: List each assembly dir instead of having this
  package provide /usr/lib/mono/gac
- disable vs2005 project file updates (new in 0.7.8)
- Update to 0.7.8
 -Fixed Bugs:
  * [BOO-603] - GetSlice doesn't work with non-indexed properties
  that return indexable object
  * [BOO-677] - variable argument lists prevent callables from
  being invoked via dictionaries
  * [BOO-724] - Private fields conflict with same named fields in
  child class
  * [BOO-819] - Disallow comparing static ref to function with
  not static ref
  * [BOO-825] - generators compiled with .net 1.1 boo binaries
  dont run with the runtime compiled for .net 2.0
  * [BOO-826] - Internal compiler error when using a generic
  method invocation as the target of a member reference expression
  * [BOO-827] - InvalidCastException when calling overloaded
  function with duck argument
  * [BOO-828] - slice in duck typing mode doesn't work with a
  non indexed property
  * [BOO-829] - Overload resolution and argument conversion is
  not the same in duck typing mode
  * [BOO-831] - CompilerGeneratedExtensions.BeginInvoke is
  ambiguous
  * [BOO-833] - Compiler thinks a property is write-only when
  only the setter is overriden
  -Improvements:
  * [BOO-44] - add pkg-config support to booc and boo nant task
  * [BOO-835] - DSL-friendly method syntax
* Wed Apr 11 2007 wberrier@novell.com
- Add mono dep/req for older distros
* Fri Mar 30 2007 wberrier@novell.com
- Adapt for build service
 -do a crazy hack for sles9 since that platform doesn't have
  shared-mime-info
 -add fedora hack to use /tmp for .wapi
 -use distro specific prefixes for mime-info and gtksourceview
* Tue Jan 30 2007 sbrabec@suse.cz
- Prefix changed to /usr.
- Spec file cleanup.
* Wed Jan 10 2007 wberrier@suse.de
- Also remove /usr/share/gtksourceview* to fix build
* Wed Jan 03 2007 wberrier@suse.de
- Add update-mime-database to post[un] for bnc #225743
  (fix from Andreas Hanke)
* Tue Oct 10 2006 wberrier@suse.de
- Remove boo.lang since it's now in gtksourceview (bnc #209516)
* Tue Aug 01 2006 wberrier@suse.de
- Update to 0.7.6.2237
- Switch to building from original source tarball now that we have
  nant, opposed to repackaging prepackaged binary dist
- minor filesystem changes
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Oct 13 2005 wberrier@suse.de
- Update to 0.7.0 version
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Fri Sep 09 2005 aj@suse.de
- Update check-build.sh.
* Sat Aug 27 2005 aj@suse.de
- Add check-build script.
* Fri Aug 12 2005 ro@suse.de
- fix pkgconfig dir for noarch package
* Thu Aug 04 2005 wberrier@suse.de
- Initial package
