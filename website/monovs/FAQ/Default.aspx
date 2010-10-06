<%@ Page Title="" Language="C#" MasterPageFile="~/FeaturePage.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="FAQ_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - FAQ
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <h1>
        Frequently Asked Questions</h1>
    <div id="toc">
        <h5>
            Table of Contents</h5>
        <div class="tocline">
            <a href="#General"><span class="number">1</span> General</a><br />
        </div>
        <div class="tocline">
            <a href="#Running_on_Mono"><span class="number">2</span> Running on Mono</a><br />
        </div>
        <div class="tocindent">
            <div class="tocindent">
                <div class="tocindent">
                    <p>
                        <a href="#-_Place_a_copy_of_the_.dll_in_the_Mono_GAC:"><span class="number">2.1</span>
                            - Place a copy of the .dll in the Mono GAC:</a><br />
                        <a href="#-_Add_a_project_reference_to_the_.dll:"><span class="number">2.2</span> -
                            Add a project reference to the .dll:</a><br />
                        <a href="#-_Place_a_copy_of_the_.dll_in_your_website.27s_Bin_folder"><span class="number">
                            2.3</span> - Place a copy of the .dll in your website's Bin folder</a><br />
                    </p>
                </div>
            </div>
        </div>
        <div class="tocline">
            <a href="#Packaging"><span class="number">3</span> Packaging</a><br />
        </div>
    </div>
    <div id="faq" class="grid_10" style="width: 600px;">
        <a name="General"></a>
        <h2>
            General
        </h2>
        <p>
            <b>How do I find out the IP address and port used by the server?</b>
        </p>
        <p>
            Right click on the server's tray icon.  This will display the port and all
            of the IP addresses that the server is accessible on.
        </p>
        <p>
            <b>My server isn't showing up in the server browser dialog</b>
        </p>
        <p>
            If your server isn't being discovered (which could be due to firewalls), you can
            manually enter your server's IP address. The default port used by the server is
            8805.
        </p>
        <p>
            <b>My server is showing up with the wrong IP address</b>
        </p>
        <p>
            This is generally caused by NAT, which masks the server's true IP address. You can
            manually enter your server's real IP address.
        </p>
        <p>
            <b>I'm running a firewall, what ports do I need to open?</b>
        </p>
        <ul>
            <li>8805 - monotools-server.exe server </li>
            <li>8806-8872 - application ports </li>
        </ul>
        <p>
            If you want to use different ports, you can change them in the configuration files:
        </p>
        <ul>
            <li>/usr/lib/monotools-gui-server.exe.config for the GUI version </li>
            <li>/usr/lib/monotools-server.exe.config for the command line version </li>
        </ul>
        <p>
            <b>What are the passwords for the MonoTools virtual machine image?</b>
        </p>
        <ul>
            <li>The default account is rupert/mono. </li>
            <li>The root account is root/mono. </li>
        </ul>
        <a name="Running_on_Mono"></a>
        <h2>
            Running on Mono
        </h2>
        <p>
            <b>How can I see output/enter input to a console program?</b>
        </p>
        <ul>
            <li>Go to the server </li>
            <li>Right click the Mono icon in the tray. </li>
            <li>Choose "Run in Terminal" </li>
        </ul>
        <p>
            Now when you run your program, a console will appear on the server that you can interact
            with.
        </p>
        <p>
            <b>Where does my application get put when I run/debug remotely?</b>
        </p>
        <p>
            Your application gets placed in: /tmp/monotools-{ProjectName}
        </p>
        <p>
            <b>I reference a .dll in the GAC in my web.config that isn't available when I run in
                Mono</b>
        </p>
        <p>
            There are a couple of options here.
        </p>
        <a name="-_Place_a_copy_of_the_.dll_in_the_Mono_GAC:"></a>
        <h5>
            - Place a copy of the .dll in the Mono GAC:</h5>
        <p>
            On Windows:
        </p>
        <pre>mono gacutil -i MyAssembly.dll</pre>
        <p>
            On Linux:
        </p>
        <pre>gacutil -i MyAssembly.dll</pre>
        <a name="-_Add_a_project_reference_to_the_.dll:"></a>
        <h5>
            - Add a project reference to the .dll:</h5>
        <ul>
            <li>Right click on References. </li>
            <li>Add a reference to the .dll. </li>
            <li>In the properties for the .dll, set Copy Local = true. </li>
        </ul>
        <a name="-_Place_a_copy_of_the_.dll_in_your_website.27s_Bin_folder"></a>
        <h5>
            - Place a copy of the .dll in your website's Bin folder</h5>
        <a name="Packaging"></a>
        <h2>
            Packaging
        </h2>
        <p>
            <b>Can I create packages for Ubuntu/Debian?</b>
        </p>
        <p>
            At this time, MonoTools only support creating packages for SUSE Linux and Red Hat Linux (.rpm). Creating
            packages for Ubuntu/Debian (.deb) is something we will definitely be considering
            for a future release.
        </p>
        <p>
            <b>How can I package a precompiled version of my web site?</b>
        </p>
        <p>
            If you are using the "Precompile Web Applications" option when running and debugging
            your ASP.NET solutions, you should package a precompiled version of your solution
            to ensure the same behavior within the packaged solution. This can be done in the
            "Files" tab of Package Configuration wizard by clicking the "Precompile this website
            to a temporary location and add files to list" link at the bottom of the form.
        </p>
        <p>
            Note this is a static copy of your website.  You will need to redo this each time
            your website changes.
        </p>
    </div>
</asp:Content>
