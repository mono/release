#!/bin/sh -x

# This is the build script for Cocoa Sharp.

BUILDROOT="/Users/Shared/CSBuild"
BASEPREFIX="/Applications"
CSPATH=""
IPATH=""
MONODOC="YES"
TESTS="YES"
RFILES="/usr/local/mono/release/osx/cocoasharp/"

usage()
{
    cat <<EOF
    buildCocoaSharp.sh usage is as follows
    -p path to where Cocoa# was checked out, required not including cocoa-sharp directory
    -i prefix to Cocoa# install location, required
    -h this message
EOF
exit 2
}

createPackage()
{
	FRAMEWORKNAME=$1
	VERSION=$2
	IDENTIFIER=$3
	DESCRIPTION=$4
	RFILES="/usr/local/mono/release/macosx/cocoasharp/resources"
	TIGER="/Volumes/tiger"
	if [ ! -d $TIGER ]; then
		echo "This script uses the PackageMaker from Tiger because the"
		echo "The Panther version always exits with a 2"
		echo "If you have Tiger installed the you need to modifiy"
		echo "the TIGER variable in this script"
		exit 2
	fi
	
	PM="$TIGER/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"
	
	if [ ! -d ${BUILDROOT}/Packages ]; then
		mkdir -p ${BUILDROOT}/Packages
	fi

        if [ ! -d ${BUILDROOT}/finished ]; then
                mkdir -p ${BUILDROOT}/finished
        fi

	if [ ! -d ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources ]; then
		mkdir -p ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources
	fi
	
	cp -r ${RFILES}/* ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources
	
cat <<EOF > ${BUILDROOT}/PKGRES/Info.plist
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

cat <<EOF > ${BUILDROOT}/PKGRES/Description.plist 
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
	<dict>
			<key>IFPkgDescriptionDeleteWarning</key>
			<string></string>
			<key>IFPkgDescriptionDescription</key>
			<string>${DESCRIPTION}</string>
			<key>IFPkgDescriptionTitle</key>
			<string>${FRAMEWORKNAME} Framework</string>
			<key>IFPkgDescriptionVersion</key>
			<string>${VERSION}</string>
	</dict>
	</plist>
EOF

# PackageMaker will package everything in the PKGROOT directory.  We really don't want
# that because then we would be creating packages that have duplicate information thus 
# defeating the purpose of have individual packages.  So once the package has been created
# we move the framework to the finished directory and test for its location there.
	if [ ! -d ${BUILDROOT}/finish/${FRAMEWORKNAME}-${VERSION}.pkg ]; then

    	${PM} -build -p ${BUILDROOT}/Packages/${FRAMEWORKNAME}-${VERSION}.pkg -f ${BUILDROOT}/PKGROOT -r ${BUILDROOT}/PKGRES/Resources -i ${BUILDROOT}/PKGRES/Info.plist -d ${BUILDROOT}/PKGRES/Description.plist
	if [ ! -d ${BUILDROOT}/finished ]; then
	    mkdir -p ${BUILDROOT}/finished
	fi
	mv ${BUILDROOT}/Packages/${FRAMEWORKNAME}-${VERSION}.pkg ${BUILDROOT}/finished
	fi

}


if [ -z $1 ]; then
    usage
else
while getopts op:i: option
do
  case "$option"
      in
      p) CSPATH="${OPTARG}/cocoa-sharp";;
      i) IPATH=$OPTARG;;
      h) usage;;
      esac
done
fi

if [ ! -d $IPATH/lib ]; then
    mkdir -p $IPATH/lib
fi
if [ ! -d $IPATH/bin ]; then
    mkdir -p $IPATH/bin
fi

cd $CSPATH
./autogen.sh --prefix=$IPATH
make
make install

# This will build monodoc that uses Cocoa-Sharp
echo "Building Monodoc for Cocoa#"
cd $CSPATH/monodoc
make install

# This will build a couple of example applications
echo "Building Cocoa# example/test applications"
cd $CSPATH/test
make

        if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks/Mono.framework/Versions/1.0 ]; then
            mkdir -p ${BUILDROOT}/PKGROOT/Library/Frameworks/Mono.framework/Versions/1.0
        fi

cp -r ${IPATH}/* ${BUILDROOT}/PKGROOT/Library/Frameworks/Mono.framework/Versions/1.0

if [ -e ${BUILDROOT}/finished/CocoaSharp.dmg ];then
    rm ${BUILDROOT}/finished/CocoaSharp.dmg
fi

createPackage CocoaSharp 0.1 com.ximian.mono "Cocoa-Sharp 0.1"

if [ ! -d {BUILDROOT}/finished/examples ]; then
    mkdir -p ${BUILDROOT}/finished/examples
fi

cd ${CSPATH}/test/nib

for i in *; do
    if [ ${i} != "CVS" ];then
	cp -r ${i} ${BUILDROOT}/finished/examples
    fi
done

hdiutil create -ov ${BUILDROOT}/CocoaSharp.dmg -srcfolder ${BUILDROOT}/finished/ -volname CocoaSharp


