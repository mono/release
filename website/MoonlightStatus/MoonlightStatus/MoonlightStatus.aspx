<%@ Page Language="C#" Inherits="MoonlightStatus.MoonlightStatus" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
<title>Moonlight 1.0 Test Sites</title>
    <link type="text/css" rel="stylesheet" href="style.css">
<link type="text/css" rel="stylesheet" href="http://mono-project.com/skins/monoproject/main.css">
    <link type="text/css" rel="stylesheet" href="http://mono-project.com/skins/monoproject/niftycorners.css">
    <link type="text/css" rel="stylesheet" href="css/tooltip.css">

<script type="text/javascript" src="js/tooltip.js">

</script>

</head>
<body >
<div id="globalWrapper">
        <div id="bigWrapper">
            <div class="portlet" id="p-logo">
                <a href="http://www.mono-project.com/Main_Page" title="Main Page"></a>
            </div>
            <div class="portlet" id="p-nav">
                <h5>Navigation</h5>
                <div class="pBody">
                    <ul>
                        <li><a href="http://www.mono-project.com/Start">Start</a></li>
                        <li><a href="http://www.mono-project.com/Contributing">Contribute</a></li>
                        <li><a href="http://www.mono-project.com/Need_Help">Need Help</a></li>
                    </ul>
                </div>
            </div>
            <div id="column-content">
                <div id="content">
                                        <div id="bodyContent">
                                <!--  BEGIN CONTENT -->

                <form id="form1" runat="server">

                        <div id="MoonContent" runat="server">

                        </div>
                </form>


                                <!--  END CONTENT -->
                                        </div>
                </div>
            </div>
        </div>
    </div>

<div id="quicklinks">
        <h3>Quick Links</h3>
        <ul>
            <li id="q-screenshots"><a href="http://www.mono-project.com/Screenshots">Screenshots</a></li>
            <li id="q-downloads"><a href="http://www.mono-project.com/Downloads">Downloads</a></li>
            <li id="q-docs"><a href="http://www.go-mono.com/docs/">Manuals &amp; Docs</a></li>
            <li id="q-blogs"><a href="http://www.go-mono.com/monologue/">Blogs</a></li>
        </ul>
    </div>

<div id="footer">

    <div id="p-search" class="portlet">
        <div class="pBody">
            <div class="split-half">
            <!-- SiteSearch Google -->
            <FORM method=GET action="http://www.google.com/search">
                <input type=hidden name=ie value=UTF-8>
                <input type=hidden name=oe value=UTF-8>
                <TABLE bgcolor="#FFFFFF"><tr><td>
                    <A HREF="http://www.google.com/"><IMG SRC="http://www.google.com/logos/Logo_40wht.gif"
                    border="0" ALT="Google"></A>
                    </td>
                    <td>
                    <INPUT TYPE=text name=q size=31 maxlength=255 value="">
                    <INPUT type=submit name=btnG VALUE="Google Search">
                    <font size=-1>
                    <input type=hidden name=domains value="www.mono-project.com"><br><input type=radio name=sitesearch value=""> WWW <input
 type=radio name=sitesearch value="www.mono-project.com" checked> www.mono-project.com <br>
                    </font>
                    </td></tr></TABLE>
            </FORM>

        <!-- SiteSearch Google -->
            </div>
            <div class="split-half">
                <form name="searchform" action="http://www.mono-project.com/Special:Search" id="searchform">
            <!--<label for="searchInput">Search</label>-->
                <input id="searchInput" name="search" type="text"
                    accesskey="f" value="" />

                <input type='submit' name="go" class="searchButton" id="searchGoButton" value="Search" />
                      <!--
                    <input type='submit' name="fulltext"
              class="searchButton"
              value="Search" />
                    -->
                </form>
            </div>
        </div>
        <br style="clear:both;" />
    </div> <!-- div p-search -->

<div id="f-copyrightico">
        <a href="http://www.gnu.org/copyleft/fdl.html"><img src="/skins/common/images/gnu-fdl.png" alt='GNU Free Documentation License 1.2 (only text)' /></a>
    </div>
    <div id="f-list">
        <div id="f-copyright">Content is available under
            <a href="http://www.gnu.org/copyleft/fdl.html" class='external'
                title="http://www.gnu.org/copyleft/fdl.html"
                rel="nofollow">GNU Free Documentation License 1.2 (only text)</a>.
        </div>
        <div id="f-disclaimer">
            <a href="http://www.mono-project.com/Mono:General_disclaimer" title="Mono:General disclaimer">Disclaimers</a>
        </div>
        <div id="f-about"><a href="http://www.mono-project.com/Mono:About" title="Mono:About">About Mono</a>
        </div>
    </div>

</body>
</html>
