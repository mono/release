<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="TestLin.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Run on Mono on Linux</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <table style="margin-top: -15px">
            <tr>
                <td style="width: 625px"><a href="TestWin.aspx" style="color: #000000;">&lt;-- Run on Mono on Windows</a></td>
                <td><a href="Debug.aspx" style="color: #000000;">Debug Remotely on Linux --&gt;</a></td>
            </tr>
        </table>
        <br />
        <br />
        <span class="feature-header">Run on Mono on Linux</span><br />
        <br />
        When porting your application to run on Mono on Linux, there are two types of issues
        that can occur: differences between Mono and .NET and differences between Windows and Linux.
        <br /><br />
        While running an application on Mono on Windows will help work through any issues arising from 
        differences between Mono and .NET, running the application on Mono on Linux will simplify the 
        process of working through issues that could be caused by differences in Windows and Linux.
        <br /><br /><br />
        <img class="shot" src="img/moma1.png" alt="Testing in Linux - Step 1" />
            <b>Step 1:</b><br />
            <br />
            Open your solution in Visual Studio and ensure it compiles.
        <div class="clearer"></div>
        <img class="shot" src="img/testlin2.png" alt="Testing in Linux - Step 2" />
            <b>Step 2:</b><br />
            <br />
            Select the Mono->Run Remotely in Mono menu item.
        <div class="clearer"></div>
        <img class="shot" src="img/testlin3.png" alt="Testing in Linux - Step 3" />
            <b>Step 3:</b><br />
            <br />
            A dialog box will prompt you to choose from the available servers it found on you local
            network.  If your server doesn't show up, you can manually enter in the IP address and 
            port of the server you wish to use.
            <br /><br /><br />
            <div class="note" style="width: 380px; margin-left: 380px; background-position: 2px 17px;">
                In order to find servers on the local subnet, UDP is used to broadcast over port 1900
                using the multicast address 239.255.255.250.  If your server is not appearing, you
                may want to check your firewall settings.            
            </div>
        <div class="clearer"></div>
        <img class="shot" src="img/testlin4.jpg" alt="Testing in Linux - Step 4" />
            <b>Step 4:</b><br />
            <br />
            Your application will be compiled, copied over to Linux, and automatically started.  If
            it is a web application, it will be launched in your default Windows web browser.
   </div>
</asp:Content>
