<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Package.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Package for Linux</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <table style="margin-top: -15px">
            <tr>
                <td style="width: 600px"><a href="Debug.aspx" style="color: #000000;">&lt;-- Debug Remotely on Linux</a></td>
                <td><a href="Studio.aspx" style="color: #000000;">Create a SUSE Linux Appliance --&gt;</a></td>
            </tr>
        </table>
        <br />
        <br />
        <span class="feature-header">Package for Linux</span><br />
        <br />
        Once your application successfully runs on Mono on Linux, it's time to package it up
        for distribution.
        <br />
        <br />
        <br />
        <br />
        <img class="shot" src="Images/package1.png" alt="Package for Linux - Step 1" />
        <b>Step 1:</b><br />
        <br />
        Add a new item to your project.
        <div class="clearer">
        </div>
        <img class="shot" src="Images/package2.png" alt="Package for Linux - Step 2" />
        <b>Step 2:</b><br />
        <br />
        Choose "Linux Package Definition".
        <div class="clearer">
        </div>
        <img class="shot" src="Images/package3.png" alt="Package for Linux - Step 3" />
        <b>Step 3:</b><br />
        <br />
        On the "General" tab, fill out basic information about your package.
        <div class="clearer">
        </div>
        <img class="shot" src="Images/package4.png" alt="Package for Linux - Step 4" />
        <b>Step 4:</b><br />
        <br />
        On the "Files" tab, add the files you wish to include in your package.
        <br />
        <br />
        <br />
        <div class="note" style="width: 380px; margin-left: 380px; background-position: 2px 17px; background-color: #E5ECF3; border-color: #666699;">
            Hint: If you are packaging a GUI or Console Application, right click your startup executable and choose "Set as Startup Executable".  This is the assembly that will get launched from your menu item.
        </div>
        <div class="clearer">
        </div>
        <img class="shot" src="Images/package5.png" alt="Package for Linux - Step 5" />
        <b>Step 5:</b><br />
        <br />
        On the "Dependencies" tab, you can set what Mono libraries or other packages your application depends on.  You can also specify what dependencies your application provides.
         <br />
        <br />
        <br />
        <div class="note" style="width: 380px; margin-left: 380px; background-position: 2px 17px; background-color: #E5ECF3; border-color: #666699;">
            Hint: If you click on the "Refresh" button, your assemblies will be scanned and your Mono dependencies will be automatically determined.
            <br /><br />
            You can then tweak them if you like.
        </div>
       <div class="clearer">
        </div>
        <img class="shot" src="Images/package6.png" alt="Package for Linux - Step 6" />
        <b>Step 6:</b><br />
        <br />
        Once you click "Build Package", your package will be built and ready for you (and your users) to install on SUSE Linux.
        <div class="clearer">
        </div>
    </div>
</asp:Content>
