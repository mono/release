<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
openSUSE Install Guide
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">openSUSE Install Guide</span><br />
       <br />
        
       <a href="images/opensuse_computer_menu.png">
         <img class="shot" src="images/opensuse_computer_menu-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       In openSUSE click on the "Computer" menu and then on "More Applications."
       <div class="clearer" />
       <br />
       
       <a href="images/app_browser-gnome-terminal.png">
         <img class="shot" src="images/app_browser-gnome-terminal-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
       In the Application Browser, click on the "System" group and then on "GNOME Terminal."
       <div class="clearer" />
       <br />
       
       <a href="images/gt_login_as_root.png">
         <img class="shot" src="images/gt_login_as_root-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
       Login as root by typing:<br />
       <strong>su -</strong><br /><br />
       And then typing the root password.
       <div class="clearer" />
       <br />
       
       <a href="images/gt_zypper_add_repo.png">
         <img class="shot" src="images/gt_zypper_add_repo-small.png" />
       </a>
       <b>Step 4:</b><br />
       <br />
       Add the MonoVS software repository by typing:<br />
       <strong>zypper addrepo http://go-mono.com/monovs-download/latest/openSUSE_11.1/&nbsp;&nbsp;&nbsp;monovs</strong>
       <div class="clearer" />
       <br />
       
       <a href="images/gt_zypper_refresh_repo.png">
         <img class="shot" src="images/gt_zypper_refresh_repo-small.png" />
       </a>
       <b>Step 5:</b><br />
       <br />
       Refresh the MonoVS software repository by typing:<br />
       <strong>zypper refresh --repo monovs</strong>
       <div class="clearer" />
       <br />
       
              
   </div>
</asp:Content>

