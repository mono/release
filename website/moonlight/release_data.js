var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";

//var release_title = "Moonlight test";

var data =
{
	"title"   : "Moonlight 1.0.1",
	"release" : "1.0.1",
	"tarball" : "http://ftp.novell.com/pub/mono/sources/moon/moon-1.0.1.tar.bz2",
	"tag"     : "http://anonsvn.mono-project.com/source/tags/moon/1.0.1",
	"archs" : [
		{
			"name" : "32 bit",
			"1.0" : "novell-moonlight-1.0.1-i586.xpi",
			"2.0" : "novell-moonlight-2.0-i586.xpi"
		},
		{
			"name" : "64 bit",
			"1.0" : "novell-moonlight-1.0.1-x86_64.xpi",
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
		"Fixed bug relating to decimal representation in different locales",
		"Fixed issues with non-ascii locales",
		"Added support for Moonshine media player",
		"Fixed codec installation issues",
		"Fixed some event handler issues"
	]
};
