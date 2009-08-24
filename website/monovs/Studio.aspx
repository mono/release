<%@ Page Title="" Language="C#" MasterPageFile="Default.master" AutoEventWireup="true"
    CodeFile="Studio.aspx.cs" Inherits="Moma" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Package for Linux</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="feature-content">
        <span class="feature-header">Create SUSE Powered Appliance</span><br />
        <br />
With SUSE Studio, you can bundle your application and a customized version of SUSE Linux into a fully configured, ready to go appliance.
        <br />
        <br />
With everything packaged in a single virtual machine, distribution and setup is simple for both you and your users!
        <br />
        <br />
        <br />
        <br />
        <img class="shot" src="Images/appliance1.png" alt="Create SUSE Studio Appliance - Step 1" />
        <b>Step 1:</b><br />
        <br />
        Go to Mono -> Create SUSE Powered Appliance
        <div class="clearer">
        </div>
        <img class="shot" src="Images/appliance2.png" alt="Create SUSE Studio Appliance - Step 2" />
        <b>Step 2:</b><br />
        <br />
        Enter your SUSE Studio username and API key.
        <br />
        <br />
        <br />
        <div class="note" style="width: 380px; margin-left: 380px; background-position: 2px 17px; background-color: #E5ECF3; border-color: #666699;">
            Hint: If you don't have a SUSE Studio account, sign up for one <a href="http://susestudio.com/account/login">here</a>.
            <br /><br />
            If you have a SUSE Studio account but don't know your API key, get it <a href="http://susestudio.com/user/show_api_key">here</a>.
        </div>
        <div class="clearer">
        </div>
        <img class="shot" src="Images/appliance3.png" alt="Create SUSE Studio Appliance - Step 3" />
        <b>Step 3:</b><br />
        <br />
        You will be presented with a list of all your appliances available on SUSE Studio.  Choose one that you wish to modify, or click the "+" button in the lower left to create a new appliance.
        <div class="clearer">
        </div>
        <img class="shot" src="Images/appliance4.png" alt="Create SUSE Studio Appliance - Step 4" />
        <b>Step 4:</b><br />
        <br />
        When you create a new appliance, you can give it a name, choose the version of SUSE you want, and the architecture you want.
        <div class="clearer">
        </div>
        <img class="shot" src="Images/appliance5.png" alt="Create SUSE Studio Appliance - Step 5" />
        <b>Step 5:</b><br />
        <br />
        Once you've selected the appliance to use, choose your Linux RPM package that you want to upload to the appliance.
         <br />
        <br />
        <br />
        <div class="note" style="width: 380px; margin-left: 380px; background-position: 2px 17px; background-color: #E5ECF3; border-color: #666699;">
            Hint: If you haven't created a Linux installer package for your application, do that first with the <a href="Package.aspx">Create Package functionality</a>.
        </div>
       <div class="clearer">
        </div>
        <img class="shot" src="Images/appliance6.png" alt="Create SUSE Studio Appliance - Step 6" />
        <b>Step 6:</b><br />
        <br />
        Your appliance will be created and your package will be uploaded to the it.  From here, you can go to the SUSE Studio website to further customize and build your appliance.
        <div class="clearer">
        </div>
    </div>
</asp:Content>
