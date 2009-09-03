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
        <a href="Moma.aspx"><img src="Images/moma64.png" alt="Scan with MoMA" width="64" height="64" /></a>
        <p>
            <a href="Moma.aspx" class="title">Scan for Mono Compatibility</a><br />
            Scan your application with the Mono Migration Analyzer (MoMA) directly in Visual
            Studio.&nbsp;&nbsp;&nbsp;<a href="Moma.aspx" class="more">more...</a><br />
        </p>
        <a href="TestWin.aspx"><img src="Images/monowin.png" alt="Test on Windows" width="64" height="64" /></a>
        <p>
            <a href="TestWin.aspx" class="title">Test on Windows</a><br />
            Compile and launch your application running in Mono on Windows.&nbsp;&nbsp;&nbsp;<a
                href="TestWin.aspx" class="more">more...</a><br />
        </p>
        <a href="TestLin.aspx"><img src="Images/monolinux.png" alt="Test on Linux" width="64" height="64" /></a>
        <p>
           <a href="TestLin.aspx" class="title">Test on Linux</a><br />
            Automatically compile your application and launch it on your Linux PC or virtual
            image.&nbsp;&nbsp;&nbsp;<a href="TestLin.aspx" class="more">more...</a><br />
        </p>
        <a href="Debug.aspx"><img src="Images/start.png" alt="Debug on Linux" width="58" height="58" /></a>
        <p>
            <a href="Debug.aspx" class="title">Debug Remotely on Linux</a><br />
            Debug your application running on Mono on Linux directly in Visual Studio, just like you
            normally do.&nbsp;&nbsp;&nbsp;<a href="Debug.aspx" class="more">more...</a><br />
        </p>
        <a href="Package.aspx"><img src="Images/packaging.png" alt="Package for Linux" width="58" height="58" /></a>
        <p>
            <a href="Package.aspx" class="title">Package for Linux</a><br />
            Visually create a SUSE RPM installer package for your application.&nbsp;&nbsp;&nbsp;<a href="Package.aspx" class="more">more...</a><br />
        </p>
        <a href="Studio.aspx"><img src="Images/studio.png" alt="Create a SUSE Linux Appliance" width="58" height="58" /></a>
        <p>
            <a href="Studio.aspx" class="title">Create a SUSE Linux Appliance</a><br />
            Bundle your application into a SUSE Linux appliance for easy distribution to your users.&nbsp;&nbsp;&nbsp;<a href="Studio.aspx" class="more">more...</a><br />
        </p>
    </div>
    <div class="right-column">
    <div class="surveydiv">
        Mono Tools for Visual Studio is currently in private preview.
        <br /><br />Sign up to be included in the next round of invitations!
        <br /><br /><a href="Signup.aspx"><img src="Images/signup-button.png" alt="Click to Signup" /></a>
    </div>
        <div class="colordiv">
            <span style="font-size: .85em;">Already received your invitation username/password?<br />
            <br />
            <a href="http://go-mono.com/monovs-download/latest/">Download current version: Beta 1 (0.3.3771)</a></span>
            <br />
            <br />
            <table style="margin-left: 32px;">
                <tr>
                    <td><a href="http://www.mono-project.com/GettingStartedWithMonoVS"><img src="Images/report.png" alt="Installation Guide" /></a></td>
                    <td style="font-size: .85em;"><a href="http://www.mono-project.com/GettingStartedWithMonoVS"> Installation Guide</a></td>
                    <td style="font-size: .85em;"> | </td>
                    <td><a href="http://mono-project.com/FAQ:_MonoVS"><img src="Images/help.png" alt="Frequently Asked Questions" /></a></td>
                    <td style="font-size: .85em;"><a href="http://mono-project.com/FAQ:_MonoVS"> FAQ</a></td>
                    <td style="font-size: .85em;"> | </td>
                    <td><a href="http://mono-project.com/Bugs"><img src="Images/bug.png" alt="File a bug" /></a></td>
                    <td style="font-size: .85em;"><a href="http://mono-project.com/Bugs"> Report Bugs</a></td>
                </tr>
            </table>
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
        - VMWare (vmx / ova) or
        <br />
        - Virtual PC (vpc)    
        <br />
        <br />
<span style="color: #FF0000;font-size: .85em;">Note: All instances of Visual Studio 2008 must be closed prior to installation.</span> </div>
</asp:Content>
