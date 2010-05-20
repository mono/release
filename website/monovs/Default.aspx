<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server"></asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">

    <div id="splash">
        <div class="container_12">
            <div class="grid_6" id="logo">
                <img alt="MonoTools for Visual Studio" src="/img/logo.png">
                <a href="#" class="download button"><span></span>Download</a>
                <p>Mono tools for Visual Studio 1.1<br>
                Download the free 30-day trial.</p>
                <p class="buynow">Or <a href="#">Buy now</a>.</p>
            </div>
            <div class="grid_6">
                <h1>Port your .NET applications to Mono and Linux without leaving Visual Studio</h1>
                <p>Mono Tools for Visual Studio is a commercial add-in for Microsoft™ Visual Studio™ that enables developers to write .NET applications for non-Windows platforms within their preferred development environment.</p>

                <p>It allows developers to build, debug and deploy .NET applications on Linux, while continuing to leverage the extensive ecosystem of code, libraries, and tools available for .NET.</p>
            </div>
        </div>
    </div>

    <div id="features">
        <div>
            <div class="container_12">
                <div class="grid_6 feature" id="feature-scan">
                    <h2><a href="#">Scan for Mono Compatibility</a></h2>
                    <p>Scan your application with the Mono Migration Analyzer (MoMA) directly in Visual Studio.</p>
                </div>
                <div class="grid_6 feature" id="feature-windows">
                    <h2><a href="#">Test on Windows</a></h2>
                    <p>Compile and launch your application running in Mono on Windows.</p>
                </div>
                <div class="grid_6 feature clear" id="feature-linux">
                    <h2><a href="#">Test on Linux</a></h2>
                    <p>Automatically compile your application and launch it on your Linux PC or virtual image.</p>
                </div>
                <div class="grid_6 feature" id="feature-debug">
                    <h2><a href="#">Debug Remotely on Linux</a></h2>
                    <p>Debug your application running on Mono on Linux directly in Visual Studio, just like you normally do.</p>
                </div>
                <div class="grid_6 feature clear" id="feature-package">
                    <h2><a href="#">Package for Linux</a></h2>
                    <p>Automatically compile your application and launch it on your Linux PC or virtual image.</p>
                </div>
                <div class="grid_6 feature" id="feature-studio">
                    <h2><a href="#">Create a SUSE Linux Appliance</a></h2>
                    <p>Bundle your application into a SUSE Linux appliance for easy distribution to your users. </p>
                </div>                                
            </div>
        </div>
    </div>

    <div class="container_12 clearfix">
        <h2>Requirements</h2>
        <div class="grid_6">
            <ul class="block">
                <li>Windows XP, Vista or 7 (32 or 64bit versions)</li>
                <li>Visual Studio 2008 SP1 or Visual Studio 2010*</li>
            </ul>
        </div>
        <div class="grid_6">
            <p>Linux Image runs in:</p>
            <ul class="block">
                <li>VMWare (VMX/OVA) or</li>
                <li>Virtual PC (VPC)</li>
            </ul>
            <p class="small">* Excludes Visual Studio Express editions.</p>
        </div>
    </div>

</asp:Content>
