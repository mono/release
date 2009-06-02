<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Debug.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Debug on Mono on Linux</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <span class="feature-header">Debug on Mono on Linux</span><br />
        <br />
        Often, the best way to work through an issue will be to debug the application on the target 
        environment.  Debug on Mono on Linux brings this functionality to Visual Studio developers 
        by enabling remote debugging of Mono applications running on Linux.
        <br /><br /><br />
        <img class="shot" src="Images/moma1.png" alt="Debug in Linux - Step 1" />
            <b>Step 1:</b><br />
            <br />
            Open your solution in Visual Studio and ensure it compiles.
        <div class="clearer"></div>
        <img class="shot" src="Images/debug3.png" alt="Debug in Linux - Step 2" />
            <b>Step 2:</b><br />
            <br />
            Set your breakpoints like you would normally do.
        <div class="clearer"></div>
        <img class="shot" src="Images/debug2.png" alt="Debug in Linux - Step 3" />
            <b>Step 3:</b><br />
            <br />
            Select the Mono->Debug Remotely in Mono menu item.
        <div class="clearer"></div>
        <img class="shot" src="Images/testlin3.png" alt="Debug in Linux - Step 4" />
            <b>Step 4:</b><br />
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
        <img class="shot" src="Images/testlin4.jpg" alt="Debug in Linux - Step 5" />
            <b>Step 5:</b><br />
            <br />
            Your application will be compiled, copied over to Linux, and automatically started.  If
            it is a web application, it will be launched in your default Windows web browser.
        <div class="clearer"></div>
        <img class="shot" src="Images/debug4.png" alt="Debug in Linux - Step 6" />
            <b>Step 6:</b><br />
            <br />
            When the application hits the breakpoint, it will stop in Visual Studio, just like normal.
            From here, you can do the normal debug actions, like examine variables and call stacks.
</div>
</asp:Content>
