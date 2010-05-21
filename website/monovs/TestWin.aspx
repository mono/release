<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="TestWin.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Run on Mono on Windows</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
  <div class="container_12">
    <div class="grid_12">
        <h1>Run on Mono on Windows</h1>
        <p>
        When porting your application to run on Mono on Linux, there are two types of issues
        that can occur: differences between Mono and .NET and differences between Windows and Linux.
        </p><p>
        One way to make this easier is to use two steps.  During the first step, use Mono
        on Windows to work out any issues arising from differences between Mono and .NET.  After
        your application works on Mono, then focus on porting it to Mono on Linux.
        </p>
        <p class="note">
            In order for this feature to work, you will need to install Mono for Windows,
            available from the Mono download page <a href="http://www.go-mono.com/mono-downloads/download.html">here</a>.
        </p>
    </div>
    <div class="grid_6">
        
        <h2>Step 1:</h2>
        <p>Open your solution in Visual Studio and ensure it compiles.</p>
        <!--<img class="shot" src="img/moma1.png" alt="Testing in Windows - Step 1">-->

        <h2>Step 2:</h2>
        <p>Select the Mono->Run Locally in Mono menu item.</p>
        <img class="shot" src="img/testwin2.png" alt="Testing in Windows - Step 2">
        
     </div>
     <div class="grid_6">
        <h2>Step 3:</h2>
        <p>The application will be compiled and launched using Mono on Windows, so
        you can try it out on Mono.</p>
        <img class="shot" src="img/testwin3.png" alt="Testing in Windows - Step 3" />
        
     </div>
   </div>
</asp:Content>
