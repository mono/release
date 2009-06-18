<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div id="banner">
        <img src="Images/port2.png" alt="Port your applications to Mono and Linux without leaving Visual Studio!" /></div>
    <div class="left-column">
        <span class="features">Features:</span><br />
        <img src="Images/moma64.png" alt="Scan with MoMA" width="64" height="64" />
        <p>
            <a href="Moma.aspx"><span class="title">Scan for Mono Compatibility</span></a><br />
            Scan your application with the Mono Migration Analyzer (MoMA) directly in Visual
            Studio.&nbsp;&nbsp;&nbsp;<a href="Moma.aspx" class="more">more...</a><br />
        </p>
        <img src="Images/monowin.png" alt="Test on Windows" width="64" height="64" />
        <p>
            <a
                href="TestWin.aspx"><span class="title">Test on Windows</span></a><br />
            Compile and launch your application running in Mono on Windows.&nbsp;&nbsp;&nbsp;<a
                href="TestWin.aspx" class="more">more...</a><br />
        </p>
        <img src="Images/monolinux.png" alt="Test on Linux" width="64" height="64" />
        <p>
           <a href="TestLin.aspx"><span class="title">Test on Linux</span></a><br />
            Automatically compile your application and launch it on your Linux PC or virtual
            image.&nbsp;&nbsp;&nbsp;<a href="TestLin.aspx" class="more">more...</a><br />
        </p>
        <img src="Images/start.png" alt="Debug on Linux" width="58" height="58" />
        <p>
            <a href="Debug.aspx"><span class="title">Debug Remotely on Linux</span></a><br />
            Debug your application running on Mono on Linux directly in Visual Studio, just like you
            normally do.&nbsp;&nbsp;&nbsp;<a href="Debug.aspx" class="more">more...</a><br />
        </p>
    </div>
    <div class="right-column">
    <div class="surveydiv">
        Mono Tools for Visual Studio is currently in private preview.
        <br /><br />Sign up to be included in the next round of invitations!
        <br /><br /><a href="Signup.aspx"><img src="Images/signup-button.png" /></a>
    </div>
        <div class="colordiv">
            <span style="font-size: .85em;">Already received your invitation username/password?<br />
            <br />
            <a href="http://go-mono.com/monovs-download/0.1/">Download current version: 0.1.1866</a></span>
        </div>
        <br />
        <br />
        <b>Requirements:</b><br />
        -
        Windows XP or Vista, 32 or 64 bits<br />
        -
        Visual Studio 2008 Standard or Professional<br />
        <br />
        
        Linux Image runs in:<br />
        - VMWare (.vmx) or
        <br />
        - Virtual PC (.vpc)    
        <br />
        <br />
<span style="color: #FF0000;font-size: .85em;">Note: All instances of Visual Studio 2008 must be closed prior to installation.</span> </div>
</asp:Content>
