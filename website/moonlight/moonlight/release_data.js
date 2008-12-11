var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";

//var release_title = "Moonlight test";

var data =
{
	"title" : "Moonlight 1.0 Beta 1",
	"release" : "1.0b1",
	"tarball" : "http://ftp.novell.com/pub/mono/sources/moon/moon-1.0b1.tar.bz2",
	"archs" : [
		{
			"name" : "32 bit",
			"1.0" : "novell-moonlight-1.0-i586.xpi",
			"2.0" : "novell-moonlight-2.0-i586.xpi"
		},
		{
			"name" : "64 bit",
			"1.0" : "novell-moonlight-1.0-x86_64.xpi",
			"2.0" : "novell-moonlight-2.0-x86_64.xpi"
		},
		{
			"name" : "PowerPC",
			"1.0" : "",
			"2.0" : ""
		}
	],
	"browsers" : [ "Firefox 2*","Firefox 3"],
	"platforms" : [
		{
			"name" : "openSuse 11.0",
			"browser" : ["yes","yes","no","no"]
		},
		{
			"name" : "Fedora 9",
			"browser" : ["yes", "yes","no","no"]
		},
		{
			"name" : "Ubuntu 8.04",
			"browser" : ["yes", "yes","no","no"]
		},
		{
			"name" : "SLED 10",
			"browser" : ["yes", "yes","no","no"]
		}
	],
	"releaseNotes" : [
		"Performance enhancements with animation, media and rendering",
		"Support for the Microsoft Media Pack",
		"Blacklist binary drivers with known performance issues",
		"Fixed several memory leaks"
	]
};
