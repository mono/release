<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial - Analyze for Mono Migration
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial - Analyze for Mono Migration</span><br />
       <br />
        
       <a href="images/blog_engine_in_vs.png">
         <img class="shot" src="images/blog_engine_in_vs-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       Open the BlogEngine solution in Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/moma_menu_item.png">
         <img class="shot" src="images/moma_menu_item-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
       In the Mono menu, click "Analyze for Mono Migration (MoMA)".
       <div class="clearer" />
       <br />

       <a href="images/moma_results.png">
         <img class="shot" src="images/moma_results-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
       MoMA will scan BlogEngine and look for code that may cause issues on Mono. These issues will be rated and placed in the Errors, Warnings and Messages Lists. Clicking them will cause Visual Studio to jump to the affected code.
       <br />
       <br />
       For details on the types of issues MoMA scans for, and how to fix them, please see the <a href="http://www.mono-project.com/MoMA_-_Issue_Descriptions">MoMA User's Guide</a>.
       <div class="clearer" />
    </div>
</asp:Content>

