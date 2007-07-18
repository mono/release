import re

ignoresource = re.compile("\.(no)?src\.rpm$")
matchrpm = re.compile("\.rpm$")

valid_arch = {
	'ia64':		'ia64 noarch',
	'i386':		'i686 i586 i386 noarch',
	'i586':		'i686 i586 i386 noarch',
        'ppc':		'ppc noarch',
	'x86_64':	'x86_64 i686 i586 i386 noarch',
}

required_rpms = {
	#ftp://ftp.novell.com/pub/ximian/redcarpet2/sles-8-i386/
	#ftp://kirk.provo.novell.com/install/sles8/
	'sles-8': 'aaa_base autoconf automake gcc iputils make rug sles-release util-linux vim',

	#ftp://ftp.novell.com/pub/ximian/redcarpet2/sles-9-ia64/
	'sles-9': 'XFree86-devel XFree86-libs aaa_base aaa_skel apache2 apache2-devel apache2-prefork autoconf automake bison expat file fontconfig fontconfig-devel freetype2 freetype2-devel gcc gdb glib2 glib2-devel glibc-devel iputils libapr0 libjpeg libpng libpng-devel libtiff libtool libungif m4 make mktemp ncurses-devel patch perl-XML-Parser pkgconfig procps pwdutils rug sles-release sudo tar termcap unzip util-linux vim yast2 yast2-ncurses yast2-packager yast2-ncurses zlib-devel librsvg-devel vte vte-devel pango-devel gtk2-devel libxml2-devel libart_lgpl-devel libgnomecanvas-devel libgnomeui libgnomeui-devel libglade2-devel libxslt-devel libgsf-devel libgnomeprint-devel libgnomeprintui-devel popt-devel esound-devel libbonoboui libgnome gnome-vfs2 libgnomeprint libgnomeprintui kbd netcfg',

	'suse-93': 'aaa_base autoconf automake gcc iputils make pwdutils rug util-linux vim',

	'suse-100': 'aaa_base apache2-devel apache2-prefork autoconf automake cpio esound-devel file freetype2-devel gcc gconf2-devel gettext giflib-devel glib2-devel gnome-panel-devel gtkhtml2-devel intltool iputils kbd libgda-devel libglade2-devel libgnomecanvas-devel libgnomedb-devel libgnomeprint libgnomeprint-devel libgnomeprintui libgnomeprintui-devel libgnomeui-devel libjpeg-devel libpng-devel librsvg librsvg-devel libtiff-devel libtool make man mozilla patch perl-XML-LibXML perl-XML-LibXML-Common perl-XML-NamespaceSupport perl-XML-Parser perl-XML-SAX pkgconfig popt-devel procps pwdutils python python-elementtree python-xml rpm-python sqlite2 sudo sysvinit tar unzip update-desktop-files util-linux vim vte vte-devel wget xorg-x11-devel yast2 yast2-ncurses yast2-packager zlib-devel',

	'suse-101': 'aaa_base apache2-devel apache2-prefork autoconf automake esound-devel file freetype2-devel gcc giflib-devel glib2-devel glibc-locale gnome-keyring-devel gnome-panel-devel gstreamer010-devel gstreamer010-plugins-base-devel gtk2-devel gtkhtml2-devel iputils libart_lgpl-devel libglade2-devel libgnomecanvas-devel libgnomeprint libgnomeprint-devel libgnomeprintui libgnomeprintui-devel libgnomeui-devel libgsf-devel libjpeg-devel libpng-devel librsvg librsvg-devel libtiff-devel libtool libxslt-devel make makedev patch perl-XML-LibXML perl-XML-LibXML-Common perl-XML-NamespaceSupport perl-XML-Parser perl-XML-SAX pkgconfig popt-devel procps pwdutils smart sqlite2 sudo sysvinit tar unzip util-linux vim vte-devel wget xorg-x11-devel yast2 yast2-ncurses zip zlib-devel',

	'suse-102': 'aaa_base apache2-devel apache2-prefork autoconf automake bc bison esound-devel file freetype2-devel gcc giflib-devel glib2-devel glibc-locale gnome-keyring-devel gnome-panel-devel gstreamer010-devel gstreamer010-plugins-base-devel gtk2-devel gtkhtml2-devel gtksourceview-devel intltool iputils libart_lgpl-devel libglade2-devel libgnomecanvas-devel libgnomeprint libgnomeprint-devel libgnomeprintui libgnomeprintui-devel libgnomeui-devel libgsf-devel libjpeg-devel libpng-devel librsvg librsvg-devel libtiff-devel libtool libxslt-devel make makedev patch perl-XML-LibXML perl-XML-LibXML-Common perl-XML-NamespaceSupport perl-XML-Parser perl-XML-SAX pkgconfig popt-devel procps pwdutils rsync sqlite2 subversion openssh sudo sysvinit tar update-desktop-files unzip util-linux vim vte-devel wget xorg-x11-devel yast2 yast2-ncurses zip zlib-devel zypper libgnomedb-devel',

	# ftp://ftp.novell.com/pub/ximian/redcarpet2/redhat-9-i386/
	# ftp://ftp.redhat.com/pub/redhat/linux/9/en/os/i386/
	'redhat-9': 'autoconf automake gcc make vim-enhanced',
	#'redhat-9': 'autoconf automake gcc make vim-enhanced bison libtool libart_lgpl-devel gtk2-devel libxml2-devel libgnomecanvas-devel libgnomeui-devel libgnomeprintui22-devel librsvg2-devel libglade2-devel librsvg2-devel httpd-devel freetype-devel libpng-devel libungif-devel libtiff-devel libjpeg-devel python patch zip unzip wget coreutils libtermcap',

	#'fedora-4': 'autoconf automake gcc make openssh-clients perl-XML-Parser perl-XML-Simple rpm-build sudo vim-enhanced yum',
	# Can be used to create jail from first iso, and then use yum for the full list
	#'fedora-4': 'gcc make openssh-clients sudo vim-minimal yum',

	'fedora-4': 'autoconf automake bzip2 coreutils fontconfig-devel freetype-devel gcc gcc-c++ libungif-devel glib2-devel gnome-panel-devel gtk2-devel gtkhtml3-devel httpd-devel libart_lgpl-devel libglade2-devel libgnomecanvas-devel libgnomeprintui22-devel libgnomeui-devel libjpeg-devel libpng-devel librsvg2-devel libtiff-devel libtool libxml2-devel make openssh-clients pango-devel perl-XML-Parser perl-XML-Simple pkgconfig rpm-build sqlite-devel sudo tcl vim-enhanced vte-devel which yum zlib-devel',

	'fedora-5': 'autoconf automake bzip2 coreutils fontconfig-devel freetype-devel gcc gcc-c++ giflib-devel glib2-devel gnome-panel-devel gtk2-devel gtkhtml3-devel httpd-devel libX11-devel libXrender-devel libart_lgpl-devel libglade2-devel libgnomecanvas-devel libgnomeprintui22-devel libgnomeui-devel libjpeg-devel libpng-devel librsvg2-devel libtiff-devel libtool libxml2-devel make openssh-clients pango-devel perl-XML-Parser perl-XML-Simple pkgconfig rpm-build sqlite-devel sudo tcl vim-enhanced vte-devel which yum zlib-devel',

}

environment = {
	'redhat-9':	"LD_ASSUME_KERNEL=2.2.5",
}


# Other various/optional post jail settings:
settings = {
        'nameservers':  '137.65.1.3 137.65.1.4 130.57.22.5',
        'users':        'builder',
}

post_install_notes = {

	'suse-101':	"""# Create some devices:
mknod -m 666 /dev/null c 1 3
mknod -m 666 /dev/zero c 1 5 
mknod -m 666 /dev/random  c  1 8
mknod -m 644 /dev/urandom c  1 9
""",
	'suse-102':	"""# Create some devices:
mknod -m 666 /dev/null c 1 3
mknod -m 666 /dev/zero c 1 5 
mknod -m 666 /dev/random  c  1 8
mknod -m 644 /dev/urandom c  1 9

	Also, had to comment out my_test_for_space in SuSEconfig script
""",

	'fedora-4':	"""Disable gpg keys and set gpgcheck to 0 in /etc/yum.repos.d/*
MAKEDEV in /dev for random, urandom and null, touch /etc/fstab""",

	'fedora-5':	"""# MAKEDEV in /dev for random, urandom and null, Add /proc to /etc/fstab""",

}


