<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial</span><br />
       <br />
        
        <h5>This tutorial assumes the following is present on the system:</h5>
<ul>
<li>Visual Studio 2008 SP1 Installed</li>
<li>Mono Plugin for Visual Studio installed. Get it <a href='http://www.go-mono.com/monovs/'>here</a>.</li>
<li>BlogEngine.Net Source Code. Get it <a href='http://blogengine.codeplex.com/Release/ProjectReleases.aspx?ReleaseId=26080'>here</a>.</li>
</ul>

<table>
<tr>
<td width="75px">
<img src="images/moma64.png"/>
</td>
<td>
<a href="./moma/"><strong>Analyze for Mono Migration</strong></a>
</td>
</tr>

<tr>
<td>
<img src="images/monowin.png"/>
</td>
<td>
<a href="./run_local/"><strong>Run Locally in Mono</strong></a>
</td>
</tr>

<tr>
<td>
<img src="images/monolinux.png"/>
</td>
<td>
<a href="./run_remote/"><strong>Run Remotely in Mono</strong></a>
</td>
</tr>

<tr>
<td>
<img src="images/start.png"/>
</td>
<td>
<a href="./debug_remote/"><strong>Debug Remotely in Mono</strong></a>
</td>
</tr>

<tr>
<td>
<img src="images/packaging.png"/>
</td>
<td>
<a href="./create_rpm/"><strong>Create Linux Package for Project</strong></a>
</td>
</tr>

<tr>
<td>
<img src="images/studio.png"/>
</td>
<td>
<a href="./create_appliance/"><strong>Create SUSE Powered Appliance</strong></a>
</td>
</tr>

</table>
    </div>
</asp:Content>

