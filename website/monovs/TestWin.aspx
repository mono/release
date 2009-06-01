<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="TestWin.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Run on Mono on Windows</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <span class="feature-header">Run on Mono on Windows</span><br />
        <br />
        When porting your application to run on Mono on Linux, there are two types of issues
        that can occur: differences between Mono and .Net and differences between Windows and Linux.
        <br /><br />
        One way to make this easier is to use two steps.  During the first step, use Mono
        on Windows to work out any issues arising from differences between Mono and .Net.  After
        you application works on Mono, then focus on porting it to Mono on Linux.
        <br /><br />
        <div class="note">
            In order for this feature to work, you will need to install Mono for Windows,
            available from the Mono download page <a href="http://www.go-mono.com/mono-downloads/download.html">here</a>.
        </div>
        <br /><br />
        <img class="shot" src="Images/moma1.png" alt="Testing in Windows - Step 1" />
            <b>Step 1:</b><br />
            <br />
            Open your solution in Visual Studio and ensure it compiles.
        <div class="clearer"></div>
        <img class="shot" src="Images/testwin2.png" alt="Testing in Windows - Step 2" />
            <b>Step 2:</b><br />
            <br />
            Select the Mono->Run Locally in Mono menu item.
        <div class="clearer"></div>
        <img class="shot" src="Images/testwin3.png" alt="Testing in Windows - Step 3" />
            <b>Step 3:</b><br />
            <br />
            The application will be compiled and launched using Mono on Windows, so
            you can try it out on Mono.
    </div>
</asp:Content>
