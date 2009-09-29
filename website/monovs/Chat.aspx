<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true"
    CodeFile="Chat.aspx.cs" Inherits="Survey" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
    Live chat (IRC) for Mono Tools for Visual Studio.  For channel details to run in your own IRC client, <a href="http://mono-project.com/IRC_MonoVS">click here</a>.
    <iframe id="irc" scrolling="no" src="http://embed.mibbit.com/index.html?server=irc.gnome.org&channel=%23monovs"></iframe>
    </div>
</asp:Content>
