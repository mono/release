<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial - Run Locally in Mono
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial - Run Locally in Mono</span><br />
       <br />
        
       <a href="images/blog_engine_in_vs.png">
         <img class="shot" src="images/blog_engine_in_vs-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       Open the BlogEngine solution in Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/run_local_menu_item.png">
         <img class="shot" src="images/run_local_menu_item-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
       In the Mono menu, click "Run Locally in Mono".
       <div class="clearer" />
       <br />

       <a href="images/need_to_install_mono_dialog.png">
         <img class="shot" src="images/need_to_install_mono_dialog-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
        If Mono for Windows isn't installed, a dialog message like this will appear. Install Mono for Windows, then proceed.
       <div class="clearer" />
        <br />

       <a href="images/windows_firewall_unblock_dialog.png">
         <img class="shot" src="images/windows_firewall_unblock_dialog-small.png" />
       </a>
       <b>Step 4:</b><br />
       <br />
Windows firewall will display a dialog saying that mono.exe has been blocked from opening a port in the firewall. Click the "Unblock" button.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_running_locally_in_ff.png">
         <img class="shot" src="images/blog_engine_running_locally_in_ff-small.png" />
       </a>
       <b>Step 5:</b><br />
       <br />
BlogEngine will be launched in the default browser.
       <div class="clearer" />
       <br />

       <a href="images/monovs_local_asp.net_tray_app.png">
         <img class="shot" src="images/monovs_local_asp.net_tray_app-small.png" />
       </a>
       <b>Step 6:</b><br />
       <br />
To stop this instance of BlogEngine, right click on the MonoVS tray icon and click "Stop".
       <div class="clearer" />
   </div>
</asp:Content>

