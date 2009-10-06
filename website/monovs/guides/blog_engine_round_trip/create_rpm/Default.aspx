<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial - Create Linux Package for Project
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial - Create Linux Package for Project</span><br />
       <br />
        
       <a href="images/blog_engine_in_vs.png">
         <img class="shot" src="images/blog_engine_in_vs-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       Open the BlogEngine solution in Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/build_solution_menu_item.png">
         <img class="shot" src="images/build_solution_menu_item-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
In the Build menu, click "Build Solution."
       <div class="clearer" />
       <br />

       <a href="images/create_rpm_menu_item.png">
         <img class="shot" src="images/create_rpm_menu_item-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
In the Mono menu, click "Create Linux Package for Project".
       <div class="clearer" />
        <br />

       <a href="images/select_project_dialog.png">
         <img class="shot" src="images/select_project_dialog-small.png" />
       </a>
       <b>Step 4:</b><br />
       <br />
Because the BlogEngine solution has 3 projects in it, a prompt to select which project to add the Linux package files to will appear.
<br>
<br>
Select BlogEngine.Web (this is the startup project), and then click the "Ok" button.
       <div class="clearer" />
       <br />

       <a href="images/package_config-general_tab.png">
         <img class="shot" src="images/package_config-general_tab-small.png" />
       </a>
       <b>Step 5:</b><br />
       <br />
Fill out the "General" tab with the following values:
<ul>
<li><strong>Application Name:</strong> BlogEngine</li>
<li><strong>Package Name:</strong> blogengine</li>
<li><strong>Version:</strong> 1.5</li>
<li><strong>License:</strong> Ms-RL</li>
<li><strong>Type:</strong> ASP.NET Application</li>
<li><strong>Virtual Path:</strong> [leave blank]</li>
<li><strong>Group:</strong> Productivity/Networking/Web/Frontends</li>
<li><strong>Summary:</strong> Blog Software</li>
<li><strong>Webpage:</strong> http://blogengine.codeplex.com</li>
<li><strong>Description:</strong> Blog Software</li>
</ul>
       <div class="clearer" />
       <br />

       <a href="images/package_config-files_tab-add_entire_directory.png">
         <img class="shot" src="images/package_config-files_tab-add_entire_directory-small.png" />
       </a>
       <b>Step 6:</b><br />
       <br />
Click on the "Files" tab, then right click on "Application Root" and select "Add Entire Directory".
       <div class="clearer" />

       <a href="images/package_config-files_tab-browse_for_folder.png">
         <img class="shot" src="images/package_config-files_tab-browse_for_folder-small.png" />
       </a>
       <b>Step 7:</b><br />
       <br />
Browse to the BlogEngine.Web folder and click the "Ok" button.
       <div class="clearer" />
       <br />

       <a href="images/package_config-dependencies_tab-rescan_dependencies.png">
         <img class="shot" src="images/package_config-dependencies_tab-rescan_dependencies-small.png" />
       </a>
       <b>Step 8:</b><br />
       <br />
Click on the "Dependencies" tab, then click on the "Rescan Dependencies" button.
       <div class="clearer" />
       <br />

       <a href="images/package_config-dependencies_tab-deps_filled_out.png">
         <img class="shot" src="images/package_config-dependencies_tab-deps_filled_out-small.png" />
       </a>
       <b>Step 9:</b><br />
       <br />
Notice that the necessary dependencies have been detected and added to the list.
       <div class="clearer" />
       <br />

       <a href="images/package_config-dependecies_tab-add_sys_management_manually.png">
         <img class="shot" src="images/package_config-dependecies_tab-add_sys_management_manually-small.png" />
       </a>
       <b>Step 10:</b><br />
       <br />
Select the "System.Management 2.0.0.0" assembly and click on the left arrow button to manually add it to the dependency list.
       <div class="clearer" />
       <br />

       <a href="images/package_config-advanced_tab.png">
         <img class="shot" src="images/package_config-advanced_tab-small.png" />
       </a>
       <b>Step 11:</b><br />
       <br />
Click on the "Advanced" tab. Everything in this tab should already be filled out correctly.
       <div class="clearer" />
       <br />

       <a href="images/package_config-create_package.png">
         <img class="shot" src="images/package_config-create_package-small.png" />
       </a>
       <b>Step 12:</b><br />
       <br />
Save the solution, then click the "Create Package" button.
       <div class="clearer" />
       <br />

       <a href="images/monovs_choose_remote_host_dialog.png">
         <img class="shot" src="images/monovs_choose_remote_host_dialog-small.png" />
       </a>
       <b>Step 13:</b><br />
       <br />
The MonoVS Choose Remote Host dialog will appear. Choose the host to remotely build the Linux package on and click the "Ok" button.
       <div class="clearer" />
       <br />

       <a href="images/create_package-save_rpm_dialog.png">
         <img class="shot" src="images/create_package-save_rpm_dialog-small.png" />
       </a>
       <b>Step 14:</b><br />
       <br />
Select the folder to save the Linux package to once it's built. For this example, it's best to just save it to the Desktop.
       <div class="clearer" />
       <br />

       <a href="images/create_package-building_rpm.png">
         <img class="shot" src="images/create_package-building_rpm-small.png" />
       </a>
       <b>Step 15:</b><br />
       <br />
While the Linux package is being built, the Visual Studio status bar will say "Building package.." Depending on the setup, this could take awhile.
<br>
<br>
Once built, the Linux package will be placed in the location chosen.
       <div class="clearer" />
       <br />
   </div>
</asp:Content>

