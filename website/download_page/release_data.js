var yast = "This distribution supports installing packages via YaST. Add the following installation source to YaST:"
var yast_help = "For assistance with using repositories and installing packages with YaST, <a href='http://en.opensuse.org/Add_Package_Repositories_to_YaST'>visit the YaST help page.</a>"
var zypper = "This distribution supports installing packages via Zypper. Add the following repository to Zypper:"
var zypper_help = "<p>To add the repository, execute the following commands (as root):<blockquote><code>zypper addrepo <em>&lt;URL&gt;</em> mono-stable<br/>zypper refresh --repo mono-stable<br/>zypper dist-upgrade --repo mono-stable</code></blockquote></p>"
var discontinued = "<div style=\"color: darkred; font-weight: bold\">Binaries for this platform have been discontinued.  Builds may be available from <a href=\"http://www.mono-project.com/Other_Downloads\">unsupported downloads</a> or we may be looking for a volunteer to maintain packages.</div>";
var i586_x86_64_ia64 = "i586, x86_64, and  ia64"
var i586_x86_64_ppc_ppc64_ia64 = "i586, x86_64, ppc, ppc64, and ia64"
var enterprise = "<p>The <a href=\"http://www.novell.com/products/mono/\">SUSE Linux Enterprise Mono Extension</a> is available for purchase from <a href=\"http://www.novell.com/\">Novell</a>.</p>"

var data =
{
	"release" : "2.4",
	"platforms" : [
	{
		"name" : "VMware",
		"icon" : "vmware_icon_2.jpg",
		"dlicon" : "vmware_icon.jpg",
		"version" : [
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : "Mono 2.4",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.1 VMWare image which includes Mono 2.4<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href='http://ftp.novell.com/pub/mono/vmware/Mono-2.4_openSUSE-11.1.zip.torrent'>via Torrent</a> <li><a href='http://ftp.novell.com/pub/mono/vmware/Mono-2.4_openSUSE-11.1.zip'>via http</a> </ul><a href='http://mono-project.com/VMware_Image'>Instructions for using the VMware image</a>."
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
				"name" : "Mono 2.4",
				"desc" : "",
				"downloadText" : "Download the openSUSE 11.1 Live CD which includes Mono 2.4<br/><a href=\"http://susestudio.com\"><img title=\"Built with SUSE Studio\" src=\"http://susestudio.com/images/built-with-web.png\" width=\"120\" height=\"30\" alt=\"Built with SUSE Studio\" align=\"right\"></a><ul><li><a href='http://ftp.novell.com/pub/mono/livecd/Mono-2.4_openSUSE-11.1.iso.torrent'>via Torrent</a> <li><a href='http://ftp.novell.com/pub/mono/livecd/Mono-2.4_openSUSE-11.1.iso'>via http</a> </ul>"
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
				"name" : i586_x86_64_ia64,
				"desc" : "",
				"downloadText" : yast + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_10.3\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_10.3</a></ul>" + yast_help
			}
			]
		},
		{
			"name" : "openSUSE 11.0",
			"arch" : [
			{
				"name" : i586_x86_64_ia64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.0</a></ul>" + zypper_help
			}
			]
		},
		{
			"name" : "openSUSE 11.1",
			"arch" : [
			{
				"name" : i586_x86_64_ia64,
				"desc" : "",
				"downloadText" : zypper + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1\">http://ftp.novell.com/pub/mono/download-stable/openSUSE_11.1</a></ul>" + zypper_help
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
			"name" : "SUSE Linux Enterprise 10",
			"arch" : [
			{
				"name" : "Novell Supported for i586, x86_64, and s390x",
				"desc" : "",
				"downloadText" : enterprise
			},
			{
				"name" : i586_x86_64_ia64,
				"desc" : "",
				"downloadText" : yast + "<ul><li><a href=\"http://ftp.novell.com/pub/mono/download-stable/SLE_10\">http://ftp.novell.com/pub/mono/download-stable/SLE_10</a></ul>" + yast_help
			}
			]
		},
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
				"downloadText" : "<ul><li><a href='http://ftp.novell.com/pub/mono/archive/2.4/windows-installer/6/mono-2.4-gtksharp-2.12.8-win32-6.exe'>Mono for Windows, Gtk#, and XSP</a></li><li><a href=\"http://ftp.novell.com/pub/mono/gtk-sharp/gtk-sharp-2.12.9-2.win32.msi\">Gtk# for .NET</a></li><li><a href='http://mono-project.com/MoMA'>Mono Migration Analyzer</a></li></ul>"
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
				"downloadText" : "Includes Mono, Cocoa#, Gtk# installs in /Library/Frameworks:<ul><li><a href='http://ftp.novell.com/pub/mono/archive/2.4/macos-10-universal/7/MonoFramework-2.4_7.macos10.novell.universal.dmg'>Mono 2.4_7 Framework - Universal</a></li><li><a href=\"http://monodevelop.com/Download/Mac_Preview\">MonoDevelop Preview</a> <span style=\"color: darkred; font-weight: bold\">(The MacOSX port of MonoDevelop is still incomplete, there may be serious bugs and / or missing features)</span></li></li><li><a href='http://go-mono.com/sources/cocoa-sharp/cocoa-sharp-0.9.4.tar.bz2'>Cocoa# 0.9.4 source</a></ul>Gtk# and System.Windows.Forms applications require X11.  Installing on a machine without X11 installed will result in errors during install, and these components will not function correctly."
			}
			]
		}
		]
	}

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
	}*/
	]
};
