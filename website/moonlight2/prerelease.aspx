<%@ Page Language="C#" MasterPageFile="frame.master" %>
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Text.RegularExpressions" %>
<script runat="server">
// UPDATE HERE FOR NEW VERSION
string version = "2.99.0.8";

string dir;
string basename;
string media;
string arch;

string [] extensions = new string [] {"xpi", "crx" };
string extension = string.Empty;
string htdocs_path = "/srv/www/htdocs/mono-website/go-mono/archive/moonlight";
string base_nightly_link = "http://moon.sublimeintervention.com/DownloadLatestFile.aspx?filename=novell-moonlight-*-{0}.{1}&amp;lane_id=17";

string i86_64Checked = string.Empty;
string i586Checked = string.Empty;
string preview_notice_display = string.Empty;

void Page_Init(object sender, EventArgs e)
{
        dir = "downloads/" + version;

        if (IsPrivate) {
                media = "-ffmpeg";
        } else {
                media = "";
        }
        basename = "novell-moonlight" + media;

        if (Regex.IsMatch(Request.UserAgent, "Linux i.86")) {
                arch = "i586";
                i586Checked = "checked='checked'";
        } else if (Regex.IsMatch(Request.UserAgent, "Linux x86_64")) {
                arch = "x86_64";
                i86_64Checked = "checked='checked'";
        } else {
                arch = "unknown";
        }

	if (Regex.IsMatch(Request.UserAgent, "Chrome")) {
		extension = ".crx";
	}
        else if (Regex.IsMatch(Request.UserAgent, "Firefox")) {
		extension = ".xpi";
        }
        
        if (extension != string.Empty)
		preview_notice_display = "none";
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

string GetFileName(string ext, string arch)
{
	return basename + "-" + version + "-" + arch + ext;
}

bool IsPrivate {
        get {
                return Request.Url.LocalPath.StartsWith ("/mpriv/");
        }
}
</script>

<asp:Content ContentPlaceHolderID="title" Runat="server">Moonlight - Preview Download</asp:Content>

<asp:Content ContentPlaceHolderID="page_heading" Runat="server">
<h1>3.0 Preview 8 Download</h1>
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

ul.machine li.wider {
	width: 20em;
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

<p>
Release notes can be found on the Moonlight project wiki, <a href="http://www.moonlight-project.com/Preview#Release_Notes">here</a>.
</p>

<p>
Check the list of <a href="faq.aspx">supported operating systems and architectures</a>
</p>

<form runat="server">
  <table>
  <tr><td colspan='2'><h2>1. Select the architecture:</h2></td></tr>
  
  <tr><td colspan='2'>
    <div onclick="flash()">
    <input type='radio' name='arch' value='32' onclick='selected32bit ();' <%= i586Checked%>/>32 bit
    <input type='radio' name='arch' value='64' onclick='selected64bit ();' <%= i86_64Checked%>/>64 bit
    </div>
  </td></tr>
  
  <tr><td colspan='2'><h2>2. Download the plugin</h2></td></tr>
  <tr style='display: <%=preview_notice_display%>;'>
    <td colspan='2'>
    <div class="preview-notice">
      <p><b>Your browser type could not be determined.</b></p>
      <p>The following plugin types are available, please select the best match for your browser.</p>
    </div>
    </td>
  </tr>

<%
  foreach (string a in new string [] {"i586", "x86_64"}) {
    string row_id =  a + "row";
    string style = "style='display: " + (a == arch ? "" : "none") + "'";
%>
  <tr id='<%=row_id%>' <%=style%>>
  <%
    foreach (string ext in extensions) {
      string id = row_id + ext;
      string cell_style = "style='display: " + (extension != string.Empty && extension != ("." + ext) ? "none" : "") + "'";
      string filepath = Path.Combine (dir, GetFileName ("." + ext, a));
      string filesize = FileSize (filepath);
      string fileupdate = LastModified (filepath);
      string title = Path.GetFileName (filepath);
      string forwhom = extension == string.Empty ? (ext == "xpi" ? "For Firefox: " : "For Chrome: ") : string.Empty;
   %>
    <td id='<%=id%>' <%=cell_style%>>
      <div class="dllink">
        <ul class="machine">
          <li class="wider">
              <a href="<%=filepath%>" title="<%=title%>">
              <img src="images/down.png" alt="Download"/>
              <strong><%=forwhom%>Linux/<%=a%></strong>
              <span class="filesize"><%=filesize%></span>
              <br/>
              <span class="updated">Last Updated: <%=fileupdate%> </span>
            </a>
          </li>
        </ul>
      </div>
    </td>
<%   } %>
  </tr>
<% } %>
  </table>
 
<div class="preview-notice">
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

<h1><a name="nightlybuild"></a>Nightly builds</h1>

  <table>
  <tr><td colspan='2'><h2>1. Select the architecture:</h2></td></tr>
  
  <tr><td colspan='2'>
    <div onclick="flash()">
    <input type='radio' name='archnightly' value='32' onclick='selected32bitnightly ();' <%= i586Checked%>/>32 bit
    <input type='radio' name='archnightly' value='64' onclick='selected64bitnightly ();' <%= i86_64Checked%>/>64 bit
    </div>
  </td></tr>
  
  <tr><td colspan='2'><h2>2. Download the plugin</h2></td></tr>

  <tr style='display: <%=preview_notice_display%>;'><td colspan='2'>
    <div class="preview-notice">
      <p><b>Your browser type could not be determined.</b></p>
      <p>The following plugin types are available, please select the best match for your browser.</p>
    </div>

  </td></tr>

<%
  // 32 bit is i686 for moonbuilder, not i586
  foreach (string a in new string [] {"i686", "x86_64"}) {
    string style = "style='display: " + (a.Replace ("i686", "i585") == arch ? "" : "none") + "'";
    string row_id = "nightly" + a + "row";
%>
  <tr id='<%=row_id%>' <%=style%>>
<%
    foreach (string ext in extensions) {
      string id = row_id + ext;
      string link = string.Format (base_nightly_link, a, ext);
      string cell_style = "style='display: " + (extension != string.Empty && extension != ("." + ext) ? "none" : "") + "'";
      string forwhom = extension == string.Empty ? (ext == "xpi" ? "For Firefox: " : "For Chrome: ") : string.Empty;
%>
    <td id='<%=id%>' <%=cell_style%>>
      <div class="dllink">
        <ul class="machine">
          <li class="wider">
            <a href="<%=link%>" title="moonlight-novell-<%=a%>-nightly.<%=ext%>">
              <img src="images/down.png" alt="Download"/>
              <strong><%=forwhom%>Linux/<%=a%></strong>
              <br/>
            </a>
          </li>
        </ul>
      </div>
    </td>
<%   } %>
  </tr>

<% } %>

  </table>
</form>
 
<div class="preview-notice">
<p><b>Nightly Build Security Notice</b></p>

<p> Nightly builds come from our automated build system, and are published
as long as the latest source code is successfully built. These packages have
not been verified in any way. Please use at your own risk.
</p>
</div>

<h1><a name="instructions"></a>Installation</h1>

<p>When installing the Novell Moonlight plugin, Firefox may prevent the installation and present you with an information bar:</p>

<p><img src="images/information-bar.png" alt="Information Bar"/></p>

<p>To continue the installation click <em>Edit Options...</em> on the information bar and add this site to <em>Allowed Sites</em>, then click on the appropriate installer again.</p>

<p><img src="images/allowed-sites.png" alt="Allowed Sites"/></p>

</asp:Content>


