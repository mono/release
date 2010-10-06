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
                        <li>About
                <ul>
                    <li><a title="Features" href="http://monotouch.net/Features">Features</a></li>
                    <li><a title="FAQ" href="http://monotouch.net/FAQ">FAQ</a></li>

                    <li><a class=" external" href="http://mono-project.com/About">About Mono</a></li>
                    <li><a title="Contact" href="http://monotouch.net/Contact">Contact</a></li>
                </ul>

                        </li>
                        <li>Documentation
                          <ul>
                                                  <li><a title="Documentation" href="http://monotouch.net/Documentation">Documentation</a></li>
                    <li><a title="Documentation/Installation" href="http://monotouch.net/Documentation/Installation">Installation&nbsp;Instructions</a></li>
                    <li><a title="Documentation/API" href="http://monotouch.net/Documentation/API">API</a></li>
                    <li><a title="Documentation/Samples" href="http://monotouch.net/Documentation/Samples">Samples</a></li>
                    <li><a title="Tutorials" href="http://monotouch.net/Tutorials">Tutorials</a></li>
                    <li><a class=" external" href="http://wiki.monotouch.net/HowTo">HowTo&nbsp;Wiki</a></li>

                </ul>

                      </li>
                        <li>Downloads
                            <ul>
                                <li><a title="DownloadTrial" href="http://monotouch.net/DownloadTrial">Download Trial</a></li>
                    <li><a class=" external" href="http://mono-project.com/Downloads">Download Mono</a></li>

                    <li><a class=" external" href="http://monodevelop.com/Download/Mac_MonoTouch">Download&nbsp;MonoDevelop</a></li>
                </ul>
                        </li>

                        <li>Community
                            <ul>
                                <li><a title="Community" href="http://monotouch.net/Community">Community</a></li>

                    <li><a class=" external" href="http://wiki.monotouch.net/">Wiki</a></li>
                    <li><a class=" external" href="http://lists.ximian.com/mailman/listinfo/monotouch">Mailing&nbsp;List</a></li>
                    <li><a title="Chat" href="http://monotouch.net/Chat">Chat</a></li>
                </ul>
                        </li>
                    </ul>
                <div style="clear: both;"></div><div id="footer-logo"><a href="http://www.novell.com/linux"><div id="novell-logo"></div></a></div>
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
