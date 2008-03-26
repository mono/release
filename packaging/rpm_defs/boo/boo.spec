
# norootforbuild

Name:           boo
Version:        0.8.1.2865
Release:        1
License:        X11/MIT
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        boo-%{version}-src.zip
Patch1:		boo-pkgconfig_path_fix.patch
Group:          Development/Languages/Other
Summary:        A CLI Scripting Language
BuildArch:      noarch
URL:            http://boo.codehaus.org

BuildRequires:  mono-devel nant unzip

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
BuildRequires:	gtksourceview18-devel shared-mime-info
%endif

# gtksourceview from 10.2 on has boo.lang
%if %suse_version == 1020
%define include_boo_lang 0
BuildRequires:	gtksourceview-devel shared-mime-info
%endif

%if %suse_version == 1010
BuildRequires:	gtksourceview-devel shared-mime-info
%endif

%if %{sles_version} == 9
BuildRequires:	%{pre_expansion_requires}
BuildRequires:	pkgconfig
# shared-mime-info package doesn't exist on sles9... must patch to build instead
%define mime_info_prefix /opt/gnome
%endif

%endif

###  Redhat  ######
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
%define env_options export MONO_SHARED_DIR=/tmp

BuildRequires:	gtksourceview-devel shared-mime-info

%if %{fedora_version} == 5
BuildRequires: mono-core
%endif

%if %{fedora_version} >= 6
%define include_boo_lang 0
%endif

%endif

# RHEL
%if 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
BuildRequires:	gtksourceview-devel shared-mime-info
%define include_boo_lang 0
%endif

%description
Boo is a new object oriented statically typed programming language for the Common Language Infrastructure with a python inspired syntax and a special focus on language and compiler extensibility.

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

%files -f %name.files
%defattr(-, root, root)
%{_bindir}/*
%{_datadir}/pkgconfig/*.pc
%{_prefix}/lib/boo
%{_prefix}/lib/mono/boo
%{_prefix}/lib/mono/gac/Boo.Lang
%{_prefix}/lib/mono/gac/Boo.Lang.CodeDom
%{_prefix}/lib/mono/gac/Boo.Lang.Compiler
%{_prefix}/lib/mono/gac/Boo.Lang.Interpreter
%{_prefix}/lib/mono/gac/Boo.Lang.Parser
%{_prefix}/lib/mono/gac/Boo.Lang.Useful
%{_prefix}/lib/mono/gac/Boo.Lang.Extensions
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
