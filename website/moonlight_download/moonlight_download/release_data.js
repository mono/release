var i586 = "x86 32bit (i586)";
var x86_64 = "x86 64bit (x86_64)";

//var release_title = "Moonlight test";

var data =
{
	"title" : "Moonlight 1.0 Beta 1",
	"release" : "1.0b1",
	"tarball" : "http://ftp.novell.com/pub/mono/sources/moon/1.0b1/moon-1.0b1.tar.bz2",
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
			"name" : "Fedora 7",
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
		"Update to 1.0b1",
		"Upgraded Cairo to 1.8.0",
		"Upgraded Pixman to 0.12.0",
		"Fixed audio issues with PulseAudio and Alsa",
		"Performance enhancements to animation, audio, video",
		"Disabled managed features",
		"Fixes libxcb issues on SLE10 (bnc438265)",
		"Fixes media playback (bnc442895,438404,439225,435908,435912,434462,434267,433621,425264)",
		"Performance fixes (bnc435431,432975,412302,402211)",
		"Animation fixes (bnc435815,434899,434298,434261,434258,429396,434462)"

	]
};
