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
usage()
{
echo "Proper usage is as follows"
cat <<EOF
	buildMono.sh
                -v <mono version> specifies version of mono to build
                -s <svn directory> build from svn checked out sources
		-R remove gz files (default no)
		-C make clean (default no)
		-c run configure (default no)
		-p create packages in $BUILDROOT/MonoBuild
		-o when used with -p will only create packages will not build
                -g do not build libgdiplus
		-h this message
        example:
        buildMono.sh 1.1.3 -p
EOF
exit
}

if [ $# == 0 ]; then
    usage
fi

if [ $1 != "-v" ]; then
    echo "For safety sake, -v must be the first option"
    usage
fi

BUILDROOT="/Users/Shared/MonoBuild"
#MONOVERSION=$1
BASEPREFIX="/Library/Frameworks"
PREFIX=""
#MONOURL="http://www.go-mono.com/archive/$1/mono-$1.tar.gz"
BUILD="YES"	
REMOVE="NO"
CLEAN="NO"
PACKAGE="NO"
CONFIGURE="NO"
PKGCONFIG="http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-0.15.0.tar.gz"
GETTEXT="http://ftp.gnu.org/pub/gnu/gettext/gettext-0.14.1.tar.gz"
GLIB="ftp://ftp.gtk.org/pub/gtk/v2.4/glib-2.4.1.tar.gz"
ICU="ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz"
SVN="NO"
PACKAGEONLY="NO"
MONOBUILDFILES=${PWD}
#build libgdiplus?  default is yes
GDIPLUS="YES" 


#the buildLibrary file contains functions to build mono
. ./buildLibrary.sh
#the packageLibrary contains the fuctions to package mono and create any 
#needed resource files
. ./packageLibrary.sh

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

trap cleanup 2

#get the options passed in on the command line.  doing this instead
#of a case -because these are optional args.
while getopts hv:piCcRs:uoOg option
	do
		echo $option
 		if [ $option == "v" ]; then
 			MONOVERSION=$OPTARG	
			MONOURL="http://www.go-mono.com/archive/${MONOVERSION}/mono-${MONOVERSION}.tar.gz"
 		fi
# 		if [ $option == "p" ]; then
# 			PREFIX=$OPTARG	
# 		fi
# 		if [ $option == "i" ]; then
# 			DEPSDIR=$OPTARG	
# 		fi
 		if [ $option == "o" ]; then
 			BUILD="NO"	
 		fi
		if [ $option == "O" ]; then
		    PACKAGEONLY="YES"
		fi
 		if [ $option == "C" ]; then
 			CLEAN="YES"	
 		fi
		if [ $option == "c" ]; then
			CONFIGURE="YES"	
		fi
		if [ $option == "R" ]; then
			REMOVE="YES"	
		fi
		if [ $option == "h" ]; then
			usage
		fi
		if [ $option == "p" ]; then
			PACKAGE="YES"	
		fi
		if [ $option == "g" ]; then
		    GDIPLUS="NO"
		fi
		if [ $option == "s" ]; then
			if [ ! -d "/Library/Frameworks/Mono.framework/Versions/Current" ]; then
				echo "To do this you MUST have the current version of Mono.framework installed"
				echo "You can dl this from http://mono-project.com/downloads/"
				exit
			else
				SVN="YES"
				SVNDIR=$OPTARG
			fi
		fi

done

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/X11R6/lib/pkgconfig
export PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin

creatDirs

# if [ $SVN == "YES" ]; then
# 	#This will build mono from the mono ximain repository.
# 	#It bypasses building Mono's deps because you must already have then installed
# 	#in order to build mono.  The -s option doesn't work if you don't have a 
# 	#previous version of Mono.framework installed.
# 	
# 	echo "Getting Mono from CVS"
# 	export CVS_RSH=ssh
# 	export CVSROOT=${CVSUSER}@mono-cvs.ximian.com:/cvs/public
# 	cd `dirname ${CVSMONO}`
# 	cvs -z3 co mono
# 
# 	echo "Setting up build env"	
# 	export PREFIX=/Library/Frameworks/Mono.framework/Versions/Current
# 	export PKG_CONFIG_PATH=/Library/Frameworks/Mono.framework/Libraries/pkgconfig
# 	export PATH=$PREFIX/bin:/usr/X11R6/bin:$PATH
# 	export ACLOCAL_FLAGS="-I /Library/Frameworks/Mono.framework/Versions/Current/share/aclocal"
# 	MONOVERSION="CVS"
# 	
# 	echo "Building Mono"
# 	cd ${SVNDIR}
# 	./autogen.sh --prefix=/Library/Frameworks/Mono.framework/Versions/CVS
# 	make
# 	cd /Library/Frameworks/Mono.framework/Versions
# 	ln -sf ${MONOVERSION} Current
#fi 	
# else
	#This is the "normal" build used mainly to create a framework that can be used
	#to create a package that can be distributed.
	
	if [ ${BUILD} == "YES" ]; then
	   if [ ${PACKAGEONLY} == "NO" ]; then
		#Build PkgConfig
		if [ ! -f "/Library/Framework/Mono.framework/Version/${MONOVERSION}/bin/pkg-config" ];then 
			build Mono.framework ${PKGCONFIG} pkgconfig pkgconfig-0.15.0.tar.gz pkgconfig-0.15.0
		fi
		
		#Build the /Library/Frameworks/GetText.framework
		if [ ! -f "/Library/Framework/Mono.framework/Version/${MONOVERSION}/bin/gettext" ];then 
			build Mono.framework ${GETTEXT} gettext gettext-0.14.1.tar.gz gettext-0.14.1
		fi
		
		#Build the /Library/Frameworks/Gnome.framework/Frameworks/Glib2.framework
		#this is don to provide a means to add more Gnome code later
		if [ ! -d "/Library/Framework/Mono.framework/Version/${MONOVERSION}/lib/glib-2.0" ];then 
			build Mono.framework ${GLIB} glib glib-2.4.1.tar.gz glib-2.4.1
		fi
		
		#Build the /Library/Frameworks/Mono.framwork/Frameworks/Icu.framework
		#icu is only used by mono so it should be placed inside the mono framework
		if [ ! -d "/Library/Framework/Mono.framework/Version/${MONOVERSION}/lib/icu" ];then 
			build Mono.framework ${ICU} icu icu-2.8.tgz icu 
		fi
		if [ $SVN == "YES" ]; then
		    svnbuild Mono.framework
		else
		    build Mono.framework ${MONOURL} mono mono-${MONOVERSION}.tar.gz mono-${MONOVERSION}
		fi
		if [${GDIPLUS} == "YES" ];then
		    ./gdipBuild.sh
		fi
	   fi
   	fi 
#fi

echo "build completed"

if [ $PACKAGE == "YES" ]; then
	echo ""
	echo "=================================================="
	echo "Packaging $BASEPREFIX/$FRAMEWORKNAME/Versions/$MONOVERSION"
	echo "=================================================="
	echo ""
	createPackage Mono ${MONOVERSION} com.ximian.mono "Mono Framework ${MONOVERSION}"

	hdiutil create -ov -srcfolder ${BUILDROOT}/Packages/MonoFramework-${MONOVERSION}.pkg -volname MonoFramework-${MONOVERSION} ${BUILDROOT}/finished/MonoFramework-${MONOVERSION}
else
	#if we aren't going to create a package then we need to 
	#go ahead and set this up as a framework.
	createFramework Mono.framework ${MONOVERSION}
	for i in \
	  `ls -al /Library/Frameworks/Mono.framework/Versions/Current/bin | grep -v total | grep -v .exe | grep -vw "\." |awk '{print $9}'`; do
	  echo ${i}
	  ln -sf /Library/Frameworks/Mono.framework/Versions/Current/bin/${i} /usr/bin/${i}
	done
fi

