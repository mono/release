<%@ Page Language="C#" AutoEventWireup="true" ValidateRequest="false" %>
<script runat="server">
    public void Page_Error( object sender, System.EventArgs e )
    {
        Exception x = Server.GetLastError();
        YAF.Classes.Data.DB.eventlog_create( YafContext.Current.PageUserID, this, x );
        YAF.Classes.Utils.CreateMail.CreateLogEmail( x );
    }		
</script>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml">
<head id="YafHead" runat="server">
    <meta name="Description" content="A bulletin board system written in ASP.NET" />
    <meta name="Keywords" content="Yet Another Forum.net, Forum, ASP.NET, BB, Bulletin Board, opensource" />
    <title>This title is overwritten</title>
        <link rel="alternate" type="application/rss+xml" title="RSS" href="http://forums.monotouch.net/yaf_rsstopic.aspx?pg=forum"/>

    <link rel="stylesheet" type="text/css" media="print" href="http://mono-project.com/skins/common/commonPrint.css" />
    <link rel="stylesheet" type="text/css" media="screen" href="http://mono-project.com/skins/MonoWave/screen.css" />
</head>
<body>
    <div id="page">
  <div id="tl"></div>
  <div id="tr"></div>
  <div id="header">
    <h1>Mono</h1>    
    <a href="/" title="MonoTouch"><div id="mono-logo"></div></a>

    <ul>
            <li id="menu-n-home" >
					    <a href="http://monotouch.net/">Home</a>

					  </li>
            <li id="menu-n-documentation" >
					    <a href="http://monotouch.net/Documentation">Documentation</a>
					  </li>
            <li id="menu-n-tutorials" >
					    <a href="http://monotouch.net/Tutorials">Tutorials</a>
					  </li>
            <li id="menu-n-community" class="current_page_item" >

					    <a href="http://monotouch.net/Community">Community</a>
					  </li>
            <li id="menu-n-wiki" >
					    <a href="http://wiki.monotouch.net/">Wiki</a>
					  </li>
            <li id="menu-n-support" >
					    <a href="http://monotouch.net/Support">Support</a>

					  </li>
            <li id="menu-n-store" >
					    <a href="http://monotouch.net/Store">Store</a>
					  </li>

    </ul>
    <div id="search">
      <form method="get" action="http://www.google.com/search?">
        <div>

          <input type="hidden" value="www.mono-project.com" id="sitesearch" name="sitesearch" />
          <input type="hidden" value="www.mono-project.com" id="domains" name="domains" />
          <input class="text" name="q" id="q" type="text" value="Search Mono" 
            onblur="if (this.value == '') this.value='Search Mono';" 
            onfocus="if (this.value == 'Search Mono') this.value='';" />
          <input class="button" type="submit" value="Go" />
        </div>
      </form>
    </div>
  </div>
    <%--<div id="content-header"><h2><!--BEGIN PAGE TITLE-->Forums<!--END PAGE TITLE--></h2></div>--%>

  <div id="headerbar"></div>
    <div id="wrapper" class="wide">
    <div id="sidebar">
    <div id="toc-parent"></div>
    <!-- BEGIN SIDE CONTENT -->
    
    
    <!-- END SIDE CONTENT -->
    </div>
    <div id="content" class="wide">
    <!-- BEGIN MAIN CONTENT -->

    <form id="form1" runat="server" enctype="multipart/form-data">
        <YAF:Forum runat="server" ID="forum"></YAF:Forum>
    </form>
    
    <!-- END MAIN CONTENT -->
    </div><!--#content-->
    
    <div id="footer">
                    <ul id="footer-menu">
                        <li><a href="http://www.novell.com/linux"><div id="novell-logo"></div></a>
                            <ul>
                                <li style="margin-top: 15px;"><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/">
                                <div id="by-sa"></div></a></li>

                                <li><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/us/">
                                <div id="by-nc-nd"></div></a></li>
                                <li><a href="/Legal">Legal Notices</a></li>
                                <li>          
                           </li>
                            </ul>
                        </li>
                        <li>Mono
                            <ul>

                                <li><a href="/About">About</a></li>
                                <li><a href="/Roadmap">Roadmap</a></li>
                                <li><a href="/Plans">Technologies</a></li>
                                <li><a href="/Screenshots">Screenshots</a></li>
                                <li><a href="/FAQ:_General">FAQ</a></li>
                                <li><a href="/Contact">Contact</a></li>

                            </ul>
                        </li>
                        <li>Download
                          <ul>
                              <li><a href="http://www.go-mono.com/mono-downloads/download.html">Latest Release</a></li>
                              <li><a href="http://mono.ximian.com/daily/">Daily Snapshots</a></li>
                              <li><a href="http://www.mono-project.com/OldReleases">Previous Releases</a></li>
                              <li><a href="http://monodevelop.com/Download">MonoDevelop</a></li>

                              <li><a href="http://www.mono-project.com/MoMA">Mono Migration Analyzer</a></li>
                              <li><a href="http://www.go-mono.com/moonlight/">Moonlight</a></li>
                              <li><a href="http://www.go-mono.com/monovs/download">Mono Tools for Visual Studio</a></li>
                              <li><a href="http://monotouch.net/DownloadTrial">MonoTouch</a></li>
                              <li><a href="http://www.novell.com/products/mono/eval.html">SUSE Linux Enterprise<br/>Edition Mono Extension</a></li>
                          </ul>

                      </li>
                        <li>Documentation
                            <ul>
                                <li><a href="/Start">Getting Started</a></li>
                                <li><a href="http://www.go-mono.com/docs/">API Reference</a></li>
                                <li><a href="/Articles">Articles</a></li>
                            </ul>
                        </li>

                        <li>Community
                            <ul>
                                <li><a href="/Mailing_Lists">Mailing Lists</a></li>
                                <li><a href="http://www.go-mono.com/forums">Forums</a></li>
                                <li><a href="/IRC" class="external">Chat/IRC</a></li>
                                <li><a href="http://www.go-mono.com/monologue">Blogs</a></li>
                            </ul>

                        </li>
                        <li>Contribute
                            <ul>
                                <li><a href="/Contributing">Contributing Guide</a></li>
                                <li><a href="/Bugs">Report Bugs</a></li>
                                <li><a href="/SVN">SVN</a></li>
                                <li><a href="http://mono.ximian.com/monobuild/">Build Status</a></li>

                                <li><a href="http://go-mono.com/status/">Class Status</a></li>

                            </ul>
                        </li>
                    </ul>
                <div style="clear: both;"></div>
    </div>
    
  </div><!--#wrapper-->
</div><!--#page-->
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>

<script type="text/javascript">
try{
var pageTracker = _gat._getTracker("UA-76510-1");
pageTracker._trackPageview();
} catch(err) {}
</script>

</body>
</html>
