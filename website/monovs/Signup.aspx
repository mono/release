<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true"
    CodeFile="Signup.aspx.cs" Inherits="Survey" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
<script type="text/javascript">
  function resizeIframe() {
    var height = document.documentElement.clientHeight;
    height -= document.getElementById('survey').offsetTop;
    height -= 130;
    document.getElementById('survey').style.height = height +"px";
  };
  window.onload = resizeIframe;
  window.onresize = resizeIframe;
</script>
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <iframe id="survey" style="padding: 20px" src="http://spreadsheets.google.com/embeddedform?key=rbEAMJjF84u6T32DVmwgqdg"
        width="810" height="1850" frameborder="0" marginheight="0" marginwidth="0">Loading...</iframe>
</asp:Content>
