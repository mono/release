var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";
var i586_x86_64 = "x86 32 and 64-bit (i586, x86_64)";
var ppc = "PowerPC 32bit (ppc32)";
var ia64 = "Itanium (ia64)";
var s390 = "IBM s390 32bit";
var s390x = "IBM s390x 64bit";
var discontinued = "<div style=\"color: darkred; font-weight: bold\">Binaries for this platform have been discontinued.  Builds may be available from <a href=\"http://www.mono-project.com/Other_Downloads\">unsupported downloads</a> or we may be looking for a volunteer to maintain packages.</div>";

var data =
{
	"release" : "2.2",
	"platforms" : [
	{
		"name" : "VMware",
		"icon" : "vmware_icon_2.jpg",
		"dlicon" : "vmware_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.0",
			"arch" : [
			{
				"name" : "Mono 2.2",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.0 VMWare image which includes Mono 2.2 <ul><li><a href='http://ftp.novell.com/pub/mono/vmware/Mono-2.2_openSUSE-11.0.zip.torrent'>via Torrent</a> <li><a href='http://ftp.novell.com/pub/mono/vmware/Mono-2.2_openSUSE-11.0.zip'>via http</a> </ul><a href='http://mono-project.com/VMware_Image'>Instructions for using the VMware image</a>."
			}
			]
		}
		]
	},
	{
		"name" : "LiveCD",
		"icon" : "livecd.jpg",
		"dlicon" : "livecd.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.0 Live CD",
			"arch" : [
			{
				"name" : "Mono 2.2",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.0 Live CD which includes Mono 2.2 <ul><li><a href='http://ftp.novell.com/pub/mono/livecd/Mono-2.2_openSUSE-11.0.iso.torrent'>via Torrent</a> <li><a href='http://ftp.novell.com/pub/mono/livecd/Mono-2.2_openSUSE-11.0.iso'>via http</a> </ul>"
			}
			]
		}
		]
	},
	{
		"name" : "openSUSE",
		"icon" : "opensuse.jpg",
		"dlicon" : "opensuse.jpg",
		"version" : [
		{
			"name" : "openSUSE 10.3",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : "This distro supports installing packages via YaST. Add the following installation source to YaST:<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_10.3\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_10.3</a></ul>For assistance with using repositories and installing packages with YaST, <a href='http://en.opensuse.org/Add_Package_Repositories_to_YaST'>visit the Yast help page.</a>"
			}
			]
		},
		{
			"name" : "openSUSE 11.0",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : "This distro supports installing packages via YaST. Add the following installation source to YaST:<ul><li><a href='" + "http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0'>http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0" + "</a></ul> For assistance with using repositories and installing packages with YaST, <a href='http://en.opensuse.org/Add_Package_Repositories_to_YaST'>visit the Yast help page.</a>"
			}
			]
		},
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : "This distro supports installing packages via YaST. Add the following installation source to YaST:<ul><li><a href='" + "http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1'>http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1" + "</a></ul> For assistance with using repositories and installing packages with YaST, <a href='http://en.opensuse.org/Add_Package_Repositories_to_YaST'>visit the Yast help page.</a>"
			}
			]
		}
		]
	},

	{
		"name" : "SLES/SLED",
		"icon" : "sles.jpg",
		"dlicon" : "sles.jpg",
		"version" : [
		{
			"name" : "Suse Linux Enterprise 10",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : "This distro supports installing packages via YaST. Add the following installation source to YaST:<ul><li><a href='" + "http://ftp.novell.com/pub/mono/download-stable/SLE_10'>http://ftp.novell.com/pub/mono/download-stable/SLE_10" + "</a></ul>For assistance with using repositories and installing packages with YaST, <a href='http://en.opensuse.org/Add_Package_Repositories_to_YaST'>visit the Yast help page.</a>"
			}
			]
		}
		]
	},

	{
		"name" : "Windows",
		"icon" : "http://www.mono-project.com/files/0/00/Mono_icon_windows.gif",
		"dlicon" : "http://www.mono-project.com/files/0/00/Mono_icon_windows.gif",
		"version" : [
		{
			"name" : "Windows 2000, XP, 2003 and Vista",
			"arch" : [
			{
				"name" : "All",
				"desc" : "This download works on all versions of Windows 2000, XP, 2003 and Vista.",
				"downloadText" : "<ul><li><a href='ftp://ftp.novell.com/pub/mono/archive/2.2/windows-installer/5/mono-2.2-gtksharp-2.12.7-win32-5.exe'>Mono for Windows, Gtk#, and XSP</a></li><li><a href=\"http://ftp.novell.com/pub/mono/gtk-sharp/\">Gtk# for .NET</a></li><li><a href='http://mono-project.com/MoMA'>Mono Migration Analyzer</a></li></ul>"
			}
			]
		}
		]
	},

	{
		"name" : "Mac&nbsp;OS&nbsp;X",
		"icon" : "http://www.mono-project.com/files/b/bf/Mono_icon_mac.gif",
		"dlicon" : "http://www.mono-project.com/files/b/bf/Mono_icon_mac.gif",
		"version" : [
		{
			"name" : "Mac OS X Tiger (10.4) and Leopard (10.5)",
			"arch" : [
			{
				"name" : "All",
				"desc" : "This download works on Mac OS X Tiger (10.4) and Leopard (10.5).",
				"downloadText" : "Includes Mono, Cocoa#, Gtk# installs in /Library/Frameworks:<ul><li><a href='http://ftp.novell.com/pub/mono/archive/2.2/macos-10-universal/5/MonoFramework-2.2_5.macos10.novell.universal.dmg'>Mono 2.2_5 Framework - Universal</a></li><li><a href=\"http://ftp.novell.com/pub/mono/monodevelop/MonoDevelop-1.9.1-1.dmg\">MonoDevelop 2.0 Alpha 2</a></li></li><li><a href='http://go-mono.com/sources/cocoa-sharp/cocoa-sharp-0.9.4.tar.bz2'>Cocoa# 0.9.4 source</a></ul>Gtk# and System.Windows.Forms applications require X11.  Installing on a machine without X11 installed will result in errors during install, and these components will not function correctly."
			}
			]
		}
		]
	},

	{
		"name" : "RedHat",
		"icon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"dlicon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"desc" : "This download works on RedHat Enterprise Linux 4 on x86 32bit (i586).",
		"version" : [
		{
			"name" : "RedHat Enterprise Linux 4",
			"arch" : [
			{
				"name" : i586,
				"desc" : discontinued + "This download works on RedHat Enterprise Linux 4 on " + i586 + ".",
				//"downloadText" : "The downloads are available <a href='http://ftp.novell.com/pub/mono/download-stable/rhel-4-i386'>here</a>."
				"downloadText" : "The prefered method for installing Mono on RedHat is to use yum. Once yum is installed, putting the <a href='http://ftp.novell.com/pub/mono/download-stable/rhel-4-i386/mono.repo'>mono.repo</a> file in /etc/yum.repos.d will allow you to install mono and related packages.<br><br>For individual packages, <a href='http://ftp.novell.com/pub/mono/download-stable/rhel-4-i386'>go here</a>.<br><br>Note: You can get yum for RHEL from the <a href='http://www.centos.org/'>CentOS project</a>."
			}
			]
		}
		]
	},
	{
		"name" : "Solaris",
		"icon" : "http://www.mono-project.com/files/2/2f/Mono_icon_solaris.gif",
		"dlicon" : "http://www.mono-project.com/files/2/2f/Mono_icon_solaris.gif",
		"version" : [
		{
			"name" : "Solaris 8",
			"arch" : [
			{
				"name" : "SPARC",
				"desc" : discontinued + "This download works on Solaris 8 on SPARC.",
				"downloadText" : "<a href='http://mono-project.com/SolarisInstructions'>Solaris package instructions<ul><li><a href='http://ftp.novell.com/pub/mono/archive/1.2.4/sunos-8-sparc/4/mono-1.2.4_4.sunos8.novell.sparc.pkg.gz'>Mono 1.2.4_4 Package</a></ul>"
			}
			]
		}
		]
	}

	]
};
