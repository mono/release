#!/bin/sh -x

#startup options
CLEAN=NO
CONFIGURE=$1
MAKE=$2
INSTALL=$3
MONOBUILDFILES=$4

BUILDROOT=/Users/Shared/MonoBuild
PLISTS=${BUILDROOT}/plists
RESOURCES=${BUILDROOT}/resources
MONOVERSION=1.1.7
FRAMEWORKPREFIX=/Library/Frameworks/Mono.framework
MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/${MONOVERSION}
DEPS=${BUILDROOT}/Dependancies

export CFLAGS="-I${MONOPREFIX}/include" 
export C_INCLUDE_FLAGS="-I${MONOPREFIX}/include"
export CPATH="${MONOPREFIX}/include"
export DYLD_LIBRARY_PATH="${MONOPREFIX}/lib"
export LDFLAGS="-L${MONOPREFIX}/lib"
export PATH="/usr/X11R6/bin/:${MONOPREFIX}/bin:$PATH"
export PKG_CONFIG_PATH="/usr/X11R6/lib/pkgconfig/:$PKG_CONFIG_PATH"
export ACLOCAL_FLAGS="-I ${MONOPREFIX}/share/aclocal/"

#		if [ ! -d ${MONOPREFIX}/lib ]; then
mkdir -p ${MONOPREFIX}/lib
mkdir -p ${MONOPREFIX}/man
mkdir -p ${MONOPREFIX}/bin
#        fi

if [ ! -d ${DEPS} ]; then
    mkdir -p ${DEPS}
fi


fetch()
{
	cd ${DEPS}
	if [ ! -e ${DEPS}/$1 ];then
		curl -L --max-redirs 5 -s -O $2
		gnutar -xzf $3
	fi
}

if [ ! -e ${DEPS} ]; then
	mkdir -p ${DEPS}
fi

build()
{
	cd $1
	if [ ${CLEAN} == "YES" ]; then
		make clean
	fi
	if [ ${CONFIGURE} == "YES" ]; then
		if [ $2 == "mono" ]; then
		
			###############################################
#Create gacutil config files specific to OS X
cat <<EOF > mcs/class/lib/default/System.Drawing.dll.config
<configuration>
        <dllmap dll="gdiplus.dll" target="/Library/Frameworks/Mono.framework/Versions/${MONOVERSION}/lib/libgdiplus.dylib" />
</configuration>
EOF

cat <<EOF > mcs/class/lib/default/System.Windows.Forms.dll.config
<configuration>
        <dllmap dll="gdiplus" target="/Library/Frameworks/Mono.framework/Versions/${MONOVERSION}/lib/libgdiplus.dylib" />
        <dllmap dll="libX11" target="/usr/X11R6/lib/libX11.dylib" />
</configuration>
EOF

			 ./configure --prefix=$MONOPREFIX --with-preview=yes 
		else
			./configure --prefix=$MONOPREFIX 
		fi
	fi
	if [ ${MAKE} == "YES" ]; then
		make 
	fi
	if [ ${INSTALL} == "YES" ]; then
		make install
	fi
}

#Function builds are the various packages included in the
#Mono.framework.
packages() 
{


#pkgconfig
#################################################
NAME=pkgconfig
VERSION=0.15.0
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://www.freedesktop.org/software/pkgconfig/releases/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"
#################################################

#gettext
#################################################
NAME=gettext
VERSION=0.14.1
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://ftp.gnu.org/pub/gnu/gettext/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"
#################################################

#glib
#################################################
NAME=glib
VERSION=2.6.3
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=ftp://ftp.gtk.org/pub/gtk/v2.6/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"
#################################################

#mono
#################################################
NAME=mono
VERSION=${MONOVERSION}
DISTNAME=${NAME}-${MONOVERSION}.tar.gz
#URL=http://www.go-mono.com/archive/${MONOVERSION}/${DISTNAME}
URL=http://primates.ximian.com/~bmaurer/sources/mono-1.1/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"

#################################################


#JPEG
#################################################
PATCHDIR=${MONOBUILDFILES}/libgdiplus/jpeg/files
NAME=jpeg
VERSION=6b 
DISTNAME=${NAME}src.v${VERSION}.tar.gz
URL=ftp://ftp.uu.net/graphics/jpeg/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

fetch ${WORKSRCDIR} ${URL} ${DISTNAME}

cd ${WORKSRCDIR}
if [ ${CLEAN} == "YES" ]; then
	make clean
fi
if [ ${CONFIGURE} == "YES" ]; then
    patch config.guess ${PATCHDIR}/patch-config.guess
    patch config.sub ${PATCHDIR}/patch-config.sub
    patch ltmain.sh ${PATCHDIR}/patch-ltmain.sh
    patch ltconfig ${PATCHDIR}/patch-ltconfig

    sed -e 's/(prefix)\/man/(prefix)\/share\/man/g' makefile.cfg > makefile.cfg.patched
    mv makefile.cfg.patched makefile.cfg

    ./configure --enable-shared --enable-static --prefix=${MONOPREFIX}  
fi
if [ ${MAKE} == "YES" ]; then
	make 
fi
if [ ${INSTALL} == "YES" ]; then
	make install
fi

################################
NAME=tiff
VERSION=3.7.1
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=ftp://ftp.freebsd.org/pub/FreeBSD/ports/distfiles/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
cd ${WORKSRCDIR}

if [ ${CLEAN} == "YES" ]; then
	make clean
fi
if [ ${CONFIGURE} == "YES" ]; then
    ./configure --prefix=${MONOPREFIX} --mandir=${MONOPREFIX}/share/man \
	--with-jpeg-include-dir=${MONOPREFIX}/include \
	--with-jpeg-lib-dir=${MONOPREFIX}/lib  
fi
if [ ${MAKE} == "YES" ]; then
	make 
fi
if [ ${INSTALL} == "YES" ]; then
	make install
fi

###############################################
NAME=libpng
VERSION=1.2.8
DISTNAME=${NAME}-${VERSION}-config.tar.gz

URL=http://easynews.dl.sourceforge.net/sourceforge/libpng/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}-config

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"

###############################################
NAME=libungif
VERSION=4.1.3
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://easynews.dl.sourceforge.net/sourceforge/libungif/libungif-4.1.3.tar.gz
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}
build ${WORKSRCDIR} ${NAME}
echo "Done with ${NAME}"

###############################################
NAME=libgdiplus
VERSION=1.1.5
DISTNAME=${NAME}-${VERSION}.tar.gz
URL=http://www.go-mono.com/archive/${VERSION}/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${WORKSRCDIR} ${URL} ${DISTNAME}

cd ${WORKSRCDIR}
if [ ${CLEAN} == "YES" ]; then
	make clean
fi
if [ ${CONFIGURE} == "YES" ]; then
	./configure --prefix=${MONOPREFIX} --with-libjpeg --includedir=${MONOPREFIX}/include  
fi
if [ ${MAKE} == "YES" ]; then
	make 
fi
if [ ${INSTALL} == "YES" ]; then
	make install
fi

#cocoa#
#################################################
#PATCHDIR=${MONOBUILDFILES}/libgdiplus/jpeg/files
#http://www.go-mono.com/archive/1.1.4/cocoa-sharp-0.2.tgz
NAME=cocoa-sharp
VERSION=1.1.4 #Original Mono version, not cocoa# version
DISTNAME=${NAME}-0.2.tgz
URL=http://www.go-mono.com/archive/${VERSION}/${DISTNAME}
WORKSRCDIR=${NAME}-${VERSION}

echo "Building ${NAME}"
fetch ${NAME} ${URL} ${DISTNAME}

# hack autogen looks for the current link so it must exist.
ln -sf ${FRAMEWORKPREFIX}/Versions/${MONOVERSION} ${FRAMEWORKPREFIX}/Versions/Current

cd ${NAME}
if [ ${CLEAN} == "YES" ]; then
	make clean
fi
if [ ${CONFIGURE} == "YES" ]; then
	./autogen.sh --prefix=${MONOPREFIX} --with-preview=yes
fi
if [ ${MAKE} == "YES" ]; then
	make 
fi
if [ ${INSTALL} == "YES" ]; then
	make install
fi

echo "Done with ${NAME}"

#################################################

}


###############################################
#create plist files that are needed by the Installer.

plists() 
{
if [ ! -d ${PLISTS} ]; then
	mkdir -p ${PLISTS}
fi

if [ ! -d ${RESOURCES} ]; then
    mkdir -p ${RESOURCES}
fi


cat <<EOF > ${PLISTS}/Info.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleGetInfoString</key>
	<string>${MONOVERSION}</string>
	<key>CFBundleIdentifier</key>
	<string>com.ximian.mono</string>
	<key>CFBundleName</key>
	<string>Mono.framework</string>
	<key>CFBundleShortVersionString</key>
	<string>${MONOVERSION}</string>
	<key>IFMajorVersion</key>
	<integer>0</integer>
	<key>IFMinorVersion</key>
	<integer>0</integer>
	<key>IFPkgFlagAllowBackRev</key>
	<false/>
	<key>IFPkgFlagAuthorizationAction</key>
	<string>AdminAuthorization</string>
	<key>IFPkgFlagDefaultLocation</key>
	<string>/</string>
	<key>IFPkgFlagInstallFat</key>
	<false/>
	<key>IFPkgFlagIsRequired</key>
	<false/>
	<key>IFPkgFlagRelocatable</key>
	<false/>
	<key>IFPkgFlagRestartAction</key>
	<string>NoRestart</string>
	<key>IFPkgFlagRootVolumeOnly</key>
	<true/>
	<key>IFPkgFlagUpdateInstalledLanguages</key>
	<false/>
	<key>IFPkgFormatVersion</key>
	<real>0.10000000149011612</real>
</dict>
</plist>
EOF

cat <<EOF > ${PLISTS}/version.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>BuildVersion</key>
	<string>${MONOVERSION}</string>
	<key>CFBundleShortVersionString</key>
	<string>${MONOVERSION}</string>
	<key>CFBundleVersion</key>
	<string>${MONOVERSION}</string>
	<key>ProjectName</key>
	<string>Mono</string>
	<key>SourceVersion</key>
	<string>${MONOVERSION}</string>
</dict>
</plist>
EOF

cat <<EOF > ${PLISTS}/Description.plist 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">


if [ ! -d ${FRAMEWORKPREFIX}/Versions/Current/Resoures ]; then
	mkdir -p ${FRAMEWORKPREFIX}/Versions/Current/Resources
fi

cp ${PLISTS}/*.plist ${FRAMEWORKPREFIX}/Versions/Current/Resources
cd ${FRAMEWORKPREFIX}
ln -sf ${FRAMEWORKPREFIX}/Versions/Current/Resources Resources
EOF
}

#####################################################
#Create the RTF files needed by the installer
#Should now be completly dynamic so versions will be correct
rtfs()
{
if [ ! -d ${RESOURCES} ]; then
    mkdir -p ${RESOURCES}
fi

cp ${PLISTS}/version.plist ${RESOURCES}/

cat <<EOF > ${RESOURCES}/License.rtf
{\rtf1\mac\ansicpg10000\cocoartf102
{\fonttbl\f0\fswiss\fcharset77 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww9000\viewh9000\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\ql\qnatural

\f0\fs24 \cf0 The software included in the package is licensed under several different agreements.\\
\\
MIT License:\\
\\
http://www.opensource.org/licenses/mit-license.php\\
\\
LGPL:\\
\\
http://www.opensource.org/licenses/lgpl-license.php\\
\\
GPL:\\
\\
http://www.opensource.org/licenses/gpl-license.php}\\
}
EOF

cat <<EOF > ${RESOURCES}/ReadMe.rtf
{\rtf1\mac\ansicpg10000\cocoartf102
{\fonttbl\f0\fswiss\fcharset77 Helvetica;\f1\fswiss\fcharset77 Helvetica-Bold;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww15940\viewh15760\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\ql\qnatural

\f0\fs24 \cf0 This README is for
\f1\b  Mono.framework ${MONOVERSION}
\f0\b0 .\\
\\
This is a repackaging of Mono environment from http://www.mono-project.com/about/index.html.  The idea of this repackaging is to provide a native Mac OS X framework for doing Mono development.\\
\\
This package installs Mono and all of its dependencies inside of /Library/Frameworks/Mono.framework.  This behavior is likely to change with a future release so that depencancies will get their own frameworks.\\
\\
What gets installed inside Mono.framework?\\
\\
        pkgconfig-0.15.0\\
        gettext-0.14.1\\
        glib-2.6.3\\
        mono-${MONOVERSION}\\
        cocoa#-0.2\\
\\
Included in this version of the Mono.framework is Cocoa#.  Cocoa# is an API bridge that allows Mono developers to call Cocoa APIs while using Mono and C#.  A Cocoa# wiki is available at http://www.lormyr.com/cocoaSharp.\\
\\
This uninstallMono.sh script is in the Resources directory of MonoFramework.pkg.\\
\\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\ql\qnatural
\cf0 If you'd like to access the mono manpages you'll have to add /Library/Framework/Mono/Versions/Current/man to your manpath\\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\ql\qnatural
\cf0 \\
During the postinstall phase of the installation, links to /usr/bin are created for binaries installed into the Commands directory.  This is done to prevent requiring modifications to the \$PATH environmental variable.  Yes, we know that this is not typical for *NIX, but this is Mac OS X. \\
\\
A simple uninstallMono.sh script is included in the disk image.  This is shell script that must be run as root, and it will remove the Mono.framework and the links in /usr/bin.\\
\\
This package was created by the Cocoa# team.  Major contributors to this team include (in alphabetical order): \\
\\
Adhamh Findlay\\
Urs Muff\\
Geoff Norton\\
Andy Satori\\
\\
Questions or problems related directly to the Mono.framework should be addressed to mono-osx@lists.ximian.com.\\
\\
Questions about Mono should be directed to an appropriate resource that can be found on http://www.mono-project.com/about. \\
}
EOF

cat <<EOF > ${RESOURCES}/Welcome.rtf
{\rtf1\mac\ansicpg10000\cocoartf102
{\fonttbl\f0\fnil\fcharset77 HelveticaNeue;\f1\fnil\fcharset77 HelveticaNeue-Bold;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww9000\viewh9000\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\ql\qnatural

\f0\fs36 \cf0 Welcome to 
\f1\b Mono.framework ${MONOVERSION}
\f0\b0  for OS X.\\
\\
\fs24 This version of Mono includes Cocoa#.  Please see the ReadMe for more details.\\
}
EOF


################################################
#Create the uninstall script
cat <<EOF > ${RESOURCES}/uninstallMono.sh
#!/bin/sh -x

#This script removes Mono from an OS X System.  It must be run as root

rm -r /Library/Frameworks/Mono.framework

rm -r /Library/Receipts/MonoFramework-${MONOVERSION}.pkg

cd /usr/bin
for i in \`ls -al | grep Mono | awk '{print \$9}'\`; do
    rm \${i}
done
EOF
chmod 755 ${RESOURCES}/uninstallMono.sh
################################################

################################################
#Create the postflight script that will create links
#once the installer is done.

cat <<EOF > ${RESOURCES}/postflight
#!/bin/sh -x
if [ -d /Library/Frameworks/Mono.framework/Commands ]; then
cd /Library/Frameworks/Mono.framework/Commands
for i in \`ls -al | grep -v .exe | awk '{print \$9}'\`; do 
    echo "\${i}"
    ln -sf \$PWD/\${i} /usr/bin/\${i}
done;
else 
    echo "/Library/Frameworks/Mono.framework/Commands does not exist"
    echo "Can not create links to /usr/bin."
fi
EOF
chmod 755 ${RESOURCES}/postflight
}

framework()
{
###############################################
#Create the framework links, so that this is an OS X framework
if [ ${INSTALL} == "YES" ]; then
	cd ${FRAMEWORKPREFIX}/Versions
	if [ -e "${FRAMEWORKPREFIX}/Versions/Current" ]; then
		rm -r Current
	fi
	
	ln -sf ${MONOVERSION} Current
	echo "Creating framework links"
	
	cd ${FRAMEWORKPREFIX}
	
	#if [ ! -d Resources ] ; then
	cd ${MONOPREFIX}
	mkdir Resources
	cp ${PLISTS}/version.plist Resources
	cp ${PLISTS}/Info.plist Resources
	cd ${FRAMEWORKPREFIX}
		
	if [ ! -e Versions/Current/Resources ]; then
		ln -sf Versions/Current/Resources Resources
	fi
	ln -sf Versions/Current/lib Libraries
	ln -sf Versions/Current/include Headers
	ln -sf Versions/Current/bin Commands
	
	
	if [ -e Versions/Current/lib/libmono.dylib ]; then
		ln -sf Libraries/libmono.dylib Mono
	else
		echo "/Library/Frameworks/Mono.framework/Libraries/libmono.dylib does not exist"
	fi
	
	for i in \
	  `ls -al ${MONOPREFIX}/bin | grep -v total | grep -v .exe | grep -vw "\." |awk '{print $9}'`; do
	  echo ${i}
	  ln -sf ${MONOPREFIX}/bin/${i} /usr/bin/${i}
	done
fi
}



################################################
#Create the pkg and dmg that will get posted.
dmg() {
if [ ! -d ${BUILDROOT}/PKGROOT ]; then
    mkdir -p ${BUILDROOT}/PKGROOT
fi

if [ ! -d ${BUILDROOT}/pkg ]; then
    mkdir -p ${BUILDROOT}/pkg
fi

PACKAGEMAKER=/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker
ditto /Library/Frameworks/Mono.framework /Users/Shared/MonoBuild/PKGROOT/Library/Frameworks/Mono.framework

${PACKAGEMAKER} -build -p ${BUILDROOT}/pkg/MonoFramework-${MONOVERSION}.pkg -f ${BUILDROOT}/PKGROOT -r ${RESOURCES} -i ${PLISTS}/Info.plist -d ${PLISTS}/Description.plist 

/usr/bin/hdiutil create -ov -srcfolder ${BUILDROOT}/pkg/MonoFramework-${MONOVERSION}.pkg -volname MonoFramework-${MONOVERSION} ${BUILDROOT}/pkg/MonoFramework-${MONOVERSION}.dmg
}

################################################
#Actualy calls the script funcations
packages
plists
rtfs
framework
dmg