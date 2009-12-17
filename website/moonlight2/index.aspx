<%@ Page Language="C#" MasterPageFile="frame.master" %>
<asp:Content ContentPlaceHolderID="title" Runat="server">Moonlight</asp:Content>

<asp:Content ContentPlaceHolderID="page_heading" Runat="server">
</asp:Content>

<asp:Content ContentPlaceHolderID="splash" Runat="server">
<div id="splash">
  <div class="widthcontainer">
    <div class="twocolumn splashimage">
      <h3 class="tagline">Moonlight.</h3>

      <div id="install-buttons">
        <div id="moonlight-banner">
        Moonshine requires the <a href="http://go-mono.com/moonlight">Moonlight plugin</a>. 
        Before installing Moonshine, please <a href="http://go-mono.com/moonlight/">install Moonlight</a>.
        </div>

        <div id="install-host">
          <p>Moonshine requires Firefox 3.0 or newer and JavaScript to be enabled in your browser. If you are
          seeing this message, it is likely that Moonshine will not run properly.</p>
        </div>
      </div><!--install-buttons-->
      
    </div><!--splashimage-->
    
    <div id="lightcone"></div>
    <h1 id="logo">Moonlight</h1>

    <div class="twocolumn" id="easymultimedia">
      <h2>Rich Internet Applications</h2>
      <p>
         Moonlight is an open source implementation of <a href="http://silverlight.net">Microsoft Silverlight</a> for Unix systems.
      </p>

      <h2 id="youcan">With Moonlight you can:</h2>

      <ul class="intro-list">
        <li><p>View Silverlight content on Linux</p></li>
        <li><p></p></li>
        <li><p></p></li>
      </ul>
    </div>
  </div><!--widthcontainer-->
</div><!--splash-->

<div class="screenshots clear">
  <div>
    <h2>Screenshots</h2>
    <div><a title="Installing Moonlight is a matter of clicking a button." 
      href="images/screenshot-install.png"><img alt="*" src="images/thumbnail-install.png" /></a></div>
    <div><a title="Windows Media Codecs get installed automatically and this only happens once." 
      href="images/screenshot-codecs.png"><img alt="*" src="images/thumbnail-codecs.png" /></a></div>
    <div><a title="Embedded live video stream from CPAN."
      href="images/screenshot-streaming.png"><img alt="*" src="images/thumbnail-streaming.png" /></a></div>    
    <div><a title="You can also install Moonshine as a standalone application to use on the desktop."
      href="images/screenshot-standalone.png"><img alt="*" src="images/thumbnail-standalone.png" /></a></div>
  </div>
</div>
</asp:Content>

<asp:Content ContentPlaceHolderID="main_container" Runat="server">
  <div class="columns">
    <div class="twocolumn">
      <h2>Why?</h2>

      <p>
         A1
      </p>
    </div>
    
    <div class="twocolumn">
      <h2>How?</h2>

      <p>
      <img class="icon" alt="" src="images/plugin.png" />
      How1
      </p>

      <p>
      How2
      </p>

      <p>
        How3
      </p>
    </div><!--twocolumn-->
  </div><!--columns-->

</asp:Content>


