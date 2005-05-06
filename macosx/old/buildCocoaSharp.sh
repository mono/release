#!/bin/sh -x


if [ $# != 1 ];then
	echo "You must specify the location of the Cocoa# source!"
	exit 2
fi

cd $1

export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Libraries/pkgconfig
export PATH=$PREFIX/bin:/Library/Frameworks/Mono.framework/Versions/Current/bin:$PATH

PREFIX=/Library/Frameworks/Mono.framework/Versions/Current
FRAMEWORKNAME="CocoaSharp"
VERSION="0.2"
DESCRIPTION="CocoaSharp ${VERSION}"
PM="/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"
DMGNAME=CocoaSharp-${VERSION}
BUILDROOT=/Users/Shared/CocoaSharpBuild
INSTALLPATH=/Library/Frameworks/Mono.framework/Versions/Current
PKGROOT=${BUILDROOT}/PKGROOT/private/tmp/cocoasharp
PKGPATH=${BUILDROOT}/PKGROOT/${PREFIX}
INSROOT="/private/tmp/cocoasharp"

./autogen.sh --prefix=${PREFIX} --with-preview=yes
make
make install

if [ ! -d ${BUILDROOT} ]; then
    mkdir -p ${BUILDROOT}
fi

 if [ ! -d ${PKGROOT} ]; then
     mkdir -p ${PKGROOT}
fi
# 
 if [ ! -d ${PKGROOT}/lib/mono/cocoa-sharp ]; then
     mkdir -p ${PKGROOT}/lib/mono/cocoa-sharp
 fi

if [ ! -d ${PKGROOT}/lib/pkgconfig ]; then
    mkdir -p ${PKGROOT}/lib/pkgconfig
fi

if [ ! -d ${PKGROOT}/bin ]; then
     mkdir ${PKGROOT}/bin
fi
# 
# if [ ! -d ${PKGPATH}/lib/mono/cocoa-sharp ]; then
#     mkdir -p ${PKGPATH}/lib/mono/cocoa-sharp
# fi
# 
# if [ ! -d ${PKGPATH}/pkgconfig ]; then
#     mkdir ${PKGPATH}/pkgconfig
# fi

if [ ! -d ${BUILDROOT}/plists ]; then
    mkdir -p ${BUILDROOT}/plists
fi

if [ ! -d ${BUILDROOT}/resources ]; then
    mkdir -p ${BUILDROOT}/resources
fi

if [ ! -d ${BUILDROOT}/Packages ]; then
    mkdir -p ${BUILDROOT}/Packages
fi

if [ ! -d ${BUILDROOT}/finished ]; then
                mkdir -p ${BUILDROOT}/finished
fi

cp ${INSTALLPATH}/lib/libCocoaSharpGlue.0.dylib ${PKGROOT}/lib/
cp ${INSTALLPATH}/lib/mono/cocoa-sharp/Apple.AppKit.dll ${PKGROOT}/lib/mono/cocoa-sharp/

cp ${INSTALLPATH}/lib/mono/cocoa-sharp/Apple.Foundation.dll ${PKGROOT}/lib/mono/cocoa-sharp/
cp ${INSTALLPATH}/lib/mono/cocoa-sharp/Apple.WebKit.dll ${PKGROOT}/lib/mono/cocoa-sharp/
cp ${INSTALLPATH}/lib/pkgconfig/cocoa-sharp.pc ${PKGROOT}/lib/pkgconfig/

cp ${1}/src/Apple.AppKit/Apple.AppKit.dll.config ${PKGROOT}/lib/mono/cocoa-sharp/
cp ${1}/src/Apple.Foundation/Apple.Foundation.dll.config ${PKGROOT}/lib/mono/cocoa-sharp/
cp ${1}/src/Apple.WebKit/Apple.WebKit.dll.config ${PKGROOT}/lib/mono/cocoa-sharp/

#cp ${INSTALLPATH}/bin/CocoaSharpLoader ${PKGROOT}/bin/

#createPackage Mono ${MONOVERSION} com.ximian.mono "Mono Framework ${MONOVERSION}"

echo ${INSROOT}


cat <<EOF > ${PKGROOT}/uninstallCocoaSharp.sh
#!/bin/sh -x
#uninstall cocoasharp

rm -r /Library/Frameworks/Mono.framework/Versions/Current/lib/libCocoaSharpGlue*
rm -r /Library/Frameworks/Mono.framework/Versions/Current/lib/mono/cocoa-sharp
#rm -r /Library/Frameworks/Mono.framework/Versions/Current/bin/CocoaSharpLoader
rm -r /Library/Frameworks/Mono.framework/Versions/nightly/lib/pkgconfig/cocoa-sharp.pc
rm -r /Library/Receipts/CocoaSharp0.2.pkg

/usr/bin/gacutil /u Apple.Foundation
/usr/bin/gacutil /u Apple.AppKit
/usr/bin/gacutil /u Apple.WebKit
EOF

cat <<EOF > ${BUILDROOT}/plists/Info.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
		<dict>
		<key>CFBundleGetInfoString</key>
		<string>${VERSION}</string>
		<key>CFBundleIdentifier</key>
		<string>${IDENTIFIER}</string>
		<key>CFBundleName</key>
		<string>${FRAMEWORKNAME}.framework</string>
		<key>CFBundleShortVersionString</key>
		<string>${VERSION}</string>
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

cat <<EOF > ${BUILDROOT}/resources/version.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>BuildVersion</key>
	<string>${VERSION}</string>
	<key>CFBundleShortVersionString</key>
	<string${VERSION}</string>
	<key>CFBundleVersion</key>
	<string>${VERSION}</string>
	<key>ProjectName</key>
	<string>${FRAMEWORKNAME}</string>
	<key>SourceVersion</key>
	<string>${VERSION}</string>
</dict>
</plist>
EOF

cat <<EOF > ${BUILDROOT}/resources/Description.plist 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
		<key>IFPkgDescriptionDescription</key>
		<string>${DESCRIPTION}</string>
		<key>IFPkgDescriptionTitle</key>
		<string>${FRAMEWORKNAME} Framework</string>
		<key>IFPkgDescriptionVersion</key>
		<string>${VERSION}</string>
</dict>
</plist>
EOF

cat <<EOF > ${BUILDROOT}/resources/postflight
#!/bin/sh -x
#this is to run gacutil and install the cocoa sharp files into gac.

if [ ! -d ${PREFIX}/lib/mono/cocoa-sharp ]; then
     mkdir ${PREFIX}/lib/mono/cocoa-sharp
fi

cp ${INSROOT}/lib/libCocoaSharpGlue.0.dylib ${PREFIX}/lib/
cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.AppKit.dll ${PREFIX}/lib/mono/cocoa-sharp/
cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.Foundation.dll ${PREFIX}/lib/mono/cocoa-sharp/
cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.WebKit.dll ${PREFIX}/lib/mono/cocoa-sharp/
cp ${INSROOT}/lib/pkgconfig/cocoa-sharp.pc ${PREFIX}/lib/pkgconfig

cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.AppKit.dll.config ${PREFIX}/lib/mono/cocoa-sharp/
cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.Foundation.dll.config ${PREFIX}/lib/mono/cocoa-sharp/
cp ${INSROOT}/lib/mono/cocoa-sharp/Apple.WebKit.dll.config ${PREFIX}/lib/mono/cocoa-sharp/ 

cd /Library/Frameworks/Mono.framework/Versions/Current/lib
ln -sf libCocoaSharpGlue.0.dylib libCocoaSharpGlue.0.0.0.dylib
ln -sf libCocoaSharpGlue.0.dylib libCocoaSharpGlue.dylib

cd /Library/Frameworks/Mono.framework/Versions/Current/lib/mono/cocoa-sharp/
 
/usr/bin/gacutil /i Apple.Foundation.dll /f /package cocoa-sharp /gacdir /Library/Frameworks/Mono.framework/Versions/Current/lib
/usr/bin/gacutil /i Apple.AppKit.dll /f /package cocoa-sharp /gacdir /Library/Frameworks/Mono.framework/Versions/Current/lib
/usr/bin/gacutil /i Apple.WebKit.dll /f /package cocoa-sharp /gacdir /Library/Frameworks/Mono.framework/Versions/Current/lib

cd /
#rm -r /tmp/cocoasharp
EOF



# PackageMaker will package everything in the PKGROOT directory.  We really don't want
# that because then we would be creating packages that have duplicate information thus 
# defeating the purpose of have individual packages.  So once the package has been created
# we move the framework to the finished directory and test for its location there.
	if [ ! -d ${BUILDROOT}/finished/${FRAMEWORKNAME}-${VERSION}.pkg ]; then
    	${PM} -build -p ${BUILDROOT}/Packages/${FRAMEWORKNAME}${VERSION}.pkg -f ${BUILDROOT}/PKGROOT -r ${BUILDROOT}/resources -i ${BUILDROOT}/plists/Info.plist -d ${BUILDROOT}/resources/Description.plist
# 	if [ ! -d ${BUILDROOT}/finished ]; then
# 	    mkdir -p ${BUILDROOT}/finished
# 	    mv ${BUILDROOT}/${FRAMEWORKNAME}-${VERSION}.pkg ${BUILDROOT}/finished
# 	fi
	fi
	cp ${PKGROOT}/uninstallCocoaSharp.sh ${BUILDROOT}/Packages/


#chmod 775 ${PKGROOT}/installCocoaSharp.sh
chmod 775 ${BUILDROOT}/Packages/uninstallCocoaSharp.sh
#chmod 775 ${BUILDROOT}/resources/postflight

hdiutil create -ov -srcfolder ${BUILDROOT}/Packages/ -volname CocoaSharp-${VERSION} ${BUILDROOT}/finished/CocoaSharp-${VERSION}