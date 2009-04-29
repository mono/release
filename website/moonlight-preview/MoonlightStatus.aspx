<%@ Page Language="C#" Inherits="MoonlightStatus.MoonlightStatus" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="KEYWORDS" content="TemplateExport" />
<meta name="robots" content="index,follow" />
<meta name="verify-v1" content="CdUrKULfeirXCs/Mpc2sobgsPFNoqmiRL/5n0n08dAY=" /><link rel="shortcut icon" href="/favicon.ico" />
<link title="Creative Commons" type="application/rdf+xml" href="/index.php?title=TemplateExport&amp;action=creativecommons" rel="meta" />
<link rel="copyright" href="http://www.gnu.org/copyleft/fdl.html" />
    <link rel="alternate" type="application/rss+xml" title="RSS" href="http://mono-project.com/news/index.rss2"/>

    <link rel="stylesheet" type="text/css" media="print" href="http://mono-project.com/skins/common/commonPrint.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="http://mono-project.com/skins/Mono2/screen.css" />
    <script type="text/javascript" src="http://mono-project.com/skins/Mono2/prototype.js"></script>
    <script type="text/javascript" src="http://mono-project.com/skins/Mono2/wikihacks.js"></script>
    <script type="text/javascript" src="http://mono-project.com/skins/common/wikibits.js"></script>
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"> </script>
    <script type="text/javascript">
        _uacct = "UA-76510-1";
        urchinTracker();
    </script>

  <script type="text/javascript" src="release_data.js"></script>
  <script type="text/javascript" src="download.js"></script>
  <link rel="stylesheet" type="text/css" href="style.css" media="screen">

<title>
<% if (Request["v"] == "2") { %>
	Moonlight 2.0 test sites
<% } else { %>
	Moonlight 1.0 test sites
<% } %>
</title>

  </head>
  <body id="page-TemplateExport" class="ns-0">
<div id="page">
  <div id="header">
    <h1>Mono</h1>
    <a href="http://mono-project.com/"><img src="http://mono-project.com/skins/Mono2/images/header-logo.png" alt="Mono" /></a>
    <ul>
          <li  id="menu-n-home"><a href="http://mono-project.com/Main_Page">Home</a></li>

      <li id="menu-n-download"><a href="http://www.go-mono.com/mono-downloads/download.html">Download</a></li>
      <li class="current_page_item" id="menu-n-start"><a href="http://mono-project.com/Start">Start</a></li>
      <li  id="menu-n-news"><a href="http://www.mono-project.com/news/">News</a></li>
      <li  id="menu-n-contribute"><a href="http://mono-project.com/Contributing">Contribute</a></li>
      <li  id="menu-n-contact"><a href="http://mono-project.com/Contact">Contact</a></li>
      <li  id="menu-n-forums"><a href="http://www.go-mono.com/forums">Forums</a></li>

      <li  id="menu-n-blogs"><a href="http://www.go-mono.com/monologue">Blogs</a></li>
    </ul>
    <div id="search">
      <form method="get" action="http://www.google.com/search?">
        <div>
          <input type="hidden" value="www.mono-project.com" id="sitesearch" name="sitesearch" />
          <input type="hidden" value="www.mono-project.com" id="domains" name="domains" />
          <input name="q" id="q" type="text" value="Search Mono" 
            onblur="if (this.value == '') this.value='Search Mono';" 
            onfocus="if (this.value == 'Search Mono') this.value='';" />

        </div>
      </form>
    </div>
  </div>


    <div id="content-header">
			<h2 class="firstHeading">
				<% if (Request["v"] == "2") { %>
				Moonlight 2.0 test sites
				<% } else { %>
				Moonlight 1.0 test sites
				<% } %>
			</h2>
	</div>
    <div id="wrapper" class="wide">
    <div id="content" class="wide">


<div class="page">

<p>This is a list of various Silverlight websites that we are using to test Moonlight 1.0, and the current status of each test.
				To edit this page, modify trunk/moon/demo-status.txt.</p>
				<p>The rating of each site is a somewhat arbitrary rank of 0-4 based on the functionality and appearance of the site.
				</p>
				<br/>
				<table border="1" cellpadding ="0">
				<tr>
					 <th width=\"50\">Rating</th><th width=\"100\">Icons</th><th>Description</th></tr>
				   <tr><td>-1</td><td><img src="http://www.mono-project.com/files/a/aa/Help.png"/></td>
					<td>Site url is broken or the application is broken on Silverlight</td></tr>

				   <tr><td>0</td><td><img src="http://www.mono-project.com/files/8/8c/Delete.png"/></td>
					<td>Site has no functionality or crashes Firefox</td></tr>

				   <tr><td>1</td><td><img src="http://www.mono-project.com/files/2/2e/Star.png"/></td>
					<td>Site has minimal functionality and/or major cosmetic issues.</td></tr>

				   <tr><td>2</td><td><img src="http://www.mono-project.com/files/2/2e/Star.png"/><img src="http://www.mono-project.com/files/2/2e/Star.png"/></td>
					<td>Site has some functionality and/or cosmetic issues</td></tr>

				   <tr><td>3</td><td><img src="http://www.mono-project.com/files/2/2e/Star.png"/><img src="http://www.mono-project.com/files/2/2e/Star.png"/><img src="http://www.mono-project.com/files/2/2e/Star.png"/></td>
					<td>Site has most features working and/or has minor cosmetic issues</td></tr>

				   <tr><td>4</td><td><img src="http://www.mono-project.com/files/2/22/Accept.png"/></td>
					<td>All feature of the site work reliably and has proper appearance</td></tr>
				</table>
				<br/>
				<br/>
                <form id="form1" runat="server">

                        <div id="MoonContent" runat="server">

                        </div>
                </form>
<!--

<table>
<tr valign='top'>
<td style='padding: 0px;'><div id='step2' class='dl-content'></div></td>
<td style='padding: 0px; padding-left: 70px;'><div id='step3' class='dl-content'></div></td>
</tr>
</table>
<div id='step4' class="dl-content"></div>


Can not find the specific download you want?   We have
some <a href="http://www.mono-project.com/Other_Downloads">unsupported
downloads</a> you might be interested in.

<p>We also have packages for some of the
more <a href="http://mono-project.com/OpenSUSE_Build_Service">popular
software</a> that runs on Mono. -->
</div> <!-- closes page --!>
    </div><!--#content-->
    
    <div id="sidebar">
    <div id="toc-parent"></div>
    <!-- BEGIN SIDE CONTENT -->

    
    
    <!-- END SIDE CONTENT -->
    </div>
    
    <div id="footer">
      <table>
      <tr>
        <td class="novell">
          <a href="http://www.novell.com/linux"><img src="http://mono-project.com/skins/Mono2/images/novell-logo.png" alt="Novell" title="The Mono Project - Sponsored by Novell"/></a>
        </td>
        <td class="text">

          <p>All text and image content on mono-project.com, unless otherwise specified, is licensed under 
          a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/">Creative Commons 
          Attribution-Share Alike 3.0 United States License</a>. This does not include the Mono name,
          logo, or icon, which are registered trademarks of <a href="http://www.novell.com/linux">Novell</a>. 
          This does not include Mono source code.</p>          
        </td>
        <td class="creative-commons"><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/us/88x31.png"/></a></td>
      </tr>
      </table>
    </div>
    
  </div><!--#wrapper-->

</div><!--#page-->

</body>
</html>




