<%@ Page Language="C#" MasterPageFile="frame.master" %>
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text.RegularExpressions" %>
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
string htdocs_path = "/srv/www/htdocs/mono-website/go-mono/archive/moonlight";

void Page_Init(object sender, EventArgs e)
{
        dir = "downloads/2.99.0.2";

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
	RadioClicked(null,null);
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
	xpi = basename + "-2.99.0.2";
	
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

<asp:Content ContentPlaceHolderID="title" Runat="server">Moonlight - Preview Download</asp:Content>

<asp:Content ContentPlaceHolderID="page_heading" Runat="server">
<h1>3.0 Preview 2 Download</h1>
</asp:Content>

<asp:Content ContentPlaceHolderID="main_container" Runat="server">
<style type="text/css">
ul.machine {
	list-style: none;
	padding: 0;
	margin-left: 0.5em;
}

ul.machine li {
	margin: 0 0 1em 0;
	width: 18em;
	border-color: #aaa;
	border-style: solid;
	border-width: 2px 2px 2px 10px;
	background: #555;
	padding: 0.5em;
	cursor: pointer;
}

ul li.disuaded {
	/* display: none; */
	opacity: 0.25;
}

ul.machine li:hover {
	background-color: #777;
}

ul.machine a:hover {
	color:	#fc0;
}

ul.machine li a {
	font-weight: bold;
	text-decoration: none;
}

ul.machine li a img {
	float: left;
	border: none;
	padding-right: 5px;
}

/* ul.machine > li:last-child {
	margin-bottom: 0em;
} */

.updated {
	font-size: 1em;
	font-weight: normal;
	color: #aaa;
}

.filesize {
	/* justify: right; */
	font-size: 0.75em;
	font-weight: normal;
	color: #aaa;
}
</style>

<% if (IsPrivate) { %>
<p><strong>THESE ARE PRIVATE BINARIES, NOT INTENTED FOR PUBLIC CONSUMPTION.   DO NOT DOWNLOAD.</strong></p>
<% } %>

<div id="preview-notice">
<p><b>Preview Release Security Notice</b></p>

<p> This release should be considered alpha quality.  There are
various new subsystems in Silverlight 3 (e.g. pixel shaders, local
messaging, the client http stack) which expose new and different
attack vectors, and the implementations of these subsystems have not
yet been exercised or audited.</p>

<p> As such we recommend that you should only use this plugin on trusted
sites (e.g. internal or well-known web sites) on non-production
computers. This situation will gradually evolve over the beta
releases. An up to date overview of Moonlight security features status
can be found on <a href="http://moonlight-project.com/SecurityStatus">Moonlight Security Status</a> wiki page.

</p>
</div>

<p>
Release notes can be found on the Moonlight project wiki, <a href="http://www.moonlight-project.com/Preview#Release_Notes">here</a>
</p>

<p>
Check the list of <a href="faq.aspx">supported operating systems and architectures</a>
</p>

<form runat="server">
  <table>
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
         <a href="downloads/2.99.0.2/<%=xpi%>" title="<%=xpi%>">
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
 
<h1><a name="instructions"></a>Installation</h1>

<p>When installing the Novell Moonlight plugin, Firefox may prevent the installation and present you with an information bar:</p>

<p><img src="images/information-bar.png" alt="Information Bar"/></p>

<p>To continue the installation click <em>Edit Options...</em> on the information bar and add this site to <em>Allowed Sites</em>, then click on the appropriate installer again.</p>

<p><img src="images/allowed-sites.png" alt="Allowed Sites"/></p>

</asp:Content>


