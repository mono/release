<%@ Page Language="C#" %>
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text.RegularExpressions" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Moonlight Downloads</title>
<link rel="stylesheet" type="text/css" href="css/moonlight.css"/>

</head>

<body>
<div id="page">

<script type="text/xaml" id="bannerxaml">
    <Canvas xmlns="http://schemas.microsoft.com/client/2007"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
            x:Name="root" Width="500" Height="25">
      <Rectangle x:Name="rect" Width="500" Height="25" Fill="#B7CEEC" RadiusX="5" RadiusY="5" />
      <TextBlock x:Name="message" TextWrapping="NoWrap" />
    </Canvas>
</script>

<div id="moonlight-banner" style="width: 100%; height: 0px;"> </div>

<script type="text/javascript" src="Silverlight.js" /></script>
<script type="text/javascript">

var released_version = "1.99.1";

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
string src_tarball_location = "http://ftp.novell.com/pub/mono/sources/moon/1.99.1";
string svn_location = "http://anonsvn.mono-project.com/source/branches/moon/1.99.1";

void Page_Init(object sender, EventArgs e)
{
        dir = "/var/www/mono-website/go-mono/archive/moonlight-plugins/1.99.1/";
        dir = "downloads/1.99.1";

        if (IsPrivate) {
                media = "-ffmpeg";
        } else {
                media = "";
        }
        basename = "novell-moonlight" + media;

        if (Regex.IsMatch(Request.UserAgent, "Firefox")) {
                if (Regex.IsMatch(Request.UserAgent, "Linux i.86")) {
                        arch = "i586";
                } else if (Regex.IsMatch(Request.UserAgent, "Linux x86_64")) {
                        arch = "x86_64";
                } else {
                        arch = "unknown";
                }
        } else {
                arch = "unknown";
        }

        if (arch == "unknown") {
		// make sure *something* is selected
		architecture.SelectedValue = "i586";
        }
        else {
		architecture.SelectedValue = arch;
        }

	ArchSelected (null, null);
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

void ArchSelected(object sender, EventArgs e)
{
	SetFileName();
	fileupdate = LastModified(filepath);
	filesize = FileSize(filepath);
	userfriendly = UserFriendly(filepath);
}

void SetFileName()
{
	xpi = basename + "-1.99.1-" + architecture.SelectedValue + ".xpi";
	filepath = Path.Combine(dir,xpi);
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
Moonlight 2.0 Beta 1
</h1>

<p><a href="http://www.mono-project.com/Moonlight">Moonlight</a> is an
open source implementation of <a
href="http://silverlight.net">Microsoft Silverlight</a> for Unix systems.</p>


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

<form runat="server">
<table>
<tr><td><h2>1. Select the architecture:</h2></td></tr>

<tr><td>
<div onclick="flash()">
<asp:RadioButtonList id="architecture" RepeatLayout="Flow" RepeatDirection="Horizontal" runat="server" AutoPostBack="true" OnSelectedIndexChanged="ArchSelected">
    <asp:ListItem Value="i586" selected="true">x86 32bit</asp:ListItem>
    <asp:ListItem Value="x86_64">x86 64bit</asp:ListItem>
</asp:RadioButtonList>
</div>
</td></tr>

<tr><td><h2>2. Download the plugin</h2></td></tr>
<tr><td>
<div id="dllink">
<ul class="machine"> 
<li>
     <a href="/archive/moonlight-plugins/1.99.1/<%=xpi%>" title="<%=xpi%>">
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

<p> When installing the Novell Moonlight plugin Firefox may prevent the installation and present you with an information bar:</p>

<img src="images/information-bar.png" alt="Information Bar"/>

<p>To continue the installation click <em>Allow.</em></p>

<h1>Release Notes</h1>
<p>Release notes can be found on the Moonlight project wiki, <a href="http://www.moonlight-project.com/Beta#Release_Notes">here</a>.</p>

<h1>Bugs</h1>
<p>If you come across any bugs using the beta, please tell us about it. See our <a href="http://mono-project.com/Bugs">Bugzilla page</a> about logging bugs.</p>
<p><a href="https://bugzilla.novell.com/enter_bug.cgi?alias=&assigned_to=&blocked=&bug_file_loc=http%3A%2F%2F&bug_severity=Normal&bug_status=NEW&cf_biz_priority=&cf_foundby=Community%20User&cf_nts_priority=&cf_nts_support_num=&cf_partnerid=&comment=Steps%20to%20reproduce%20the%20problem%3A%0D%0A%0D%0A%0D%0A%0D%0AExpected%20results%3A%0D%0A%0D%0A%0D%0AActual%20results%3A%0D%0A%0D%0A%0D%0AHow%20often%20does%20this%20happen%3F%20Always&component=&contenttypeentry=&contenttypemethod=autodetect&contenttypeselection=text%2Fplain&data=&deadline=&dependson=&description=&estimated_time=0.0&flag_type-2=X&flag_type-3=X&form_name=enter_bug&keywords=&maketemplate=Remember%20values%20as%20bookmarkable%20template&op_sys=Other&priority=P5%20-%20None&product=Moonlight&qa_contact=&rep_platform=Other&short_desc=&version=1.99.1">
Use this template</a> to log a bug against the Moonlight Beta</p>

<h1>Source</h1>
<p>You can download a tarball of the source <a href="<%=src_tarball_location%>">here</a>, or you can check it out from svn.
<pre> svn co <%=svn_location%> </pre></p>

</div> <!-- col2 -->
</div> <!-- page -->


<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-76510-5");
pageTracker._trackPageview();
} catch(err) {}</script>


<% if (Request["unknown"] == "1") { %>
<script type="text/javascript">
	alert("Moonlight 2.0 does not support your operating system and/or browser configuration. Please check the list of supported platforms for more details");
</script>
<% } %>


</body>
</html>
