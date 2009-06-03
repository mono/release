<%@ Page Language="C#" %> 
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text.RegularExpressions" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Moonlight Downloads</title>
<link rel="stylesheet" type="text/css" href="css/moonlight.css"/>
<script type="text/javascript" src="release_data.js"></script>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-76510-5");
pageTracker._trackPageview();
} catch(err) {}</script>
</head>

<body>
<div id="page">

<script type="text/xaml" id="bannerxaml">
    <Canvas xmlns="http://schemas.microsoft.com/client/2007"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
            x:Name="root" Width="500" Height="25">
      <Rectangle x:Name="rect" Width="500" Height="25" Fill="Orange" RadiusX="5" RadiusY="5" />
      <TextBlock x:Name="message" TextWrapping="NoWrap" />
    </Canvas>
</script>

<div id="moonlight-banner" style="width: 100%; height: 0px;"> </div>

<script type="text/javascript" src="Silverlight.js" /></script>
<script type="text/javascript">

var released_version = "1.9.3";

var plugin = navigator.plugins["Silverlight Plug-In"];
if (plugin.filename.indexOf("libmoonloader") == 0) {
  //console.log ("they're running moonlight");

  var moonlight_banner = document.getElementById ("moonlight-banner")

  function onPluginError (sender, args) {
    //console.log ("onPluginError");
    moonlight_banner.style.background="red";

    moonlight_banner.innerHTML = "error initializing plugin: " + args.errorMessage;
    moonlight_banner.style.height = "25px";
    moonlight_banner.style.marginBottom = "10px";
  }

  var root;
  var message;
  var rect;

  function control_resize ()
  {
    var control_width = parseFloat (document.defaultView.getComputedStyle (moonlight_banner,null).getPropertyValue ("width"));
    var control_height = parseFloat (document.defaultView.getComputedStyle (moonlight_banner,null).getPropertyValue ("height"));

    //console.log ("control size is " + control_width + " x " + control_height);

    root.width = rect.width = control_width;
    root.height = rect.height = control_height;

    message["Canvas.Left"] = control_width / 2 - message.actualWidth / 2; 
    message["Canvas.Top"] = control_height / 2 - message.actualHeight / 2; 
  }

  function onPluginLoad (control, userContext, rootElement)
  {
    root = rootElement;
    message = root.findName ("message");
    rect = root.findName ("rect");

    control.content.onResize = control_resize;

    //console.log ("onPluginLoad");

    moonlight_banner.style.height = "25px";
    moonlight_banner.style.marginBottom = "10px";

    var moonlight_version = control.settings.version;
    dump("current version = " + moonlight_version);
    dump("released version = " + released_version);
    //var x = Components.classes["@mozilla.org/xpcom/version-comparator;1"]
    //            .getService(Components.interfaces.nsIVersionComparator)
    //            .compare(moonlight_version,released_version);

	

    //console.log ("control.settings.version = " + control.settings.version);    

    if (moonlight_version == released_version) {
      message.text = "Congratulations, you're running the current preview release of moonlight!";
    }
    else if ((moonlight_version == "1.0.1")) {
      message.text = "You're running the latest stable release of moonlight.";
    }
    else if ((moonlight_version < released_version) || 
		(moonlight_version == "1.0b1") ||
		(moonlight_version == "1.0b2") || 
		(moonlight_version == "1.0")) {
      message.text = "You're running an older release of moonlight.  time to upgrade.";
    }
    else {
      message.text = "You're running an unstable build of moonlight.";
    }
  }

  //console.log ("creating moonlight instance");

  Silverlight.createObjectEx ({
	source: "#bannerxaml",
	parentElement: document.getElementById("moonlight-banner"),
	id: "moonlight-banner-control",
	properties: {
		width: "100%",
		height: "25",
		version: "1.0",
		isWindowless: "true"
	},
	events: {
		onError: onPluginError,
		onLoad: onPluginLoad
	}
  });
}
</script>

<div id="col1">
<img src="images/moonlight_logo.png" alt="Moonlight Logo"/>
</div>

<script runat="server">
string dir;
string basename;
string media;
string arch;

string xpi = string.Empty;
string filepath = string.Empty;
string filesize = string.Empty;
string fileupdate = string.Empty;
string userfriendly = string.Empty;
string htdocs_path = "/srv/www/htdocs/mono-website/go-mono/archive/moonlight-preview";

void Page_Init(object sender, EventArgs e)
{
        dir = "/var/www/mono-website/go-mono/archive/moonlight-plugins/1.9.3/";
        dir = "downloads/1.9.3";

        if (IsPrivate) {
                media = "-ffmpeg";
        } else {
                media = "";
        }
        basename = "novell-moonlight" + media;

        if (Regex.IsMatch(Request.UserAgent, "Firefox")) {
                if (Regex.IsMatch(Request.UserAgent, "Linux i.86")) {
                        arch = "i586";
                        arch32.Checked = true;
                        
                } else if (Regex.IsMatch(Request.UserAgent, "Linux x86_64")) {
						arch64.Checked = true;
                        arch = "x86_64";
                } else {
						arch32.Checked = true;
                        arch = "unknown";
                }
        } else {
                arch = "unknown";
				arch32.Checked = true;
        }
	//	prof1_0.Checked = true;
		RadioClicked(null,null);
      //  lbl.Text = "page loaded";
}
void Page_Load(object sender, EventArgs e)
{

}

string LastModified (string path)
{
	string abspath = Path.Combine(htdocs_path,path);

	if (File.Exists(abspath))
        	return new FileInfo (abspath).LastWriteTime.ToString ("MMM dd, yyyy");
        else
	{
        	return string.Format("File \"{0}\" Not Found",path);
	}
}

string FileSize (string path)
{
	string abspath = Path.Combine(htdocs_path,path);

	if (File.Exists(abspath))
        	return (((decimal) new FileInfo (abspath).Length) / 1024 / 1024).ToString("F1") + " MB";
    	else
    		return string.Format("File \"{0}\" Not Found",path);
}

string [] GetDownloads (string version)
{
        return Directory.GetFiles (dir, basename + "-" + version + "-*.xpi");
}

string UserFriendly (string fname)
{
        string t = Path.GetFileNameWithoutExtension (fname);
        return t.Substring (t.LastIndexOf("-")+1);
}

void RadioClicked(object sender, EventArgs e)
{
	//lbl.Text = ((System.Web.UI.WebControls.RadioButton)sender).ID.ToString();
	SetFileName();
	fileupdate = LastModified(filepath);
	filesize = FileSize(filepath);
	userfriendly = UserFriendly(filepath);
	//yourlink.NavigateUrl = filepath;
	//yourlink.Text = linktext();
	
}

void SetFileName()
{
	xpi = basename + "-1.9.3";
	
	//if (prof1_0.Checked)
	//	xpi += "-1.0";
	//else
	//	xpi += "-2.0";	

	if (arch32.Checked)
		xpi += "-i586";
	else
		xpi += "-x86_64";
	
	xpi += ".xpi";
	filepath = Path.Combine(dir,xpi);
	//return xpi;
}

bool IsPrivate {
        get {
                return Request.Url.LocalPath.StartsWith ("/mpriv/");
        }
}


</script>

<script type="text/javascript">
function flash()
{
	var obj = document.getElementById('dllink').style;	
	obj.cssText = "opacity:0.50"
}

</script>


<div id="col2">
<h1>
Moonlight 2.0 Preview 4
</h1>

<p><a href="http://www.mono-project.com/Moonlight">Moonlight</a> is an
open source implementation of <a
href="http://silverlight.net">Microsoft Silverlight</a> for Unix systems.</p>


<p>View the fixes and change log <a href="#changelog">here</a></p>


<% if (IsPrivate) { %>
<p><strong>THESE ARE PRIVATE BINARIES, NOT INTENTED FOR PUBLIC CONSUMPTION.   DO NOT DOWNLOAD.</strong></p>
<% } %>
<p>Please see the <a href="#instructions">installation instructions</a> below.</p>

<p>
Check the list of <a href="http://mono-project.com/MoonlightSupportedPlatforms">supported operating systems and architectures</a>
</p>

<div id="preview-notice">
<p><b>Preview Release Security Notice</b> </p>

<p>
Keep in mind this preview release is not feature complete. Most importantly <b>not</b> all security features are present or fully enabled in this release. Even existing security features have, at this stage, received only minimal testing and no security audit of the source code (mono or moonlight) has yet been done.
As such you should only use this preview plugin on trusted sites (e.g. internal or well-known web sites) on non-production computers. This situation will gradually evolve over the next preview and beta releases. An up to date overview of Moonlight security features status can be found on <a href="http://moonlight-project.com/SecurityStatus">Moonlight Security Status</a> wiki page.
</p>
</div>

<!--
<table id="sysreq">
<script>

	var html = "<tr style='font-weight:bold;'><td class='sys'>Operating System&nbsp;&nbsp;&nbsp;&nbsp;</td>";
	for (i =0; i < data.browsers.length; i++) {
		html += "<td class='browser'>" + data.browsers[i] + "</td>";
	}
	html += "</tr>";

	for (i=0; i < data.platforms.length; i++) {
		html += "<tr><td class='sys'>" + data.platforms[i].name + "</td>";
		for (j=0; j < data.browsers.length; j++) {
			html += "<td class='browser'>" + data.platforms[i].browser[j] + "</td>";
		}
		html += "</tr>";
	}

	document.write(html);

</script>
</table>
<p>*Firefox 2 has limited features.</p>
-->

<form runat="server">
<table>
<!--
<tr><td><h2>1. Select the profile:</h2></td></tr>

<tr><td>
<div onclick="flash()">
<asp:RadioButton id="prof1_0" Text="1.0" groupname="profile" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
<asp:RadioButton id="prof2_0" Text="2.0 EXPERIMENTAL" groupname="profile" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
</div>
</td></tr>
-->
<tr><td><h2>1. Select the architecture:</h2></td></tr>

<tr><td>
<div onclick="flash()">
<asp:RadioButton id="arch32" Text="32 bit" groupname="architecture" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
<asp:RadioButton id="arch64" Text="64 bit" groupname="architecture" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
</div>
</td></tr>

<tr><td><h2>2. Download the plugin</h2></td></tr>
<tr><td>
<div id="dllink">
<ul class="machine"> 
<li>
    <!-- <a href="<%=filepath%>" title="<%=xpi%>"> -->
     <a href="/archive/moonlight-plugins/1.9.3/<%=xpi%>" title="<%=xpi%>">
      <img src="images/down.png" alt="Download"/>
      <strong>Linux/<%=userfriendly%></strong>
      <span class="filesize"><%=filesize%></span>
      <br/>
      <span class="updated">Last Updated: 
          <%=fileupdate%>
      </span>
    </a>
  </li>
</ul>
</div>
</td></tr>

</table>
</form>
 
<br/>
<h1><a name="instructions"></a>Installation instructions</h1>

<p>When installing the Novell Moonlight plugin Firefox may prevent the installation and present you with an information bar.</p>

<p><img src="images/information-bar.png" alt="Information Bar"/></p>

<p>To continue the installation click <em>Allow.</em>

<h2><a name="changelog"></a>Release Notes</h2>
Release notes can be found on the Moonlight project wiki, <a href="http://www.moonlight-project.com/Preview#Release_Notes">here</a>.

<h1>Bugs</h1>
If you come across any bugs using the preview, please tell us about it. See our <a href="http://mono-project.com/Bugs">Bugzilla page</a> about logging bugs.
<br/>
<h1>Source</h1>
You can download a tarball of the source
<script type="text/javascript">
	var html = "<a href='" + data.tarball + "'>here</a> ";
	document.write(html);
</script>

or you can check it out from svn.
<script type="text/javascript">
	var html = "<pre> svn co " + data.tag + "</pre> ";
	document.write(html);
</script>


</div> <!-- col2 -->
</div> <!-- page -->

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-76510-1");
pageTracker._trackPageview();
</script>


<% if (Request["unknown"] == "1") { %>
<script type="text/javascript">
	alert("Moonlight 2.0 does not support your operating system and/or browser configuration. Please check the list of supported platforms for more details");
</script>
<% } %>


</body>
</html>
