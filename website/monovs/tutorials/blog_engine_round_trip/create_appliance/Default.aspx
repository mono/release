<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial - Create SUSE Powered Appliance
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial - Create SUSE Powered Appliance</span><br />
       <br />
        
       <a href="images/blog_engine_in_vs.png">
         <img class="shot" src="images/blog_engine_in_vs-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       Open the BlogEngine solution in Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/create_appliance_menu_item.png">
         <img class="shot" src="images/create_appliance_menu_item-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
In the Mono menu, click "Create SUSE Powered Appliance".
       <div class="clearer" />
       <br />

       <a href="images/appliance_wizard_step_1.png">
         <img class="shot" src="images/appliance_wizard_step_1-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
The SUSE Studio wizard will appear. Once the text has been read, click the "Next" button.
       <div class="clearer" />
        <br />

       <a href="images/appliance_wizard_step_2.png">
         <img class="shot" src="images/appliance_wizard_step_2-small.png" />
       </a>
       <b>Step 4:</b><br />
       <br />
Enter the Username and API key and click the "Next" button.
<br>
<br>
If either the Username or API key is unknown, use the help links in the dialog and follow the instructions.
       <div class="clearer" />
       <br />

       <a href="images/appliance_wizard_step_3.png">
         <img class="shot" src="images/appliance_wizard_step_3-small.png" />
       </a>
       <b>Step 5:</b><br />
       <br />
Select "Or create a new appliance:" and fill out the form with the following Values:<br>
<ul>
<li><strong>Name:</strong> BlogEngine Appliance</li>
<li><strong>Template:</strong> Mono ASP.NET Server (openSUSE)</li>
<li><strong>Architecture:</strong> 32 bit</li>
</ul>
When done, click the "Next" button.
       <div class="clearer" />
       <br />

       <a href="images/appliance_wizard_step_4.png">
         <img class="shot" src="images/appliance_wizard_step_4-small.png" />
       </a>
       <b>Step 6:</b><br />
       <br />
Select the package that was created during the <a href="../create_rpm">Create Linux Package for Project</a> tutorial and click the "Next" button.
       <div class="clearer" />

       <a href="images/appliance_wizard_step_5.png">
         <img class="shot" src="images/appliance_wizard_step_5-small.png" />
       </a>
       <b>Step 7:</b><br />
       <br />
When the appliance has been built, a completion dialog will be displayed. Click the "Finish" button.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_login_page.png">
         <img class="shot" src="images/suse_studio_login_page-small.png" />
       </a>
       <b>Step 8:</b><br />
       <br />
SUSE Studio will be launched in the default browser. Login to SUSE Studio.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_start_page.png">
         <img class="shot" src="images/suse_studio_start_page-small.png" />
       </a>
       <b>Step 9:</b><br />
       <br />
The SUSE Studio Start page will be displayed. Click on the "Build" tab.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_build_page.png">
         <img class="shot" src="images/suse_studio_build_page-small.png" />
       </a>
       <b>Step 10:</b><br />
       <br />
Change the "Format" to be "VMware / VirtualBox" and click the "Build" button.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_building_vm.png">
         <img class="shot" src="images/suse_studio_building_vm-small.png" />
       </a>
       <b>Step 11:</b><br />
       <br />
SUSE Studio will start building the VM. This may take a few minutes.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_testdrive_button.png">
         <img class="shot" src="images/suse_studio_testdrive_button-small.png" />
       </a>
       <b>Step 12:</b><br />
       <br />
Once the VM is done building, click on the "Testdrive" link.
<br>
<br>
<strong>Warning:</strong> Testdrive will only allow the VM to run for 60 minutes.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_test_drive_booted.png">
         <img class="shot" src="images/suse_studio_test_drive_booted-small.png" />
       </a>
       <b>Step 13:</b><br />
       <br />
Testdrive will boot the newly created VM and login as the "rupert" user. Since this is an ASP.NET server appliance, the VM will boot to text mode.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_test_drive_networking_tab.png">
         <img class="shot" src="images/suse_studio_test_drive_networking_tab-small.png" />
       </a>
       <b>Step 14:</b><br />
       <br />
Change to the Network tab and click on the "Enable Networking" button.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_test_drive_networking_tab_try_out_your_web_app.png">
         <img class="shot" src="images/suse_studio_test_drive_networking_tab_try_out_your_web_app-small.png" />
       </a>
       <b>Step 15:</b><br />
       <br />
In the Network tab under "Try out your web app", click on the port 80 link.
       <div class="clearer" />
       <br />

       <a href="images/suse_studio_test_drive_blog_engine_running.png">
         <img class="shot" src="images/suse_studio_test_drive_blog_engine_running-small.png" />
       </a>
       <b>Step 16:</b><br />
       <br />
BlogEngine will appear.
       <div class="clearer" />
       <br />
   </div>
</asp:Content>

