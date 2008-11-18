<%@ Page Language="C#" %> 
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text.RegularExpressions" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>Moonlight Downloads</title>
<link rel="stylesheet" type="text/css" href="moonlight.css"/>
<script type="text/javascript" src="release_data.js"></script>
</head>

<body>
<div id="page">
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

void Page_Init(object sender, EventArgs e)
{
        dir = "/var/www/mono-website/go-mono/archive/moonlight-plugins/latest/";
        dir = "downloads/latest";

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
		prof1_0.Checked = true;
		RadioClicked(null,null);
      //  lbl.Text = "page loaded";
}
void Page_Load(object sender, EventArgs e)
{

}

string LastModified (string path)
{
	string abspath = Path.Combine("/var/www/mono-website/go-mono/archive/moonlight",path);

	if (File.Exists(abspath))
        	return new FileInfo (abspath).LastWriteTime.ToString ("MMM dd, yyyy");
        else
	{
        	return string.Format("File \"{0}\" Not Found",path);
	}
}

string FileSize (string path)
{
	string abspath = Path.Combine("/var/www/mono-website/go-mono/archive/moonlight",path);

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
	xpi = basename;
	
	if (prof1_0.Checked)
		xpi += "-1.0";
	else
		xpi += "-2.0";	

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
<script type="text/javascript">
	var t = data.title;
	document.write(t);
</script>
</h1>

<p><a href="http://www.mono-project.com/Moonlight">Moonlight</a> is an
open source implementation of <a
href="http://silverlight.net">Microsoft Silverlight</a> for Unix systems.</p>

<!-- 
<p>View the fixes and change log for 0.8 <a href="#changelog">here</a></p>
-->

<p><strong>Warning:</strong> These are test installers and are not
complete or bug free.  They are snapshots from our
development tree and might not work.</p>

<% if (IsPrivate) { %>
<p><strong>THESE ARE PRIVATE BINARIES, NOT INTENTED FOR PUBLIC CONSUMPTION.   DO NOT DOWNLOAD.</strong>
<% } else { %>
<p><strong>Note:</strong> These are currently built <em>without</em> multimedia support.  No video or mp3 playback is enabled on these binaries.</p>
<% } %>
<p>Please see the <a href="#instructions">installation instructions</a> below.</p>



<form runat="server">
<table>
<tr><td><h2>1. Select the profile:</h2></td></tr>

<tr><td>
<div onclick="flash()">
<asp:RadioButton id="prof1_0" Text="1.0" groupname="profile" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
<asp:RadioButton id="prof2_0" Text="2.0 EXPERIMENTAL" groupname="profile" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
</div>
</td></tr>

<tr><td><h2>2. Select the architecture:</h2></td></tr>

<tr><td>
<div onclick="flash()">
<asp:RadioButton id="arch32" Text="32 bit" groupname="architecture" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
<asp:RadioButton id="arch64" Text="64 bit" groupname="architecture" runat="server" OnCheckedChanged="RadioClicked" AutoPostBack="true" />
</div>
</td></tr>

<tr><td><h2>3. Download the plugin</h2></td></tr>
<tr><td>
<div id="dllink">
<ul class="machine"> 
<li>
    <!-- <a href="<%=filepath%>" title="<%=xpi%>"> -->
     <a href="/archive/moonlight-plugins/latest/<%=xpi%>" title="<%=xpi%>">
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
<h1><a name="instructions"></a>Instructions</h1>

<p>When installing the Novell Moonlight plugin Firefox may prevent the installation and present you with an information bar.</p>

<p><img src="images/information-bar.png" alt="Information Bar"/></p>

<p>To continue the installation click <em>Edit Options...</em> on the information bar and add this site to <em>Allowed Sites</em>, then click on the appropriate installer again.</p>

<p><img src="images/allowed-sites.png" alt="Allowed Sites"/></p>

<!--
<h2><a name="changelog"></a>Release Notes</h2>
<ul><li>Plugin
<ul>
<li>Webkit loads the plugin (kangaroo, lewing)</li>
<li>The stream/downloader/request/response logic (used for
downloading media) has been been almost entirely moved from the
browser bridges into libmoon, with the browsers providing
subclasses. (kangaroo, sde)</li>
<li>Finally add argument checking to all wrapped plugin objects (fejj).</li>
<li>Windowless mode fixes (lewing, toshok)</li>
<li> Plugin event handling fixes (lewing)</li>
</ul>
</li>
<li>Engine
<ul>
<li>Many clock/animation framework fixes.  We now pass both animation
matrix tests, and many, *many* other bugs (and regressions) have
been fixed. (mdk).</li>
<li>Bug fixes in the Stroke{Collection}.HitTest and
Stroke{Collection}.Bounds code (toshok, sde).</li>
<li>Namescope merging fixes (sde, jackson)</li>
<li>Parser fixes, and changes paving the way for 2.0 work (jackson)</li>
<li>Fix mouse event bubbling behavior (toshok)</li>
</ul>
</li>
<li>Media
<ul>
<li>Big, big strides in our media framework and the various (file,
http, mms) downloaders, (fejj, rolf, kangaroo, fer)</li>
<li>MMS stream selection (kangaroo)</li>
</ul>
</li>
<li>Performance
<ul>
<li>Shape caching and bounds computation reduction (spouliot)</li>
<li>Geometry bounds work (spouliot)</li>
<li>Fast path for position updates (Canvas.Left/Canvas.Top) (toshok)</li>
<li>Improved temporary cairo surface bounds (lewing)</li>
<li>Glyph rendering speedups (fejj)</li>
<li>Resort by ZIndex as a dirty pass (toshok)</li>
</ul>
</li>
<li>Silverlight 2.0
<ul>
<li>work is progressing. A very simple 2.0 application successfully
ran. (miguel, jackson, sde).</li>
</ul>
</li>
</ul>

-->

<br/>
<h1>Source</h1>
You can download a tar ball of the source <a href="ftp://ftp.novell.com/pub/mono/sources/moon/moon-0.8.tar.bz2">here</a> or you can check it out from svn.
<pre>
svn co svn://anonsvn.mono-project.com/source/trunk/moon
</pre>



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

</body>
</html>
