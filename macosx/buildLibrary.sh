#functions to build mono.

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
    DEPNAME=$3
	if [ ! -d $BUILDROOT/Dependancies/icu ]; then
		echo "Downloading icu-2.8"
		curl -L -Z 5 -s -O --disable-epsv ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz
		gnutar xzf $3
	fi
	if [ $REMOVE == "YES" ]; then rm $3; fi

    cd icu/source
	if [ ${CONFIGURE} == "YES" ]; then
	    #echo "Configuring ICU"
	    #exit
		echo ""
		echo "=================================================="
		echo "Configuring $DEPNAME"
		echo "=================================================="
		echo ""
	    ./runConfigureICU MacOSX --with-data-packaging=library --quiet --prefix=$PREFIX --libdir=$PREFIX/lib/ 
   	gnumake
	fi
	echo $PWD
	if [ $CLEAN == "YES" ]; then 
		echo ""
		echo "=================================================="
		echo "Cleaning $DEPNAME"
		echo "=================================================="
		echo ""
		make clean
	fi
		echo ""
		echo "=================================================="
		echo "Building $DEPNAME"
		echo "=================================================="
		echo ""
    make install
    #make clean
    
    cd $PREFIX/lib
    
		echo ""
		echo "=================================================="
		echo "Installing $DEPNAME"
		echo "=================================================="
		echo ""
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
				curl -L -Z 5 -s -O $URL
				gnutar xzf $TARBALL
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
				make clean
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