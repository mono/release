<%@ Page Title="" Language="C#" MasterPageFile="FeaturePage.master" AutoEventWireup="true"
    CodeFile="Package.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Package for Linux
</asp:Content>

<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
        <h1>Package for Linux</h1>
        <p>
            Once your application successfully runs on Mono on Linux, it's time to package it
            up for distribution.
            </p>
        <br /><h2>Step 1:</h2>
        <p>
            Add a new item to your project.</p>
        <br /><img class="shot" src="img/package1.png" alt="Package for Linux - Step 1" />
        <br /><h2>Step 2:</h2>
        <p>
            Choose "Linux Package Definition".</p>
        <br /><img class="shot" src="img/package2.png" alt="Package for Linux - Step 2" />
        <br /><h2>Step 3:</h2>
        <p>
            On the "General" tab, fill out basic information about your package.</p>
        <br /><img class="shot" src="img/package3.png" alt="Package for Linux - Step 3" />
        <br /><h2>Step 4:</h2>
        <p>
            On the "Files" tab, add the files you wish to include in your package.</p>
        <br /><p class="note">
            Hint: If you are packaging a GUI or Console Application, right click your startup
            executable and choose "Set as Startup Executable". This is the assembly that will
            get launched from your menu item.
        </p>
        <br /><img class="shot" src="img/package4.png" alt="Package for Linux - Step 4" />
        <br /><h2>Step 5:</h2>
        <p>
            On the "Dependencies" tab, you can set what Mono libraries or other packages your
            application depends on. You can also specify what dependencies your application
            provides.</p>
        <br /><p class="note">
            Hint: If you click on the "Refresh" button, your assemblies will be scanned and
            your Mono dependencies will be automatically determined. You can then tweak them
            if you like.</p>
        <br /><img class="shot" src="img/package5.png" alt="Package for Linux - Step 5" />
        <br /><h2>Step 6:</h2>
        <p>
            Once you click "Build Package", your package will be built and ready for you (and
            your users) to install on SUSE Linux.</p>
        <br /><img class="shot" src="img/package6.png" alt="Package for Linux - Step 6" /><br /><br /><br />
    </div>
</asp:Content>
