<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="tutorials_blog_engine_round_trip_moma_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
BlogEngine.Net Tutorial - Debug Remotely in Mono
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <div class="feature-content">
       <span class="feature-header">BlogEngine.Net Tutorial - Debug Remotely in Mono</span><br />
       <br />
        
       <a href="images/blog_engine_in_vs.png">
         <img class="shot" src="images/blog_engine_in_vs-small.png" />
       </a>
       <b>Step 1:</b><br />
       <br />
       Open the BlogEngine solution in Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs-small.png" />
       </a>
       <b>Step 2:</b><br />
       <br />
       Open default.aspx.cs.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_break_point_set.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_break_point_set-small.png" />
       </a>
       <b>Step 3:</b><br />
       <br />
Set a break point on the first line of the Page_Load method.
       <div class="clearer" />
        <br />

       <a href="images/debug_remote_menu_item.png">
         <img class="shot" src="images/debug_remote_menu_item-small.png" />
       </a>
       <b>Step 4:</b><br />
       <br />
In the Mono menu, click "Debug Remotely in Mono".
       <div class="clearer" />
       <br />

       <a href="images/monovs_choose_remote_host_dialog.png">
         <img class="shot" src="images/monovs_choose_remote_host_dialog-small.png" />
       </a>
       <b>Step 5:</b><br />
       <br />
The MonoVS Choose Remote Host dialog will appear. Choose the host to remotely debug on and click the "Ok" button.
<br>
<br>
Depending on the setup, this process may take awhile to complete as BlogEngine is copied to the remote host in order to be able to be debugged.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_tray_icon_bubble.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_tray_icon_bubble-small.png" />
       </a>
       <b>Step 6:</b><br />
       <br />
A bubble will appear over the MonoVS tray application informing that a remote instance of BlogEngine is running.
       <div class="clearer" />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point-small.png" />
       </a>
       <b>Step 7:</b><br />
       <br />
Visual Studio will stop at the break point.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_inspect_local_variables.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_inspect_local_variables-small.png" />
       </a>
       <b>Step 8:</b><br />
       <br />
Notice that local variables can be inspected inside Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_inspect_call_stack.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_inspect_call_stack-small.png" />
       </a>
       <b>Step 9:</b><br />
       <br />
Notice that the call stack can be inspected inside Visual Studio.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_immediate_window.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_immediate_window-small.png" />
       </a>
       <b>Step 10:</b><br />
       <br />
In the immediate window, type "Page.IsCallback" and press enter. Notice that the immediate window says that Page.IsCallback is currently set to "false."
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_step_over.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_step_over-small.png" />
       </a>
       <b>Step 11:</b><br />
       <br />
In the Debug menu, click "Step Over."
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_default.aspx.cs_stopped_at_break_point_press_continue.png">
         <img class="shot" src="images/blog_engine_default.aspx.cs_stopped_at_break_point_press_continue-small.png" />
       </a>
       <b>Step 12:</b><br />
       <br />
In Visual Studio, Press the "Play" button to continue running BlogEngine.
       <div class="clearer" />
       <br />

       <a href="images/blog_engine_running_remotely_in_ff.png">
         <img class="shot" src="images/blog_engine_running_remotely_in_ff-small.png" />
       </a>
       <b>Step 13:</b><br />
       <br />
BlogEngine will be launched in the default browser.
       <div class="clearer" />
       <br />

       <a href="images/monovs_remote_asp.net_tray_app.png">
         <img class="shot" src="images/monovs_remote_asp.net_tray_app-small.png" />
       </a>
       <b>Step 14:</b><br />
       <br />
To stop this instance of BlogEngine, right click on the MonoVS tray icon and click "Stop".
       <div class="clearer" />
       <br />
   </div>
</asp:Content>

