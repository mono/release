<%@ Page Title="" Language="C#" MasterPageFile="FeaturePage.master" AutoEventWireup="true"
    CodeFile="Debug.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Debug on Mono on Linux
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
            <h1>
                Debug on Mono on Linux</h1>
            <p>
                Often, the best way to work through an issue will be to debug the application on
                the target environment. Debug on Mono on Linux brings this functionality to Visual
                Studio developers by enabling remote debugging of Mono applications running on Linux.</p>
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
                Select the Mono->Debug Remotely in Mono menu item.</p>
            <br /><img class="shot" src="img/debug2.png" alt="Debug in Linux - Step 3" />
            <br /><h2>Step 4:</h2>
            <p>
                A dialog box will prompt you to choose from the available servers it found on you
                local network. If your server doesn't show up, you can manually enter in the IP
                address and port of the server you wish to use.</p>
            <br /><p class="note">
                In order to find servers on the local subnet, UDP is used to broadcast over port
                1900 using the multicast address 239.255.255.250. If your server is not appearing,
                you may want to check your firewall settings.
            </p>
            <br /><img class="shot" src="img/testlin3.png" alt="Debug in Linux - Step 4" />
            <br /><h2>Step 5:</h2>
            <p>
                Your application will be compiled, copied over to Linux, and automatically started.
                If it is a web application, it will be launched in your default Windows web browser.</p>
            <br /><img class="shot" src="img/debug4.png" alt="Debug in Linux - Step 6" />
            <br /><h2>Step 6:</h2>
            <p>
                When the application hits the breakpoint, it will stop in Visual Studio, just like
                normal. From here, you can do the normal debug actions, like examine variables and
                call stacks.</p>
            <br /><img class="shot" src="img/testlin4.jpg" alt="Debug in Linux - Step 5" /><br /><br /><br />
        </div>
</asp:Content>
