# spec file for building local build buddy rpm used by Mono team

Name:     	build-buddy
Version: 	1.6.4
Release:	0.novell
Vendor:		Novell, Inc.
BuildRoot:	/var/tmp/%{name}-%{version}-root
License:	GPL
Docdir:         /usr/share/doc/packages

BuildArch:      noarch
URL:		http://www.go-mono.com
Source0:	bb-%{version}.tar.gz
Summary:	Build Buddy for Mono packaging
Group:		Development

# ditch the find/provides specific to perl
#%define __find_requires %{nil}
#%define __find_provides %{nil}

# The above didn't seem to work, but this did
Autoreq: 0
Autoprov: 0

%description
Build Buddy for Mono packaging

%prep
rm -rf "$RPM_BUILD_ROOT"
%setup -n bb-%{version}

%build
perl Makefile.PL
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Move perl modules into a version agnostic path so we don't have to build for each distro
#  (necessary?)
mkdir -p $RPM_BUILD_ROOT/usr/lib/perl5/vendor_perl
mv $RPM_BUILD_ROOT/usr/lib/perl5/site_perl/*/Ximian $RPM_BUILD_ROOT/usr/lib/perl5/vendor_perl

# Install config stuff that otherwise doesn't get installed
######################
DEST=$RPM_BUILD_ROOT/usr/share/ximian-build-system

mkdir -p $DEST/conf

cp -f conf/os.conf $DEST/conf
cp -f conf/bb.conf $DEST/conf
cp -f conf/packsys.conf $DEST/conf

cp -Rf packsys $DEST

mkdir -p $DEST/scripts
cp -f scripts/distribution.guess $DEST/scripts
cp -f scripts/config.guess $DEST/scripts
######################

# Remove unused files:
find $RPM_BUILD_ROOT -name perllocal.pod | xargs rm -f
find $RPM_BUILD_ROOT -name .packlist | xargs rm -f
rm -Rf $RPM_BUILD_ROOT/usr/share/ximian-build-system/packsys/rpm/.cvsignore

%clean
rm -rf "$RPM_BUILD_ROOT"


%files
%defattr(-, root, root)
%doc README
/usr/bin/bb_*
/usr/share/man/man3/Ximian*
/usr/share/man/man1/bb_*
/usr/share/ximian-build-system
/usr/lib/perl5/vendor_perl/Ximian

%changelog
* Tue Sep 21 2006 Novell, Inc.
- New build

