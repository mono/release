BUILDROOT="/Users/Shared/MonoBuild"
MONOURL="http://www.go-mono.com/archive/1.0.1/mono-1.0.1.tar.gz"
BASEPREFIX="/Library/Frameworks"


createFramework()
{	
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
		curl -L -Z 5 -s -O $2 $3
		gnutar xzf $4
	fi
	if [ $REMOVE == "YES" ]; then rm $3; fi

    cd icu/source
	if [ ! -f ./Makefile ]; then
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
	#build FRAMEWORKNAME FRAMEWORKVERSION URL TARBALL DIR
	#FRAMEWORKNAME = PkgConfig.Framework | Gnome.framework/Framewoks/Glib2.framework
	cd $BUILDROOT/Dependancies
	FRAMEWORKNAME=$1
	FRAMEWORKVERSION=$2
	URL=$3
	TARBALL=$4
	DIR=$5
	PREFIX="$BASEPREFIX/$FRAMEWORKNAME/Versions/$FRAMEWORKVERSION"
	#sets the build env.  
	export PATH=$PREFIX/bin:/usr/X11R6/bin:$PATH
	export ACLOCAL_FLAGS="-I $PREFIX/share/aclocal/"
	export C_INCLUDE_PATH=$C_INCLUDE_PATH:$PREFIX/include
	export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
	export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/usr/X11R6/lib:$PREFIX/lib
	export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:$PREFIX/lib/pkgconfig

	# Check to see if $FRAMEWORKNAME is present, needs to be dled, and/or installed
	if [ ! -d "$BASEPREFIX/$FRAMEWORKNAME/Versions/$FRAMEWORKVERSION" ] || [ $FRAMEWORKNAME = "Gnome.framework/Frameworks/Gnome-icon-theme.framework" ] || [ $FRAMEWORKNAME = "Mono.framework" ]; then
	    
	echo ""
        echo ==================================================================================
        echo "Building $BASEPREFIX/$FRAMEWORKNAME/Versions/$FRAMEWORKVERSION"
        echo ==================================================================================        
	echo ""

	echo "Creating $BASEPREFIX/$FRAMEWORKNAME"
		
		if [ ! $FRAMEWORKNAME = "Gnome.framework/Frameworks/Gnome-icon-theme.framework" ]; then
			mkdir -p $PREFIX
			mkdir -p $PREFIX/bin
			mkdir -p $PREFIX/lib		
			mkdir -p $PREFIX/include
			mkdir -p $PREFIX/share
			mkdir -p $PREFIX/include		
			mkdir -p $PREFIX/man/man1
		fi

		echo "Creating Framework"

		if [ $PACKAGE == "NO" ]; then
		    createFramework $FRAMEWORKNAME $FRAMEWORKVERSION
		    cd $BUILDROOT/Dependancies
		fi


		if [ $FRAMEWORKNAME = "Icu.framework" ]; then
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
				echo""
				echo "Configuring $FRAMEWORKNAME"
				echo""
				case "$FRAMEWORKNAME" in 
 					"Gnome.framework/Frameworks/Png.framework") 
					        cp scripts/makefile.darwin Makefile;
						perl -p -i.bak -e 's/prefix=\/usr\/local/prefix=\/Library\/Frameworks\/Gnome.framework\/Frameworks\/Png.Framework\/Versions\/Current/g' Makefile;
						;; 
 					"Gnome.framework/Frameworks/Gtk2+.framework") 
						./configure --prefix=$PREFIX --without-libjpeg; 
						;; 
	 				"Gnome.framework/Frameworks/Popt.framework") 
						export BEFORE_POPT_LDFLAGS=$LDFLAGS
						export LDFLAGS=""
						./configure --prefix=$PREFIX;
						;; 
	 				"Gnome.framework/Frameworks/ORBit2.framework") 
						export LDFLAGS=$BEFORE_POPT_LDFLAGS
						export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
						export CFLAGS="$CFLAGS -DBIND_8_COMPAT=1"
						./configure --prefix=$PREFIX; 
						;; 
 					"Gnome.framework/Frameworks/XML-Parser.framework") 
						perl Makefile.PL EXPATLIBPATH=/usr/X11R6/lib EXPATINCPATH=/usr/X11R6/include; 
						;; 
 					"Gnome.framework/Frameworks/Gnome-vfs.framework") 

 						for i in `ls -al ${SHPATH}/patch/gnome-vfs | grep diff | awk '{print $9}'` ;do
 							cp ${SHPATH}/patch/gnome-vfs/${i} ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1
 						done
						#cp "${SHPATH}/patch/gnome-vfs/*.diff" /Users/Shared/MonoBuild/Dependancies/gnome-vfs-2.6.1.1
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_bzip2-method.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_extfs-method.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_file-metod.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_gnome-vfs-cdrom.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_gnome-vfs-utils.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_pty-open.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/gnome-vfs-2.6.1.1 < patch_sftp-method.diff
						export CFLAGS="-no-cpp-precomp -flat_namespace -undefined suppress"
						export CPPFLAGS="-L$PREFIX/lib -I$PREFIX/include"
						./configure --prefix=$PREFIX; 
						;; 
 					"Gnome.framework/Frameworks/Libgnome.framework") 
						cp $SHPATH/patch/libgnome/*.diff ${BUILDROOT}/Dependancies/libgnome-2.4.0
						patch -p0 -d ${BUILDROOT}/Dependancies/libgnome-2.4.0 < patch_gnome-score.diff
						patch -p0 -d ${BUILDROOT}/Dependancies/libgnome-2.4.0 < patch_gnome-util.diff
						export CFLAGS="-flat_namespace -undefined suppress"
						export CPPFLAGS="-L$PREFIX/lib -I$PREFIX/include"
						./configure --prefix=$PREFIX; 
						;; 
					"Gnome.framework/Frameworks/XML-Parser.framework") 
						perl Makefile.PL EXPATLIBPATH=/usr/X11R6/lib EXPATINCPATH=/usr/X11R6/include; 
						;; 
					"Cups.framework") 
						export BEFORE_CUPS_LDFLAGS=$LDFLAGS
						export LDFLAGS=""
						./configure --prefix=$PREFIX; 
						;; 
 					"Gnome.framework/Frameworks/Libgnomeprint.framework") 
						export LDFLAGS=$BEFORE_CUPS_LDFLAGS
						export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
						./configure --disable-font-install --prefix=$PREFIX; 
						;; 
 					"Gnome.framework/Frameworks/Hicolor-icon-theme.framework") 
						./configure --prefix=/Library/Frameworks/Gnome.framework/Frameworks/Gnome-icon-theme.framework/Versions/1.2.3; 
						;; 
					"Gnome.framework/Frameworks/Vte.framework") 
						echo "replacing dumpkeys.c"	
						rm ${BUILDROOT}/Dependancies/vte-0.11.10/src/dumpkeys.c
						cp -f $SHPATH/patch/vte/*.c ${BUILDROOT}/Dependancies/vte-0.11.10/src/dumpkeys.c
						#patch -p0 -d ${BUILDROOT}/Dependancies/vte-0.11.10 < patch_dumpkeys.diff
						export CFLAGS="-fstrict-aliasing -funroll-loops"
						export CPPFLAGS="-L/usr/X11R6/lib -I/usr/X11R6/include/ -I/usr/X11R6/include/freetype2/":$CPPFLAGS
						./configure --with-ft-prefix=/usr/X11R6/ --disable-freetypetest --with-ft-include-prefix=/usr/X11R6/include/freetype2/ --prefix=$PREFIX; 
						;; 
	 				"Gnome.framework/Frameworks/Gtkhtml.framework") 
						cd ${BUILDROOT}/Dependancies/gtkhtml-3.1.12/components/html-editor
						mv spell.h spellslikahorse.h
						sed -e s/spell.h/spellslikahorse.h/g Makefile.in > Makefile.in2
						rm Makefile.in
						mv Makefile.in2 Makefile.in
						sed -e s/spell.h/spellslikahorse.h/g spell.c > spell.c2
						rm spell.c
						mv spell.c2 spell.c
						sed -e s/spellslikahorse.has_control/spell_has_control/g spell.c > spell.c2
						rm spell.c
						mv spell.c2 spell.c
						sed -e s/spell.h/spellslikahorse.h/g control-data.c > control-data.c2
						rm control-data.c
						mv control-data.c2 control-data.c
						sed -e s/spell.h/spellslikahorse.h/g control-data.h > control-data.h2
						rm control-data.h
						mv control-data.h2 control-data.h
						sed -e s/spell.h/spellslikahorse.h/g editor-control-factory.c > editor-control-factory.c2
						rm editor-control-factory.c
						mv editor-control-factory.c2 editor-control-factory.c
						sed -e s/spell.h/spellslikahorse.h/g engine.c > engine.c2
						rm engine.c
						mv engine.c2 engine.c
						sed -e s/spell.h/spellslikahorse.h/g gnome-gtkhtml-editor.c > gnome-gtkhtml-editor.c2
						rm gnome-gtkhtml-editor.c
						mv gnome-gtkhtml-editor.c2 gnome-gtkhtml-editor.c
						sed -e s/spell.h/spellslikahorse.h/g menubar.c > menubar.c2
						rm menubar.c
						mv menubar.c2 menubar.c
						sed -e s/spellslikahorse.has_control/spell_has_control/g menubar.c > menubar.c2
						rm menubar.c
						mv menubar.c2 menubar.c
						sed -e s/spell.h/spellslikahorse.h/g popup.c > popup.c2
						rm popup.c
						mv popup.c2 popup.c
						cd ../..
						export CFLAGS="-no-cpp-precomp -flat_namespace -undefined suppress"
						./configure --prefix=$PREFIX; 
						;; 
					"GTKSharp.framework")
						./configure --prefix=/Library/Frameworks/Mono.framework/Versions/Current;
						;;
					"Mono.framework")
						#echo "Mono foo here";
                                                ./configure --prefix=$PREFIX;
						;;

					*) 
						./configure --prefix=$PREFIX; 
						;; 
				esac

			#clear
			if [ "$FRAMEWORKNAME" == "GTKSharp.framework" ] ;then 
                            #work around    
			    cd art
                            make install
			    gacutil -i art-sharp.dll
 
			    make install
			    for i in `find . -name "*.dll"`; do gacutil -i ${i}; done
			
			else
				make
				make install
			fi

			fi
			#if we aren't going to create a package then we need to 
			#go ahead and set this up as a framework.
			#if [ $PACKAGE == "NO" ]; then
				#createFramework $FRAMEWORKNAME $FRAMEWORKVERSION
			#fi
			cd $BUILDROOT/Dependancies	
		fi
	fi
}


createPackage()
{
	FRAMEWORKNAME=$1
	VERSION=$2
	IDENTIFIER=$3
	DESCRIPTION=$4
	RFILES="${CVS}/release/macosx/resources"
	TIGER="/Volumes/tiger"

	if [ ! -d $TIGER ]; then
		echo "This script uses the PackageMaker from Tiger because the"
		echo "The Panther version always exits with a 2"
		echo "If you have Tiger installed the you need to modifiy"
		echo "the TIGER variable in this script"
		TIGER=""
	fi

	PM="$TIGER/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker"
	
	if [ ! -d ${BUILDROOT}/PKGROOT/Library/Frameworks ]; then
		mkdir -p ${BUILDROOT}/PKGROOT/Library/Frameworks
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
