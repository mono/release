#contains functions to create plist, rtf files, and then to package mono.

createPackage()
{
	FRAMEWORKNAME=$1
	VERSION=$2
	IDENTIFIER=$3
	DESCRIPTION=$4
	RFILES="mono/resources"
	#TIGER="/Volumes/Tiger"
	PM="/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"
	#if [ -d ${TIGER} ]; then
	  #  PM="${TIGER}/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"
	#fi

	if [ ! -e ${PM} ]; then
		echo "This script uses the PackageMaker from Tiger because the"
		echo "The Panther version always exits with a 2"
		echo "If you have Tiger installed the you need to modifiy"
		echo "the TIGER variable in this script"
		exit 2
	fi
	
	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks ]; then
		mkdir -p ${BUILDROOT}/PKGROOT/Library/Frameworks
	fi

	if [ ! -d ${BUILDROOT}/Packages ]; then
		mkdir -p ${BUILDROOT}/Packages
	fi

        if [ ! -d ${BUILDROOT}/finished ]; then
                mkdir -p ${BUILDROOT}/finished
        fi

	if [ ! -d ${BUILDROOT}/${FRAMWORKNAME}/resources ]; then
		mkdir -p ${BUILDROOT}/${FRAMWORKNAME}/resources
	fi
	
	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework ]; then
		ditto -V /Library/Frameworks/${FRAMEWORKNAME}.framework ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/
	fi
	
# 	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources ]; then
# 		mkdir ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources
# 	fi
# 	ditto ${BUILDROOT}/plists/ ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources/

	if [ ! -d ${BUILDROOT}/plists ]; then
		mkdir -p ${BUILDROOT}/plists
	fi
	
	#EVIL HACK
	cd ${MONOBUILDFILES}
	for i in `ls ${RFILES}`; do
		if [ ! ${i} == "CVS" ]; then
			cp -R ${RFILES}/${i} ${BUILDROOT}/resources
		fi
	done
	
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
	<string>${VERSION}</string>
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
#Create the links in the framework to have it fit the normal Framework structure.
if [ -d /Library/Frameworks/Mono.framework ]; then
	cd /Library/Frameworks/Mono.framework
	if [ -e /Library/Frameworks/Mono.framework/Versions/Current ]; then
		rm -f /Library/Frameworks/Mono.framework/Versions/Current
	fi
	ln -sf ${MONOVERSION} Versions/Current
	ln -sf Versions/Current/lib Libraries
	ln -sf Versions/Current/include Headers
	ln -sf Versions/Current/bin Commands
	ln -sf Versions/Current/Resources Resources

        if [ ! -d /Library/Frameworks/Mono.framework/Versions/Current/Resources ]; then
            mkdir -p /Library/Frameworks/Mono.framework/Versions/Current/Resources
        fi
        #cp ../Info.plist /Library/Frameworks/Mono.framework/Versions/Current/Resources/
        #cp ./version.plist /Library/Frameworks/Mono.framework/Versions/Current/Resources/


else 
	echo "/Library/Frameworks/Mono.framework does not exist"
fi

if [ -d /Library/Frameworks/Mono.framework/Commands ]; then
cd /Library/Frameworks/Mono.framework/Commands
for i in \`ls -al | grep -v .exe | awk '{print \$9}'\`; do 
	echo "\${i}"
	ln -sf \$PWD/\${i} /usr/bin/\${i}
done;
else 
	echo "/Library/Frameworks/Mono.framework/Commands does not exist"
fi

if [ -e /Library/Frameworks/Mono.framework/Libraries/libmono.dylib ];then
	ln -sf /Library/Frameworks/Mono.framework/Libraries/libmono.dylib /Library/Frameworks/Mono.framework/Mono
else
	echo "/Library/Frameworks/Mono.framework/Libraries/libmono.dylib does not exist"
fi
EOF

	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources ]; then
		mkdir -p ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources
	fi
	cp ${BUILDROOT}/plists/Info.plist ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources/
	cp ${BUILDROOT}/resources/version.plist ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework/Versions/${VERSION}/Resources/

# PackageMaker will package everything in the PKGROOT directory.  We really don't want
# that because then we would be creating packages that have duplicate information thus 
# defeating the purpose of have individual packages.  So once the package has been created
# we move the framework to the finished directory and test for its location there.
	if [ ! -d ${BUILDROOT}/finished/${FRAMEWORKNAME}-${VERSION}.pkg ]; then
    	${PM} -build -p ${BUILDROOT}/Packages/${FRAMEWORKNAME}Framework-${VERSION}.pkg -f ${BUILDROOT}/PKGROOT -r ${BUILDROOT}/resources -i ${BUILDROOT}/plists/Info.plist -d ${BUILDROOT}/resources/Description.plist
	if [ ! -d ${BUILDROOT}/finished ]; then
	    mkdir -p ${BUILDROOT}/finished
	    mv ${BUILDROOT}/${FRAMEWORKNAME}-${VERSION}.pkg ${BUILDROOT}/finished
	fi
	fi
	cp -r ${RFILES}/uninstallMono.sh ${BUILDROOT}/Packages/${FRAMEWORKNAME}Framework-${VERSION}.pkg/Contents/Resources

}
