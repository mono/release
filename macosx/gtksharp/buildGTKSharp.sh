#!/bin/sh -x

#Modified by Attila Balogh to build GTK#

#Complete rewrite by Adhamh Findlay <mono@adhamh.com> 7-14-04
#now compiles gettext, pkgconfig, icu, glib, and mono into frameworks
#more extensible so that other projects can be built into frameworks as well.
#this script can't build from CVS because it uses curl to download releases
#possible improvements
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
# Changes July 29 by d0lphin
# - Added gnome, cups, gtk#

. ./library.sh

set -e 

BUILDROOT="/Users/Shared/MonoBuild"
VERSION="1.0.1"
BASEPREFIX="/Library/Frameworks"
PREFIX=""
MONOURL="http://www.go-mono.com/archive/1.0.1/mono-1.0.1.tar.gz"
REMOVE="NO"
CLEAN="NO"
PACKAGE="NO"
CONFIGURE="YES"
SHPATH=$PWD
#CVS is the path to the directory where you checked out modules, module names should not be included.
CVS=""

usage()
{
# 		-p <prefix for builds> #default is /Library/Frameworks/Mono.framework/Versions/\$VERSION
# 		-v <version of Mono>
# 		-i <dependencies dir> #location for mono deps
# 		-m <mono url> #url to use for Mono source
echo "Proper usage is as follows"
cat <<EOF
buildNew.sh
	-o path to where CVS modules were checked out, don't include module name
		example:  /usr/local/monocvs
	-g remove gz files (default no)
	-m make clean (default no)
	-c run configure (default yes)
	-p create packages in $BUILDROOT/MonoBuild
	-h this message
EOF
exit
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


trap cleanup 2

#get the options passed in on the command line.  doing this instead
#of a case because these are optional args.
if [ -z $1 ]; then
	usage
else
while getopts hvpimcg option
	do
		#Turn this back on when CVS builds are ready.
		#case $option in
		#	"o") CVS=$OPTARG;;
		#	/?) usage;;
		#esac
 		if [ $option == "s" ]; then
 			CVS=$OPTARG	
 		fi
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
fi

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/X11R6/lib/pkgconfig

creatDirs

#Shez, seems like we need a config file that would be parsed for this info.
#Build the /Library/Frameworks/PkgConfig.framework
build PkgConfig.framework 0.15 \
	http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-0.15.0.tar.gz \
	pkgconfig-0.15.0.tar.gz pkgconfig-0.15.0
#Build the /Library/Frameworks/GetText.framework
build GetText.framework 0.14.1 \
	http://ftp.gnu.org/pub/gnu/gettext/gettext-0.14.1.tar.gz \
	gettext-0.14.1.tar.gz gettext-0.14.1

#Build the /Library/Frameworks/Gnome.framework/Frameworks/Glib2.framework
#this is don to provide a means to add more Gnome code later

build Gnome.framework/Frameworks/Glib2.framework 2.4.1 \
	ftp://ftp.gtk.org/pub/gtk/v2.4/glib-2.4.1.tar.gz \
	glib-2.4.1.tar.gz glib-2.4.1

build Gnome.framework/Frameworks/Atk.framework 1.4.1 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/atk-1.4.1.tar.gz \
	atk-1.4.1.tar.gz atk-1.4.1

build Gnome.framework/Frameworks/Pango.framework 1.2.5 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/pango-1.2.5.tar.gz \
	pango-1.2.5.tar.gz pango-1.2.5

build Gnome.framework/Frameworks/Intltool.framework 0.30.0 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/intltool-0.30.tar.gz \
	intltool-0.30.tar.gz intltool-0.30

build Gnome.framework/Frameworks/Jpeg.framework 6.0 \
	http://www.xfig.org/jpeg/jpegsrc.v6b.tar.gz \
	jpegsrc.v6b.tar.gz jpeg-6b

build Gnome.framework/Frameworks/Tiff.framework 3.6.1 \
	http://dl1.maptools.org/dl/libtiff/tiff-v3.6.1.tar.gz \
	tiff-v3.6.1.tar.gz tiff-v3.6.1

build Gnome.framework/Frameworks/Png.framework 1.2.6 \
 	http://umn.dl.sourceforge.net/sourceforge/libpng/libpng-1.2.6.tar.gz \
	libpng-1.2.6.tar.gz libpng-1.2.6

build Gnome.framework/Frameworks/Gtk2+.framework 2.2.4 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/gtk+-2.2.4.tar.gz \
	gtk+-2.2.4.tar.gz gtk+-2.2.4

build Gnome.framework/Frameworks/Libart_lgpl.framework 2.3.16 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libart_lgpl-2.3.16.tar.gz \
	libart_lgpl-2.3.16.tar.gz libart_lgpl-2.3.16

build Gnome.framework/Frameworks/LibIDL.framework 0.8.3 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libIDL-0.8.3.tar.gz \
	libIDL-0.8.3.tar.gz libIDL-0.8.3

build Gnome.framework/Frameworks/Popt.framework 1.7 \
	ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.1.x/popt-1.7.tar.gz \
	popt-1.7.tar.gz popt-1.7

build Gnome.framework/Frameworks/ORBit2.framework 2.11.1 \
	ftp://ftp.gnome.org/pub/gnome/sources/ORBit2/2.11/ORBit2-2.11.1.tar.gz \
	ORBit2-2.11.1.tar.gz ORBit2-2.11.1

build Gnome.framework/Frameworks/Libxml2.framework 2.6.4 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libxml2-2.6.4.tar.gz \
	libxml2-2.6.4.tar.gz libxml2-2.6.4

build Gnome.framework/Frameworks/Libbonobo.framework 2.4.3 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libbonobo-2.4.3.tar.gz \
	libbonobo-2.4.3.tar.gz libbonobo-2.4.3

build Gnome.framework/Frameworks/Libglade.framework 2.0.1 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libglade-2.0.1.tar.gz \
	libglade-2.0.1.tar.gz libglade-2.0.1

build Gnome.framework/Frameworks/Libgnomecanvas.framework 2.4.0 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libgnomecanvas-2.4.0.tar.gz \
	libgnomecanvas-2.4.0.tar.gz libgnomecanvas-2.4.0

build Gnome.framework/Frameworks/GConf.framework 2.4.0 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/GConf-2.4.0.1.tar.gz \
	GConf-2.4.0.1.tar.gz GConf-2.4.0.1

#this one is actually not a framework itself, it installs into /L/F/Perl.framework
build Gnome.framework/Frameworks/XML-Parser.framework 2.34 \
	ftp://ftp.cpan.org/pub/CPAN/modules/by-module/XML/XML-Parser-2.34.tar.gz \
	XML-Parser-2.34.tar.gz XML-Parser-2.34

build Gnome.framework/Frameworks/Gnome-mime-data.framework 2.4.1 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/gnome-mime-data-2.4.1.tar.gz \
	gnome-mime-data-2.4.1.tar.gz gnome-mime-data-2.4.1

build Gnome.framework/Frameworks/Gnome-vfs.framework 2.6.1 \
	ftp://ftp.acc.umu.se/pub/GNOME/desktop/2.6/2.6.2/sources/gnome-vfs-2.6.1.1.tar.gz \
	gnome-vfs-2.6.1.1.tar.gz gnome-vfs-2.6.1.1

build Gnome.framework/Frameworks/Libgnome.framework 2.4.0 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libgnome-2.4.0.tar.gz \
	libgnome-2.4.0.tar.gz libgnome-2.4.0

build Gnome.framework/Frameworks/Libbonoboui.framework 2.4.3 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libbonoboui-2.4.3.tar.gz \
	libbonoboui-2.4.3.tar.gz libbonoboui-2.4.3

build Gnome.framework/Frameworks/Libgnomeui.framework 2.4.0.1 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libgnomeui-2.4.0.1.tar.gz \
	libgnomeui-2.4.0.1.tar.gz libgnomeui-2.4.0.1

build Gnome.framework/Frameworks/Librsvg.framework 2.4.0 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/librsvg-2.4.0.tar.gz \
	librsvg-2.4.0.tar.gz librsvg-2.4.0

build Gnome.framework/Frameworks/Gail.framework 1.4.1 \
	ftp://ftp.gnome.org/Public/GNOME/desktop/2.4/2.4.2/sources/gail-1.4.1.tar.gz \
	gail-1.4.1.tar.gz gail-1.4.1

build Cups.framework 58 \
	http://www.opensource.apple.com/darwinsource/tarballs/other/cups-58.tar.gz \
	cups-58.tar.gz cups-58

build Gnome.framework/Frameworks/Libgnomeprint.framework 2.6.2 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.6/2.6.2/sources/libgnomeprint-2.6.2.tar.gz \
	libgnomeprint-2.6.2.tar.gz libgnomeprint-2.6.2

build Gnome.framework/Frameworks/Hicolor-icon-theme.framework 0.5 \
	http://freedesktop.org/Software/icon-theme/releases/hicolor-icon-theme-0.5.tar.gz \
	hicolor-icon-theme-0.5.tar.gz hicolor-icon-theme-0.5

#build Gnome.framework/Frameworks/Gnome-icon-theme.framework 1.2.3 \
#	ftp://ftp.gnome.org/Public/GNOME/desktop/2.6/2.6.2/sources/gnome-icon-theme-1.2.3.tar.gz \
#	gnome-icon-theme-1.2.3.tar.gz gnome-icon-theme-1.2.3

build Gnome.framework/Frameworks/Libgnomeprintui.framework 2.4.2 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libgnomeprintui-2.4.2.tar.gz \
	libgnomeprintui-2.4.2.tar.gz libgnomeprintui-2.4.2

build Gnome.framework/Frameworks/Libxslt.framework 1.1.2 \
	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/libxslt-1.1.2.tar.gz \
	libxslt-1.1.2.tar.gz libxslt-1.1.2

#missing the docbook dtds
#build Gnome.framework/Frameworks/Scrollkeeper.framework 0.3.14 \
#	ftp://ftp.gnome.org/pub/GNOME/desktop/2.4/2.4.2/sources/scrollkeeper-0.3.14.tar.gz \
#	scrollkeeper-0.3.14.tar.gz scrollkeeper-0.3.14

#build Gnome.framework/Frameworks/Libgnomedb.framework 1.1.5 \
#	ftp://ftp.gnome.org/pub/GNOME/sources/libgnomedb/1.1/libgnomedb-1.1.5.tar.gz \
#	libgnomedb-1.1.5.tar.gz libgnomedb-1.1.5
#exit

build Gnome.framework/Frameworks/Gtkhtml.framework 3.1.12 \
	ftp://ftp.gnome.org/Public/GNOME/sources/gtkhtml/3.1/gtkhtml-3.1.12.tar.gz \
	gtkhtml-3.1.12.tar.gz gtkhtml-3.1.12

build Gnome.framework/Frameworks/Vte.framework 0.11.10 \
	http://ftp.acc.umu.se/pub/GNOME/sources/vte/0.11/vte-0.11.10.tar.gz \
	vte-0.11.10.tar.gz vte-0.11.10

build Gnome.framework/Frameworks/Libgda.framework 1.0.4 \
	ftp://ftp.acc.umu.se/pub/GNOME/sources/libgda/1.0/libgda-1.0.4.tar.gz \
	libgda-1.0.4.tar.gz libgda-1.0.4

build Gnome.framework/Frameworks/Gtksourceview.framework 1.0.1 \
	ftp://ftp.gnome.org/Public/GNOME/sources/gtksourceview/1.0/gtksourceview-1.0.1.tar.gz \
	gtksourceview-1.0.1.tar.gz gtksourceview-1.0.1

#You should already have Mono.framework installed.

build Icu.framework 2.8 \
	"--disable-epsv ftp://www-126.ibm.com/pub/icu/2.8/icu-2.8.tgz" \
	icu-2.8.tgz icu 

build Mono.framework 1.0.1 \
	http://www.go-mono.com/archive/1.0.1/mono-1.0.1.tar.gz \
	mono-1.0.1.tar.gz mono-1.0.1 

build GTKSharp.framework 1.0 \
	http://mono.ximian.com/archive/1.0/gtk-sharp-1.0.tar.gz \
	gtk-sharp-1.0.tar.gz gtk-sharp-1.0 

echo "build completed"

if [ $PACKAGE == "YES" ]; then
	echo "starting packaging"
	createPackage PkgConfig 0.15 org.freedesktop.pkgconfig "PkgConfig Framework 0.15"
	createPackage GetText 0.14.1 org.gnu.gettext "GetText Framework 0.14.1"
	createPackage Gnome 2.4 org.gnome "Gnome Framework 2.4"
	createPackage Mono 1.0 com.ximian.mono "Mono Framework 1.0" Framework 1.0
fi
