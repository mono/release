#functions to build mono.

createFramework()
{	
	echo ""
	echo "=================================================="
	echo "Creating framework work $BASEPREFIX/$FRAMEWORKNAME"
	echo "=================================================="
	echo ""
	
	FRAMEWORKNAME=$1
	cd $BASEPREFIX/$FRAMEWORKNAME/Versions
	if [ -e "$BASEPREFIX/$FRAMEWORKNAME/Versions/Current" ]; then
		rm -r Current
	fi
	
	ln -sf $2 Current
	echo "Creating framework links"
	cd $BASEPREFIX/$1

        ln -sf Versions/Current/Resources Resources
	ln -sf Versions/Current/lib Libraries
	ln -sf Versions/Current/include Headers
	ln -sf Versions/Current/bin Commands
}

createConfigFiles()
{
    #Create gacutil config files specific to OS X
    cat <<EOF > ${BUILDROOT}/Dependancies/mono-${MONOVERSION}/mcs/class/lib/default/System.Drawing.dll.config
<configuration>
        <dllmap dll="gdiplus.dll" target="/Library/Frameworks/Mono.framework/Versions/${MONOVERSION}/lib/libgdiplus.dylib" />
</configuration>

EOF

    cat <<EOF > ${BUILDROOT}/Dependancies/mono-${MONOVERSION}/mcs/class/lib/default/System.Windows.Forms.dll.config
<configuration>
        <dllmap dll="gdiplus" target="/Library/Frameworks/Mono.framework/Versions/${MONOVERSION}/lib/libgdiplus.dylib" />
        <dllmap dll="libX11" target="/usr/X11R6/lib/libX11.dylib" />
</configuration>

EOF
}

build()
{
	#buildDepNew FRAMEWORKNAME FRAMEWORKVERSION URL TARBALL DIR
	#FRAMEWORKNAME = PkgConfig.Framework | Gnome.framework/Framewoks/Glib2.framework
	cd $BUILDROOT/Dependancies
	#This is used to build the prefix for each dep.
	FRAMEWORKNAME=$1
	#MONOVERSION=$2
	URL=$2
	DEPNAME=$3
	TARBALL=$4
	DIR=$5
	PREFIX="$BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION"
	
	echo ""
	echo "=================================================="
	echo "Building $DEPNAME"
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
	
		
		if [ ! -d $PREFIX/lib ]; then
			echo "Creating $DEPNAME Directories"
			mkdir -p $PREFIX/lib
            mkdir -p $PREFIX/man
			mkdir -p $PREFIX/bin
        fi
		
		if [ $DIR = "icu" ]; then
			echo foo
			icuSpecificBuild $PREFIX $URL $TARBALL
		else
			if [ ! -d $BUILDROOT/Dependancies/$DIR ]; then
				echo "Downloading $DIR"
				curl -L --max-redirs 5 -s -O $URL
				gnutar xzf $TARBALL
				CLEAN=NO
			fi
			if [ $REMOVE == "YES" ]; then rm $TARBALL; fi
			
			cd $DIR
			#echo "Building $FRAMEWORKNAME"
			#CLEAN must be YES if the --prefix has changed
			if [ $CLEAN == "YES" ]; then 
				echo ""
				echo "=================================================="
				echo "Cleaning $TARBALL"
				echo "=================================================="
				echo ""
				if [ -e ./config.log ]; then
				    make clean
				fi
			fi
			if [ $CONFIGURE == "YES" ]; then
			    #echo "Configuring $DIR"
				echo ""
				echo "=================================================="
				echo "Configuring $DIR"
				echo "=================================================="
				echo ""
			    #exit
			    if [ $DIR == mono-${MONOVERSION} ]; then
			    	./configure --quiet --prefix=$PREFIX --with-preview=yes
			    	make
				if [ ${SVN} == NO ];then
				    createConfigFiles
				fi
    			    else
    			    	./configure --quiet --prefix=$PREFIX
			    fi
			    
			fi			
			make install
		fi
		cd $BUILDROOT/Dependancies	
	#fi
	
	echo ""
	echo "=================================================="
	echo "built $DEPNAME"
	echo "=================================================="
	echo ""

}

svnbuild() {
    clear
    
    export PREFIX=/Library/Frameworks/Mono.framework/Versions/Current
    export NEW_PREFIX=/Library/Frameworks/Mono.framework/Versions/nightly

    export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Library/pkgconfig
    export PATH=${PREFIX}/bin:/usr/X11R6/bin:$PATH
        export ACLOCAL_FLAGS="-I /Library/Frameworks/Mono.framework/Versions/Current/share/aclocal/"
        export C_INCLUDE_PATH=${C_INCLUDE_PATH}:${PREFIX}/include
        export LDFLAGS="-L$PREFIX/lib $LDFLAGS"
        export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/usr/X11R6/lib:${PREFIX}/lib

    cd ${SVNDIR}
    ./autogen.sh --prefix=${NEW_PREFIX}
    make
    make install
}
