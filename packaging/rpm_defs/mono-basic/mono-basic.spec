%define prebuilt_release 0

Name:           mono-basic
BuildRequires:  mono-devel unzip
License:        LGPL v2.1 or later
Group:          Development/Languages/Mono
Summary:        Mono's VB Runtime
Url:            http://go-mono.org/
Version:        2.2
Release:        6
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-%{version}-%{prebuilt_release}.win4.novell.x86.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version} || 0%{?rhel_version}
%define env_options export MONO_SHARED_DIR=/tmp
%endif

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's VB runtime.



Authors:
--------
    Miguel de Icaza <miguel@ximian.com>
    Paolo Molaro <lupus@ximian.com>
    Dietmar Maurer <dietmar@ximian.com>

%files
%defattr(-, root, root)
%_mandir/man1/vbnc.1%
%_prefix/bin/vbnc
%_prefix/lib/mono/2.0/vbnc*
%_prefix/lib/mono/gac/Microsoft.VisualBasic
%_prefix/lib/mono/*/Microsoft.VisualBasic.dll

%prep
%setup -q

%build
%{?env_options}
./configure --prefix=/usr
make

%install
## Get ms.net runtime out of noarch rpm (building in buildservice or autobuild)
if [ ! -e %{S:1} ] ; then
	# Check for binaries built on windows (for building on monobuild)
	if test %{prebuilt_release} == 0 ; then
		release_dir=""
	else
		release_dir="-%{prebuilt_release}"
	fi
	file="%{name}-%{version}-%{prebuilt_release}.win4.novell.x86.zip"
	path="win-4-i386/%{name}/%{version}${release_dir}/files/downloads/$file"
	pushd %{_sourcedir}
	wget --tries=1 --timeout=10 http://build.mono.lab.novell.com/builds/RELEASE/$path || true
	wget --tries=1 --timeout=10 http://build.mono.lab.novell.com/builds/HEAD/$path || true
	popd
fi
# If we have windows built binaries, inject them into the package (to provide the 1.0 runtime)
if [ -e %{S:1} ] ; then 
	unzip %{S:1}
	# Remove vbnc built runtime
	rm -Rf ${RPM_BUILD_ROOT}/%_prefix/lib/mono/gac/Microsoft.VisualBasic/7.0.*
	# Fix permissions on files so they are readable
	chmod 755 lib/mono/1.0/Microsoft.VisualBasic.dll
	## Install into new gac
	gacutil -package 1.0 -root ${RPM_BUILD_ROOT}/usr/lib -i lib/mono/1.0/Microsoft.VisualBasic.dll
else
	# If we're building from HEAD, print warning (HEAD doesn't have a version with periods)
	if test `echo "%{version}" | sed -e 's/\.//g'` == "%{version}" ; then
		echo ""
		echo "*** vbnc DEBUG BUILD!  Don't ship this RPM! ***"
		echo ""
	# Otherwise RELEASE, fail build, because we don't want to ship an rpm without the 1.0 runtime
	else
		false
	fi
fi
%{?env_options}
make install DESTDIR=%buildroot
cd %buildroot
rm -f .%{_prefix}/lib/mono/2.0/extract-source.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-console.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-execute.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt.exe*

%clean
rm -rf ${RPM_BUILD_ROOT}
%if 0%{?fedora_version} || 0%{?rhel_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'

%changelog
