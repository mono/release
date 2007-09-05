
# norootforbuild

Name:           mono-basic
BuildRequires:  mono-devel
License:        GNU Library General Public License v. 2.0 and 2.1 (LGPL)
Group:          Development/Languages/Other
Summary:        Mono's VB runtime
URL:            http://go-mono.org/
Version:	1.2.5
Release:	0.novell
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-%{version}-0.novell.noarch.rpm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

# Fedora options (Bug in fedora images where 'abuild' user is the same id as 'nobody')
%if 0%{?fedora_version}
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
%_prefix/bin/vbnc
%_prefix/lib/mono/2.0/vbnc*
%_prefix/lib/mono/gac/Microsoft.VisualBasic
%_prefix/lib/mono/*/Microsoft.VisualBasic.dll

%debug_package
%prep
%setup -q

%build
%{?env_options}
./configure --prefix=/usr
make

%install
%{?env_options}
make install DESTDIR=${RPM_BUILD_ROOT}

## Get ms.net runtime out of noarch rpm (building in buildservice or autobuild)
if [ -e %{S:1} ] ; then
	rpm2cpio %{S:1} | cpio -idv
	# Remove vbnc built runtime
	rm -Rf ${RPM_BUILD_ROOT}/usr/lib/mono/gac/Microsoft.VisualBasic
	rm -Rf ${RPM_BUILD_ROOT}/usr/lib/mono/2.0/Microsoft.VisualBasic.dll
	## Install runtime from noarch.rpm into new gac
	gacutil -package 1.0 -root ${RPM_BUILD_ROOT}/usr/lib -i usr/lib/mono/1.0/Microsoft.VisualBasic.dll
	gacutil -package 2.0 -root ${RPM_BUILD_ROOT}/usr/lib -i usr/lib/mono/2.0/Microsoft.VisualBasic.dll
else
        # Check for binaries built on windows (for building on monobuild)
        f="mono-basic-%{version}-0.win4.novell.x86.zip"
        p="win-4-i386/mono-basic/%{version}/files/downloads/$f"
        wget --tries=1 --timeout=10 http://c243.mono.lab.novell.com/builds/RELEASE/$p || true
        wget --tries=1 --timeout=10 http://c243.mono.lab.novell.com/builds/HEAD/$p || true

        # If we have windows built binaries, inject them into the package (to provide the 1.0 runtime)
        if [ -e "$f" ] ; then 
                unzip mono-basic-%{version}-0.win4.novell.x86.zip
                # Remove vbnc built runtime
                rm -Rf ${RPM_BUILD_ROOT}/%_prefix/lib/mono/gac/Microsoft.VisualBasic
                rm -Rf ${RPM_BUILD_ROOT}/%_prefix/lib/mono/2.0/Microsoft.VisualBasic.dll

                # Fix permissions on files so they are readable
                chmod 755 lib/mono/1.0/Microsoft.VisualBasic.dll lib/mono/2.0/Microsoft.VisualBasic.dll

                ## Install into new gac

                gacutil -package 1.0 -root ${RPM_BUILD_ROOT}/usr/lib -i lib/mono/1.0/Microsoft.VisualBasic.dll
                gacutil -package 2.0 -root ${RPM_BUILD_ROOT}/usr/lib -i lib/mono/2.0/Microsoft.VisualBasic.dll
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
fi

# Not needed in 1.2.4, since we can bootstrap vbnc
# ship prebuilt vbnc for now...
#mkdir -p ${RPM_BUILD_ROOT}/usr/bin
#cp -f usr/bin/vbnc ${RPM_BUILD_ROOT}/usr/bin
#cp usr/lib/mono/2.0/vbnc.* ${RPM_BUILD_ROOT}/usr/lib/mono/2.0

cd $RPM_BUILD_ROOT
rm -f .%{_prefix}/lib/mono/2.0/extract-source.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-console.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt-execute.exe*
rm -f .%{_prefix}/lib/mono/2.0/rt.exe*

%clean
rm -rf ${RPM_BUILD_ROOT}

# auto dep/req generation for older distros (it will take a while for the .config scanning to get upstream)
%if 0%{?suse_version} <= 1040 || 0%{?fedora_version} <= 7
%if 0%{?fedora_version}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%endif
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort | uniq'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort | uniq'
%endif

%changelog
