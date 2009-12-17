<%@ Page Language="C#" MasterPageFile="frame.master" %>
<asp:Content ContentPlaceHolderID="title" Runat="server">Moonlight</asp:Content>

<asp:Content ContentPlaceHolderID="page_heading" Runat="server">
</asp:Content>

<asp:Content ContentPlaceHolderID="splash" Runat="server">
<div id="splash">
  <div id="stars"></div>
  <div class="widthcontainer">
    <div id="clouds"></div>
    <div class="columns" id="overlay">  
      <div class="twocolumn">
        <h1 id="logo">Moonlight</h1>        
        <h3 class="tagline">Silverlight for Linux: a free plug-in.</h3>
        <h4 class="tagline">Bringing a new level of interactivity wherever the Web works.</h4>

        <div id="install-buttons">
          <div id="moonlight-banner">
          </div>

          <div id="install-host">
          </div>
        </div><!--install-buttons-->
      </div>  

      <div id="infocolumn" class="twocolumn">
        <h2>Rich Internet Applications</h2>
        <p>

           Moonlight is an open source implementation of <a
           href="http://silverlight.net">Microsoft Silverlight</a> for
           Unix systems.  With Moonlight you can access videos,
           applications and content created for Silverlight on Linux.

        </p>

        <h2 id="youcan">With Moonlight you can:</h2>

        <ul class="intro-list">
          <li><p>View Silverlight content on Linux</p></li>
          <li><p>Watch videos delivered with Smoothstreaming</p></li>
          <li><p>Run Silverlight applications on Linux</p></li>
        </ul>
      </div><!--infocolumn-->
    </div><!--columns-->
  </div><!--widthcontainer-->
</div><!--splash-->

<div class="screenshots clear">
  <div>
    <h2>Screenshots</h2>
    <div><a title="Installing Moonlight is a matter of clicking a button." rel="scr"
      href="images/screenshot-install.png"><img alt="*" src="images/thumbnail-install.png" /></a></div>
    <div><a title="Windows Media Codecs get installed automatically and this only happens once."  rel="scr"
      href="images/screenshot-codecs.png"><img alt="*" src="images/thumbnail-codecs.png" /></a></div>
    <div><a title="QuakeLight running in Moonlight." rel="scr"
      href="images/screenshot-quakelight.png"><img alt="*" src="images/thumbnail-quakelight.png" /></a></div>    
    <div><a title="Smooth Streaming in Moonlight." rel="scr"
      href="images/screenshot-streaming.png"><img alt="*" src="images/thumbnail-streaming.png" /></a></div>
  </div>
</div>
</asp:Content>

<asp:Content ContentPlaceHolderID="main_container" Runat="server">
  <div class="columns">
    <div class="twocolumn">
      <h2>What is Moonlight?</h2>

      <p>

	Moonlight was built by Novell in collaboration with Microsoft
	which provided Novell with test suites, specifications, open
	source code and Media Codecs to create an entirely open
	sourced Silverlight-compatible implementation for Unix
	systems.

      </p>

      <p>

	Access to licensed Media Codecs (MP3, WMV, VC-1) is provided
	by Microsoft to Moonlight 1.0 and 2.0 users.  The first time
	that you access a web site that requires these codecs,
	Moonlight will prompt you to download the codecs from
	Microsoft and install those on your system. 

      </p>

    </div>
    
    <div class="twocolumn">
      <h2>Developing Moonlight/Silverlight Applications</h2>

      <p>
      <img class="icon" alt="" src="images/plugin.png" />

      You can develop Silverlight/Moonlight applications using both
      the tools available on Windows or in Linux and MacOS you can use
      the <a href="http://monodevelop.com">MonoDevelop</a> Integrated
      Development Environment.

      </p>

    </div><!--twocolumn-->
  </div><!--columns-->

</asp:Content>


