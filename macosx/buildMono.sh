#!/bin/sh -x

# Complete rewrite by Adhamh Findlay <mono@adhamh.com> 7-14-04
# now compiles gettext, pkgconfig, icu, glib, and mono into frameworks
# more extensible so that other projects can be built into frameworks as well.
# this script can't build from CVS because it uses curl to download releases
# possible improvements
#	add function to get source from cvs
#	add some real functionality to the cleanup function
#	improve the initial directory creation and add option to remove framework directories
#		that will force a rebuild of the frameworks

# this horrid little script updates a mono revision
# Author: Andy Satori <dru@satori-assoc.com>
# Modifications: kangaroo
# Changes June 10/2004
#  - Updated for beta3 0.96
# Changes June 2/2004
#  - Updated for beta2 0.95
#  - Updated to boehm.gc.a6
#  - Updated to glib-2.4.1

set -e 

BUILDROOT="/Users/Shared/MonoBuild"
MONOVERSION="1.0.1"
BASEPREFIX="/Library/Frameworks"
PREFIX=""
MONOURL="http://www.go-mono.com/archive/1.0.1/mono-1.0.1.tar.gz"
REMOVE="NO"
CLEAN="NO"
PACKAGE="NO"
CONFIGURE="NO"
PKGCONFIG="http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-0.15.0.tar.gz"
GETTEXT="http://ftp.gnu.org/pub/gnu/gettext/gettext-0.14.1.tar.gz"
GLIB="ftp://ftp.gtk.org/pub/gtk/v2.4/glib-2.4.1.tar.gz"
ICU="ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz"

usage()
{
echo "Proper usage is as follows"
cat <<EOF
	buildNew.sh
		-g remove gz files (default no)
		-m make clean (default no)
		-c run configure (default yes)
		-p create packages in $BUILDROOT/MonoBuild
		-h this message
EOF
}

cleanup()
{
	#Cleans up if the script is interupted.
	echo
	echo "Interupted cleaning"
}

creatDirs()
{

	if [ ! -d "$BUILDROOT/Dependancies" ]; then
		mkdir -p $BUILDROOT/Dependancies
	fi
	
}

createFramework()
{	
	echo ""
	echo "=================================================="
	echo "Creating framework work $BASEPREFIX/$FRAMEWORKNAME"
	echo "=================================================="
	echo ""
	
	cd $BASEPREFIX/$1/Versions
	if [ -e "$BASEPREFIX/$FRAMEWORKNAME/Versions/Current" ]; then
		rm Current
	fi
	
	ln -sf $2 Current
	echo "Creating framework links"
	cd $BASEPREFIX/$1
	if [ $FRAMEWORKNAME != "PkgConfig.framework" ]; then
		ln -sf Versions/Current/lib Libraries
		ln -sf Versions/Current/include Headers
	fi
	ln -sf Versions/Current/bin Commands
}

icuSpecificBuild()
{
    PREFIX=$1
    
	if [ ! -d $BUILDROOT/Dependancies/icu ]; then
		echo "Downloading icu-2.8"
		curl -L -Z 5 -s -O --disable-epsv ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz
		gnutar xzf $3
	fi
	if [ $REMOVE == "YES" ]; then rm $3; fi

    cd icu/source
	if [ ${CONFIGURE} == "YES" ]; then
	    echo "Configuring ICU"
	    exit
	    ./runConfigureICU MacOSX --with-data-packaging=library --prefix=$PREFIX --libdir=$PREFIX/lib/ 
	fi
	echo $PWD
	if [ $CLEAN == "YES" ]; then make clean; fi
    gnumake
    make install
    #make clean
    
    cd $PREFIX/lib
    
    # libicudata
    install_name_tool -id $PREFIX/lib/libicudata.dylib.28 libicudata.dylib.28.0
    
    # libicui18n
    install_name_tool -id $PREFIX/lib/libicui18n.dylib.28 libicui18n.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicui18n.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicui18n.dylib.28.0
    
    # libicuio
    install_name_tool -id $PREFIX/lib/libicuio.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicuio.dylib.28.0
    install_name_tool -change libicui18n.dylib.28 $PREFIX/lib/libicui18n.dylib.28 libicuio.dylib.28.0
    
    # libicule
    install_name_tool -id $PREFIX/lib/libicule.dylib.28 libicule.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicule.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicule.dylib.28.0

    # libiculx
    install_name_tool -id $PREFIX/lib/libiculx.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libiculx.dylib.28.0
    install_name_tool -change libicule.dylib.28 $PREFIX/lib/libicule.dylib.28 libiculx.dylib.28.0

    # libicutoolutil
    install_name_tool -id $PREFIX/lib/libicutoolutil.dylib.28 libicutoolutil.dylib.28.0
    install_name_tool -change libicuuc.dylib.28 $PREFIX/lib/libicuuc.dylib.28 libicutoolutil.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicutoolutil.dylib.28.0

    # libicuuc
    install_name_tool -id $PREFIX/lib/libicuuc.dylib.28 libicuuc.dylib.28.0
    install_name_tool -change libicudata.dylib.28 $PREFIX/lib/libicudata.dylib.28 libicuuc.dylib.28.0

}

build()
{
	#buildDepNew FRAMEWORKNAME FRAMEWORKVERSION URL TARBALL DIR
	#FRAMEWORKNAME = PkgConfig.Framework | Gnome.framework/Framewoks/Glib2.framework
	cd $BUILDROOT/Dependancies
	FRAMEWORKNAME=$1
	#MONOVERSION=$2
	URL=$2
	TARBALL=$4
	DIR=$5
	PREFIX="$BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION"
	
	echo ""
	echo "=================================================="
	echo "Building $BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION"
	echo "=================================================="
	echo ""

	#sets the build env.  
	export PATH=$PREFIX/bin:/usr/X11R6/bin:$PATH
	export ACLOCAL_FLAGS="-I $PREFIX/share/aclocal/"
	export C_INCLUDE_PATH=$C_INCLUDE_PATH:$PREFIX/include
	export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
	export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/X11R6/lib:$PREFIX/lib

	# Check to see if pkg-config is present, needs to be dled, and/or installed
	#if [ ! -d "$BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION" ]; then
	
		echo "Creating $BASEPREFIX/$FRAMEWORKNAME"
		
		mkdir -p $PREFIX/lib
                mkdir -p $PREFIX/man
                mkdir -p $PREFIX/bin
		
		if [ $DIR = "icu" ]; then
			icuSpecificBuild $PREFIX $URL $TARBALL
		else
			if [ ! -d $BUILDROOT/Dependancies/$DIR ]; then
				echo "Downloading $DIR"
				curl -L -Z 5 -s -O $URL
				gnutar xzf $TARBALL
			fi
			if [ $REMOVE == "YES" ]; then rm $TARBALL; fi
			
			cd $DIR
			echo "Building $FRAMEWORKNAME"
			#CLEAN must be YES if the --prefix has changed
			if [ $CLEAN == "YES" ]; then 
				make clean
			fi
			if [ $CONFIGURE == "YES" ]; then
			    echo "Configuring $DIR"
			    exit
			    ./configure --prefix=$PREFIX
			fi
			make
			make install
		fi
		cd $BUILDROOT/Dependancies	
	#fi
	
	echo ""
	echo "=================================================="
	echo "built $BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION"
	echo "=================================================="
	echo ""

}


createPackage()
{
	FRAMEWORKNAME=$1
	VERSION=$2
	IDENTIFIER=$3
	DESCRIPTION=$4
	RFILES="/usr/local/mono/release/macosx/resources"
	TIGER="/Volumes/Tiger"
	PM="$TIGER/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"

	if [ ! -d $TIGER ]; then
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

	if [ ! -d ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources ]; then
		mkdir -p ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources
	fi
	
	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks/${FRAMEWORKNAME}.framework ]; then
		cp -r /Library/Frameworks/${FRAMEWORKNAME}.framework ${BUILDROOT}/PKGROOT/Library/Frameworks
	fi
	
	#cp -r ${RFILES}/* ${BUILDROOT}/${FRAMWORKNAME}/PKGRES/Resources
	
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
	    mv ${BUILDROOT}/${FRAMEWORKNAME}-${VERSION}.pkg ${BUILDROOT}/finished
	fi
	fi
}

trap cleanup 2

#get the options passed in on the command line.  doing this instead
#of a case -because these are optional args.
while getopts hvpimcg option
	do
# 		if [ $option == "v" ]; then
# 			VERSION=$OPTARG	
# 		fi
# 		if [ $option == "p" ]; then
# 			PREFIX=$OPTARG	
# 		fi
# 		if [ $option == "i" ]; then
# 			DEPSDIR=$OPTARG	
# 		fi
 		if [ $option == "m" ]; then
 			CLEAN="YES"	
 		fi
		if [ $option == "c" ]; then
			CONFIGURE="YES"	
		fi
		if [ $option == "g" ]; then
			REMOVE="YES"	
		fi
		if [ $option == "h" ]; then
			usage
		fi
		if [ $option == "p" ]; then
			PACKAGE="YES"	
		fi
done

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/X11R6/lib/pkgconfig

creatDirs

#Build the /Library/Frameworks/PkgConfig.framework
build Mono.framework ${PKGCONFIG} pkgconfig pkgconfig-0.15.0.tar.gz pkgconfig-0.15.0

#Build the /Library/Frameworks/GetText.framework
build Mono.framework ${GETTEXT} gettext gettext-0.14.1.tar.gz gettext-0.14.1
	
#Build the /Library/Frameworks/Gnome.framework/Frameworks/Glib2.framework
#this is don to provide a means to add more Gnome code later

build Mono.framework ${GLIB} glib glib-2.4.1.tar.gz glib-2.4.1
#Build the /Library/Frameworks/Mono.framwork/Frameworks/Icu.framework
#icu is only used by mono so it should be placed inside the mono framework

build Mono.framework ${ICU} icu icu-2.8.tgz icu 

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/Library/Frameworks/Gnome.framework/Frameworks/Glib2.framework/Libraries/pkgconfig

build Mono.framework ${MONOURL} mono mono-1.0.1.tar.gz mono-1.0.1 

echo "build completed"

if [ $PACKAGE == "YES" ]; then
	echo "starting packaging"
	createPackage Mono ${VERSION} com.ximian.mono "Mono Framework ${VERSION}"
else
	#if we aren't going to create a package then we need to 
	#go ahead and set this up as a framework.
	createFramework $FRAMEWORKNAME $MONOVERSION
	for i in \
	  `ls -al | grep -v total | grep -v .exe | grep -vw "\." |awk '{print $9}'`; do
	  echo ${i}
	  ln -sf $PWD/${i} /usr/bin/${i}
	done
fi