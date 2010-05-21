<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="TestLin.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Run on Mono on Linux</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
<div class="container_12">
    <div class="grid_12">
        <h1>Run on Mono on Linux</h1>

        <p>While running an application on Mono on Windows will help work through any issues arising from 
        differences between Mono and .NET, running the application on Mono on Linux will simplify the 
        process of working through issues that could be caused by differences in Windows and Linux.</p>

    </div>
    <div class="grid_6">
        <h2>Step 1:</h2>
        <p>Open your solution in Visual Studio and ensure it compiles.</p>
        
        <!--<img class="shot" src="img/moma1.png" alt="Testing in Linux - Step 1">-->
        

        <h2>Step 2:</h2>
        
        <p>Select the Mono->Run Remotely in Mono menu item.</p>
        
        <!--<img class="shot" src="img/testlin2.png" alt="Testing in Linux - Step 2">-->

        <h2>Step 3:</h2>

        <p>A dialog box will prompt you to choose from the available servers it found on you local
        network.  If your server doesn't show up, you can manually enter in the IP address and 
        port of the server you wish to use.</p>

        <img class="shot" src="img/testlin3.png" alt="Testing in Linux - Step 3">
    </div>
    <div class="grid_6">
        <h2>Step 4:</h2>

        <p>Your application will be compiled, copied over to Linux, and automatically started.  If
        it is a web application, it will be launched in your default Windows web browser.</p>
        
        <img class="shot" src="img/testlin4.jpg" alt="Testing in Linux - Step 4">
    </div>
    <div class="grid_12">
        <p class="note">
            In order to find servers on the local subnet, UDP is used to broadcast over port <code>1900</code>
            using the multicast address <code>239.255.255.250</code>.  If your server is not appearing, you
            may want to check your firewall settings.            
        </p>
    </div>    
</div>
    
</asp:Content>
