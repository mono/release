var yast = "This distribution supports installing packages via YaST. Add the following installation source to YaST:"
var yast_help = "For assistance with using repositories and installing packages with YaST, <a href=\"http://en.opensuse.org/Add_Package_Repositories_to_YaST\">visit the YaST help page.</a>"
var zypper = "This distribution supports installing packages via Zypper. Add the following repository to Zypper:"
var zypper_help = "<p>To add the repository, execute the following commands (as root):<blockquote><code>zypper addrepo <em>&lt;URL&gt;</em> mono-stable<br/>zypper refresh --repo mono-stable<br/>zypper dist-upgrade --repo mono-stable</code></blockquote></p>"
var discontinued = "<div style=\"color: darkred; font-weight: bold\">Binaries for this platform have been discontinued.  Builds may be available from <a href=\"http://www.mono-project.com/Other_Downloads\">unsupported downloads</a> or we may be looking for a volunteer to maintain packages.</div>";
var i586_x86_64 = "i586, x86_64"
var i586_x86_64_ppc_ppc64_ia64 = "i586, x86_64, ppc, ppc64, and ia64"
var enterprise = "<p>The <a href=\"http://www.novell.com/products/mono/\">SUSE Linux Enterprise Mono Extension</a> is available for purchase from <a href=\"http://www.novell.com/\">Novell</a>.</p>"

var data =
{
	"release" : "2.6",
	"platforms" : [
	{
		"name" : "Virtual PC",
		"icon" : "virtualpc.jpg",
		"dlicon" : "virtualpc_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : "Mono 2.4.2.3",
				"desc" : "",
				"downloadText" : "Download an openSUSE 11.1 Virtual PC image which includes Mono 2.4.2.3<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3-vpc.zip.torrent\">via Torrent</a> <li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3-vpc.zip\">via http</a> </ul><a href=\"http://mono-project.com/VirtualPC_Image\">Instructions for using the Virtual PC image</a>."
			}
			]
		}
		]
	},
	{
		"name" : "VMware",
		"icon" : "vmware_icon_2.jpg",
		"dlicon" : "vmware_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : "Mono 2.4.2.3",
				"desc" : "",
				"downloadText" : "Download an openSUSE 11.1 VMWare image which includes Mono 2.4.2.3<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3-vmx.zip.torrent\">via Torrent</a> <li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3-vmx.zip\">via http</a> </ul><a href=\"http://mono-project.com/VMware_Image\">Instructions for using the VMware image</a>."
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
			"name" : "openSUSE 11.1 Live CD",
			"arch" : [
			{
				"name" : "Mono 2.4.2.3",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.1 Live CD which includes Mono 2.4.2.3<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3.iso.torrent\">via Torrent</a> <li><a href=\"http://ftp.novell.com/pub/mono/appliance/2.4.2.3/Mono-2.4.2.3.iso\">via http</a> </ul>"
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
			"name" : "openSUSE 11.0",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0</a></ul>" + zypper_help
			}
			]
		},
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1</a></ul>" + zypper_help
			}
			]
		},
		{
			"name" : "openSUSE 11.2",
			"arch" : [
			{
				"name" : i586_x86_64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.2\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.2</a></ul>" + zypper_help
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
			"name" : "SUSE Linux Enterprise 11",
			"arch" : [
			{
				"name" : "Novell Supported for i586, x86_64, and s390x",
				"desc" : "",
				"downloadText" : enterprise
			},
			{
				"name" : i586_x86_64_ppc_ppc64_ia64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/SLE_11\">http://ftp.novell.com/pub/mono/download-stable/SLE_11</a></ul>" + zypper_help
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
				"downloadText" : "<ul><li><a href=\"http://ftp.novell.com/pub/mono/archive/2.6/windows-installer/4/mono-2.6-gtksharp-2.12.9-win32-4.exe\">Mono for Windows, Gtk#, and XSP</a></li><li><a href=\"http://ftp.novell.com/pub/mono/gtk-sharp/gtk-sharp-2.12.9-2.win32.msi\">Gtk# for .NET</a></li><li><a href=\"http://mono-project.com/MoMA\">Mono Migration Analyzer</a></li></ul>"
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
			"name" : "Mac OS X Tiger (10.4), Leopard (10.5), and Snow Leopard (10.6)",
			"arch" : [
			{
				"name" : "All",
				"desc" : "This download works on Mac OS X Tiger (10.4), Leopard (10.5), and Snow Leopard (10.6).",
				"downloadText" : "Includes Mono, Cocoa#, Gtk# installs in /Library/Frameworks:<br/><em>The CSDK packages are for developers embedding mono into their applications.  If you don't know what that means you don't need it.</em><ul><li>Mono 2.6 Framework<ul><li><a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-x86/4/MonoFramework-2.6_4.macos10.novell.x86.dmg\">Intel</a> <span style=\"font-size: small\">(<a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-x86/4/MonoFramework-CSDK-2.6_4.macos10.novell.x86.dmg\">CSDK</a>)</span></li><li><a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-ppc/4/MonoFramework-2.6_4.macos10.novell.ppc.dmg\">PowerPC</a> <span style=\"font-size: small\">(<a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-ppc/4/MonoFramework-CSDK-2.6_4.macos10.novell.ppc.dmg\">CSDK</a>)</span></li><li><a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-universal/4/MonoFramework-2.6_4.macos10.novell.universal.dmg\">Universal</a> (if you don't know what you need) <span style=\"font-size: small\">(<a href=\"http://ftp.novell.com/pub/mono/archive/2.6/macos-10-universal/4/MonoFramework-CSDK-2.6_4.macos10.novell.universal.dmg\">CSDK</a>)</span></li></ul><li><a href=\"http://monodevelop.com/Download/Mac_Preview\">MonoDevelop Preview</a></li></li><li><a href=\"http://go-mono.com/sources/cocoa-sharp/cocoa-sharp-0.9.5.tar.bz2\">Cocoa# 0.9.5 source</a></ul>Gtk# and System.Windows.Forms applications require X11.  Installing on a machine without X11 installed will result in errors during install, and these components will not function correctly."
			}
			]
		}
		]
	},

/*	{
		"name" : "RedHat",
		"icon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"dlicon" : "http://www.mono-project.com/files/6/6e/Mono_icon_redhat.gif",
		"version" : [
		{
			"name" : "RedHat Enterprise Linux",
			"arch" : [
			{
				"name" : "All",
				"desc" : discontinued,
				"downloadText" : ""
			}
			]
		}
		]
	},*/
	{
		"name" : "Other",
		"icon" : "linux_icon.jpg",
		"version" : [
		{
			"name" : "Debian",
			"icon" : "debian_icon.jpg",
			"url" : "http://mono-project.com/DistroPackages/Debian"
		},
		{
			"name" : "Ubuntu",
			"icon" : "ubuntu_icon.jpg",
			"url" : "http://mono-project.com/DistroPackages/Ubuntu"
		},
		{
			"name" : "Other",
			"icon" : "linux_icon.jpg",
			"url" : "http://www.mono-project.com/Other_Downloads"
		}
		]
	}
	]
};
