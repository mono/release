<%@ Page Title="" Language="C#" MasterPageFile="FeaturePage.master" AutoEventWireup="true"
    CodeFile="Debug.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Run and Debug on Mono
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
            <h1>
                Run and Debug on Mono</h1>
            <p>
                Often, the best way to work through an issue will be to debug the application on
                the target environment. Debug on Mono brings this functionality to Visual
                Studio developers by enabling local debugging of Mono applications on Windows
                or remote debugging on Linux and Mac.</p>
            <br /><h2>Step 1:</h2>
            <p>
                Open your solution in Visual Studio and ensure it compiles.</p>
            <br /><img class="shot" src="img/moma1.png" alt="Debug in Linux - Step 1" />
            <br /><h2>Step 2:</h2>
            <p>
                Set your breakpoints like you would normally do.</p>
            <br /><img class="shot" src="img/debug3.png" alt="Debug in Linux - Step 2" />
            <br /><h2>Step 3:</h2>
            <p>
                Select the Mono->Debug in Mono menu item.</p>
            <br /><img class="shot" src="img/debug2.png" alt="Debug in Linux - Step 3" />
            <br /><h2>Step 4:</h2>
            <p>
                A dialog box will prompt you to choose from Mono profiles you have available 
                for running and debugging Mono applications. If you have not created a 
                profile, you can click the "Create Profile" link to create a new configuration for a 
                local or remote Mono installation.</p>
            <br />           
            <p>
                Alternatively, you can enter server details
                in the "Quick Launch" section on the right to run against a remote server instance
                without creating a new configuration.</p>
            <br /><img class="shot" src="img/profile1.png" alt="Debug in Linux - Step 4 - Choose Profile" />    
            <br />          
            <p>
                If you choose to create a new profile, you will have the option to specify the
                path to a locally installed version of Mono, or you can select "Remote Server"
                and specify a server name and port for a remote machine running the Mono Tools
                remote server</p>
            <br />
            <p class="note">
                In order to find servers on the local subnet when configuring a remote server, UDP is 
                used to broadcast over port 1900 using the multicast address 239.255.255.250. If your 
                server is not appearing, you may want to check your firewall settings.
            </p>
            <br />
            <p>
               You can either leave the profile name blank or give it a descriptive name.</p>
            <br /><img class="shot" src="img/profile2.png" alt="Debug in Linux - Step 4 - Create Profile" />
            <br /><h2>Step 5:</h2>
            <p>
                Your application will be compiled, copied over to Linux, and automatically started.
                If it is a web application, it will be launched in your default Windows web browser.</p>
            <br /><img class="shot" src="img/testlin4.jpg" alt="Debug in Linux - Step 5" />
            <br /><h2>Step 6:</h2>
            <p>
                When the application hits the breakpoint, it will stop in Visual Studio, just like
                normal. From here, you can do the normal debug actions, like examine variables and
                call stacks.</p>
            <br /><img class="shot" src="img/debug4.png" alt="Debug in Linux - Step 6" /><br /><br /><br />
        </div>
</asp:Content>
