<%@ Page Language="C#" MasterPageFile="frame.master" %>
<asp:Content ContentPlaceHolderID="title" Runat="server">Moonlight - IRC Chat</asp:Content>

<asp:Content ContentPlaceHolderID="page_heading" Runat="server">
<h1>Moonlight IRC Chat</h1>
</asp:Content>

<asp:Content ContentPlaceHolderID="main_container" Runat="server">
<iframe width="100%" scrolling="no" height="400px" src="http://embed.mibbit.com/index.html?server=irc.gnome.org&amp;channel=%23moonlight" id="irc"> </iframe></p>

      <p>If you prefer, you can use a desktop IRC client, here are some popular clients:</p>
      <ul>
          <li>MacOS X: <a class="external" title="http://www.colloquy.info" rel="nofollow" href="http://www.colloquy.info/">Colloquy</a></li>
          <li>Linux: <a class="external" title="http://www.xchat.org/" rel="nofollow" href="http://www.xchat.org/">XChat</a></li>
          <li>Windows: <a class="external" title="http://www.mirc.com" rel="nofollow" href="http://www.mirc.com/">mIRC</a></li>
          <li>Cross-Platform (using GNOME) build on Mono: <a class="external" title="http://www.smuxi.org/" rel="nofollow" href="http://www.smuxi.org/">Smuxi</a></li>
      </ul>
      </p>

</asp:Content>