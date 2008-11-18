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


<p>View the fixes and change log <a href="#changelog">here</a></p>


<% if (IsPrivate) { %>
<p><strong>THESE ARE PRIVATE BINARIES, NOT INTENTED FOR PUBLIC CONSUMPTION.   DO NOT DOWNLOAD.</strong></p>
<% } else { %>
<p><strong>Note:</strong> These are currently built <em>without</em> multimedia support.  No video or mp3 playback is enabled on these binaries.</p>
<% } %>
<p>Please see the <a href="#instructions">installation instructions</a> below.</p>


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
<h1><a name="instructions"></a>Installation instructions</h1>

<p>When installing the Novell Moonlight plugin Firefox may prevent the installation and present you with an information bar.</p>

<p><img src="images/information-bar.png" alt="Information Bar"/></p>

<p>To continue the installation click <em>Edit Options...</em> on the information bar and add this site to <em>Allowed Sites</em>, then click on the appropriate installer again.</p>

<p><img src="images/allowed-sites.png" alt="Allowed Sites"/></p>

<h2><a name="changelog"></a>Release Notes</h2>
<ul>
<script type="text/javascript">
	var notes = "";
	for(i=0; i < data.releaseNotes.length; i++)
	{
		notes += "<li>" + data.releaseNotes[i] + "</li>";

	}
	document.write(notes);

</script>
<!-- -->
</ul>

<h1>Bugs</h1>
If you come across any bugs in Moonlight 1.0, please tell us about it. See our <a href="http://mono-project.com/Bugs">Bugzilla page</a> about logging bugs.
<br/>
<h1>Source</h1>
You can download a tar ball of the source 
<script type="text/javascript">
	
	var html = "<a href='" + data.tarball + "'>here</a> ";
	document.write(html);

</script>
or you can check it out from svn.
	<pre> svn co svn://anonsvn.mono-project.com/source/tags/moon/1.0b1 </pre>

As always, you can get the development soucre from trunk:

	<pre> svn co svn://anonsvn.mono-project.com/source/trunk/moon </pre>


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
