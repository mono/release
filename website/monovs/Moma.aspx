<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Moma.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Scan with MoMA</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <span class="feature-header">Scan for Mono Compatibility</span><br />
        <br />
        There are some common stumbling blocks that keep .NET applications from being able
        to run on Mono.  These can be due to using parts of the .NET framework that Mono
        does not implement or implements differently, or reliance on native platform 
        code like user32.
        <br /><br />
        The <a href="http://www.mono-project.com/MoMA">Mono Migration Analyzer (MoMA)</a> can scan your compiled assemblies for these types
        of issues and point them out, making it easy to find them and work around them.
        <br /><br /><br />
        <img class="shot" src="Images/moma1.png" alt="Scanning with MoMA - Step 1" />
            <b>Step 1:</b><br />
            <br />
            Open your solution in Visual Studio and ensure it compiles.
        <div class="clearer"></div>
        <img class="shot" src="Images/moma2.png" alt="Scanning with MoMA - Step 2" />
            <b>Step 2:</b><br />
            <br />
            Select the Mono->Scan with MoMA menu item.
        <div class="clearer"></div>
        <img class="shot" src="Images/moma3.png" alt="Scanning with MoMA - Step 3" />
            <b>Step 3:</b><br />
            <br />
            MoMA will scan your application and look for code that may cause issues on Mono.
            These issues will be rated and placed in the Error List.  Clicking them will take
            you to the affected code.<br /><br />
            For details on the types of issues MoMA scans for, and how to fix them, please
            see the <a href="http://www.mono-project.com/MoMA_-_Issue_Descriptions">MoMA User's Guide</a>.
    </div>
</asp:Content>
