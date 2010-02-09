<%@ Page Language="C#" Src="core.cs" %>
<%@ Import Namespace="System.Net.Mail" %>
<%@ Register TagPrefix="recaptcha" Namespace="Recaptcha" Assembly="Recaptcha" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html dir="ltr" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml" lang="en"><head>

  
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="KEYWORDS" content="IRC/Chat">
<meta name="robots" content="index,follow">
<meta name="verify-v1" content="CdUrKULfeirXCs/Mpc2sobgsPFNoqmiRL/5n0n08dAY="><link rel="shortcut icon" href="http://mono-project.com/favicon.ico">
<link rel="copyright" href="http://www.gnu.org/copyleft/fdl.html">
    <title>Contact - Mono</title>
    <link rel="alternate" type="application/rss+xml" title="RSS" href="http://mono-project.com/news/index.rss2"/>
    <link rel="stylesheet" type="text/css" media="print" href="http://mono-project.com/skins/common/commonPrint.css" />  
    <link rel="stylesheet" type="text/css" href="http://mono-project.com/skins/MonoWaveWide/screen.css" />
    <script type="text/javascript" src="http://mono-project.com/skins/Mono2/prototype.js"></script>
    <script type="text/javascript" src="http://mono-project.com/skins/Mono2/wikihacks.js"></script>
    <script type="text/javascript" src="http://mono-project.com/skins/common/wikibits.js"></script>
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"> </script>
    <script type="text/javascript">
        _uacct = "UA-76510-1";
        urchinTracker();
    </script>
    <link rel="stylesheet" href='MonoForm.css' type="text/css" media="screen" /> 
</head><body class="ns-0">
   
  <div id="header">
		<div class="wrapper">
	    <h1>Mono</h1>    
	    <a href="http://mono-project.com/" title="Mono"><div id="mono-logo"></div></a>
	    <ul>
	    	      <li  id="menu-n-home"><a href="http://mono-project.com/Main_Page">Home</a></li>

		      <li id="menu-n-download"><a href="http://www.go-mono.com/mono-downloads/download.html">Download</a></li>
		      <li id="menu-n-start"><a href="http://mono-project.com/Start">Start</a></li>
		      <li id="menu-n-news"><a href="http://www.mono-project.com/news/">News</a></li>
		      <li id="menu-n-contribute"><a href="http://mono-project.com/Contributing">Contribute</a></li>
		      <li id="menu-n-community"><a href="http://mono-project.com/Community">Community</a></li>
		      <li class="current_page_item" id="menu-n-support"><a href="http://mono-project.com/Support">Support</a></li>
		      <li id="menu-n-store"><a href="http://mono-project.com/Store">Store</a></li>
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
      </div><!--#search-->
    </div><!--.wrapper-->
  </div><!--#header-->


<div id="page">
    <div id="content-header"><h2><!--BEGIN PAGE TITLE-->Contact Mono at Novell<!--END PAGE TITLE--></h2></div>

    <div id="wrapper" class="wide">

    <div id="sidebar">
    <div id="toc-parent"></div>
    <!-- BEGIN SIDE CONTENT -->
    
    
    <!-- END SIDE CONTENT -->
    </div><!--#sidebar-->
    <div id="content" class="wide">
    <!-- BEGIN MAIN CONTENT -->
<script runat="server">
void btnSubmit_OnClick (object o, EventArgs a)
{
   if (!Page.IsValid)
      return;

   SmtpClient c = new SmtpClient ("localhost");
   string from = email.Text;
   string to   = ContactForm.EmailAddress;
   string body = String.Format ("Sender: {0}\nIP: {1}\n\nMessage:\n\n{2}", email.Text, Request.UserHostAddress, msg.Text);
   string subject = String.Format ("{0} from {1}", subjectctl.SelectedItem.Text, email.Text);

   MailMessage mail_message = new MailMessage (from, to, subject, body);
   try {
       mail_message.ReplyTo = new MailAddress (email.Text);
   } catch {}

   c.Send (mail_message);
   Server.Transfer ("thankyou.aspx");
}
   
</script>

<form runat="server">
  <asp:RequiredFieldValidator ControlToValidate="email" ID="rqdEmail" runat="server"  Display="Dynamic" 
    ErrorMessage="Please enter an email address"></asp:RequiredFieldValidator>
  <asp:RegularExpressionValidator ControlToValidate="email" ID="regexEmail" runat="server" Display="Dynamic"
    ErrorMessage="Please enter a valid email address" ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
  <div id="contact-form-container">
 
  <table id="contact-form">
    <tr>
      <th>Email Address:</th>
      <td><asp:TextBox name="email" id="email" runat="server" style="width: 300px"/></td>
    </tr>
    <tr>
      <th>Subject:</th>
      <td>
        <asp:DropDownList ID="subjectctl" runat="server" style="width: 300px">
          <asp:ListItem>General Comment</asp:ListItem>
          <asp:ListItem>Embedded/Gaming Licensing</asp:ListItem>
          <asp:ListItem>Moonlight</asp:ListItem>
          <asp:ListItem>Mono Tools for Visual Studio</asp:ListItem>
          <asp:ListItem>monoTouch</asp:ListItem>
          <asp:ListItem>Problem Report</asp:ListItem>
          <asp:ListItem>Criticism</asp:ListItem>
          <asp:ListItem>Suggestion</asp:ListItem>
          <asp:ListItem>Licensing</asp:ListItem>
          <asp:ListItem>Consulting and Tech Support.</asp:ListItem>
          <asp:ListItem>Security Report</asp:ListItem>
          <asp:ListItem>Web Site Issues</asp:ListItem>
        </asp:DropDownList>
      </td>
    </tr>
    <tr class="message-box">
      <th class="top-align">Message:</th>
      <td><asp:TextBox name="msg" id="msg" TextMode="Multiline" runat="server"/></td>
    </tr>
    <tr>
      <th class="top-align" style="padding-top: 15px">Are you<br/>human?</th>
      <td style="padding-top: 15px">
        <recaptcha:RecaptchaControl
            ID="recaptcha"
            runat="server"
            Theme="clean"
            PublicKey="6LevKgMAAAAAAFBU2BuqpQOkn2fUnJE_PLVTNj0u"
            PrivateKey="6LevKgMAAAAAAI4NimISmjEd4FabHTNLwhTBu4gW" />
	
      </td>
    </tr>
    <tr>
      <th>&nbsp;</th>
      <td style="padding-top: 15px"> 
        <asp:Button Text="Send Inquiry" runat="server" ID="btnSubmit" OnClick="btnSubmit_OnClick" />
        <asp:Label id="report" runat="server"/>
      </td>
    </tr>
  </table>
  </div>
</form>

    <!-- END MAIN CONTENT -->

    </div><!--#content-->
    

    
  </div><!--#wrapper-->
</div><!--#page-->
<div id="footer-hr"></div>
<div id="footer">
                <ul id="footer-menu">
                    <li><a href="http://www.novell.com/linux"><div id="novell-logo"></div></a>
                        <ul>
                            <li style="margin-top: 15px;"><a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/us/">
                            <div id="by-sa"></div></a></li>

                            <li><a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/us/">
                            <div id="by-nc-nd"></div></a></li>
                            <li><a href="http://mono-project.com/Legal">Legal Notices</a></li>
                            <li>          
<a href="http://mono-project.com/index.php?title=Special:Userlogin&amp;returnto=Contributing">Editor Login</a>                        </li>
                        </ul>
                    </li>
                    <li>Mono
                        <ul>

                            <li><a href="http://mono-project.com/About">About</a></li>
                            <li><a href="http://mono-project.com/Roadmap">Roadmap</a></li>
                            <li><a href="http://mono-project.com/Plans">Technologies</a></li>
                            <li><a href="http://mono-project.com/Screenshots">Screenshots</a></li>
                            <li><a href="http://mono-project.com/FAQ:_General">FAQ</a></li>
                            <li><a href="http://mono-project.com/Contact">Contact</a></li>

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
                            <li><a href="http://mono-project.com/Start">Getting Started</a></li>
                            <li><a href="http://www.go-mono.com/docs/">API Reference</a></li>
                            <li><a href="http://mono-project.com/Articles">Articles</a></li>
                        </ul>
                    </li>

                    <li>Community
                        <ul>
                            <li><a href="http://mono-project.com/Mailing_Lists">Mailing Lists</a></li>
                            <li><a href="http://www.go-mono.com/forums">Forums</a></li>
                            <li><a href="http://mono-project.com/IRC" class="external">Chat/IRC</a></li>
                            <li><a href="http://www.go-mono.com/monologue">Blogs</a></li>
                        </ul>

                    </li>
                    <li>Contribute
                        <ul>
                            <li><a href="http://mono-project.com/Contributing">Contributing Guide</a></li>
                            <li><a href="http://mono-project.com/Bugs">Report Bugs</a></li>
                            <li><a href="http://mono-project.com/SVN">SVN</a></li>
                            <li><a href="http://wrench.mono-project.com/builds">Build Status</a></li>

                            <li><a href="http://go-mono.com/status/">Class Status</a></li>

                        </ul>
                    </li>
                </ul>
            <div style="clear: both;"></div>
</div>


</body>
</html>