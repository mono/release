<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">Mono Tools for Visual Studio</asp:Content>

<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
    <script type="text/javascript" src="/js/jquery.fancybox.js"></script>
    <link rel="stylesheet" type="text/css" href="css/fancybox.css" />
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">

    <div id="splash">
        <div class="container_12">
            <div class="grid_4" id="logo" style="margin-top: 20px;">
                <img alt="MonoTools for Visual Studio" src="/img/logo.png" />

                <div style="margin: 10px 0 0 23px;">
                    <a href="/download/" class="download button" style="margin-bottom: 15px;"><span></span>Download</a>
                    <p>Mono Tools for Visual Studio 2.0<br />
                    Download the free 30-day trial.</p>
                    <p class="buynow">Or <a href="http://go-mono.com/store/">Buy now</a>.</p>
                </div>
            </div>

            <div class="grid_10" style="width: 625px; margin-left: -50px"><br /><br />
                <h1 style="font-size: 140%;">Port your .NET applications to Mono and Linux without leaving Visual Studio!</h1>
                <p>Mono Tools for Visual Studio is a commercial add-in for Microsoft™ Visual Studio™ that enables developers to write .NET applications for non-Windows platforms within their preferred development environment.</p>

                <p>It allows developers to build, debug and deploy .NET applications on Linux, while continuing to leverage the extensive ecosystem of code, libraries, and tools available for .NET.</p>
                <br /><br />
                <a href="/Moma.aspx"><div class="grid_4 feature" id="feature-scan" style="width: 215px;">
                    <h2>Scan for Mono Compatibility</h2>
                    <p>Scan your application with the Mono Migration Analyzer (MoMA) directly within Visual Studio.</p>
                </div></a>
                <a href="/Debug.aspx"><div class="grid_4 feature" id="feature-debug" style="width: 215px;">
                    <h2>Run and Debug on Mono</h2>
                    <p>Launch your application locally, or remotely on Linux or Mac OS X, with <b>full Visual Studio debugging support</b>.</p>
                </div></a>                <div class="clear"></div><br /><br />

                 <a href="/Package.aspx"><div class="grid_4 feature clear" id="feature-package" style="width: 215px;">
                    <h2>Package for Linux</h2>
                    <p>Create an RPM based package for simple distribution to Linux computers.</p>
                </div></a>
                <a href="/Studio.aspx"><div class="grid_4 feature" id="feature-studio" style="width: 215px;">
                    <h2>Create a Linux Appliance</h2>
                    <p>Bundle your application into a SUSE Linux appliance for easy distribution to your users. </p>
                </div>                        </a>        
                <div class="clear"></div><br />
                <div class="tip clear" style="display:none">
                    <h2>Not sure where to start?</h2>
                    <p>Follow our <a href="http://www.go-mono.com/monotools/guides/blog_engine_round_trip/Default.aspx"><strong>tutorial</strong></a> to see an open source ASP.NET application (<a href="http://www.dotnetblogengine.net/">BlogEngine.NET</a>) converted from start to finish! </p>
                </div>
            </div>
        </div>
    </div>
</asp:Content>
