<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="download_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
    Mono Tools for Visual Studio - Download
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
<div class="container_12">
    <div class="grid_7">

    
    <p><b>Download a free, fully-functional 30-day trial of Mono Tools for Visual Studio.</b>  At any point you may <a href="http://mono-project.com/Store">purchase Mono Tools for Visual Studio from Novell</a> to receive an activation code which removes the time limitations from your installed add-in.</p>
    <h1>Registration</h1>
      <p>Please enter your registration information and click 'Download' to start 
      your trial of Mono Tools for Visual Studio.  </p>      
    </div>
    <div class="grid_5">
        <!--<img src='<%= ResolveClientUrl("~/img/MonoVS_Menu_cropped.png") %>'>-->
        <img src='<%= ResolveClientUrl("~/img/vs_partner_2010_293.png") %>'>
    </div>   
    <div class="grid_12 clear">  
            <div>
                <table id="tblForm" runat="server">
                  <tr>
                    <td colspan="2">
                        <asp:ValidationSummary ID="ValidationSummary1" runat="server" />
  </td></tr>
                  <tr>

                    <td align="right"><label for="txtEmail">Email Address<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtEmail" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdEmail" runat="server" 
                        ErrorMessage="Email Address is required" 
                        Display="None" ControlToValidate="txtEmail"></asp:RequiredFieldValidator>
                    <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server" 
                        ErrorMessage="Email Address is invalid"
                        Display="None" ControlToValidate="txtEmail" 
                            ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator></td>
                  </tr>
                  <tr>

                    <td align="right">
                    <label for="txtFirstName">First Name<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtFirstName" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdFirstName" runat="server" 
                        ErrorMessage="First Name is required" 
                        Display="None" ControlToValidate="txtFirstName"></asp:RequiredFieldValidator></td>
                  </tr>
                  <tr>

                    <td align="right">
                    <label for="txtLastName">Last Name<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtLastName" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdLastName" runat="server" 
                        ErrorMessage="Last Name is required" 
                        Display="None" ControlToValidate="txtLastName"></asp:RequiredFieldValidator></td>
                  </tr>
                  <tr>

                    <td align="right"><label for="txtOrg">Organization:</label></td>
                    <td><asp:TextBox ID="txtOrg" runat="server"></asp:TextBox></td>
                  </tr>
                  <tr>

                    <td align="right"><label for="ddlAppType">What are you interested in building?</label></td>
                    <td>
                        <asp:DropDownList ID="ddlAppType" runat="server">
                            <asp:ListItem Selected="True" Value="Choose..."></asp:ListItem>
                            <asp:ListItem Value="Corporate (internal) Website"></asp:ListItem>
                            <asp:ListItem Value="Corporate (internal) Desktop application"></asp:ListItem>
                            <asp:ListItem Value="Desktop application for resale"></asp:ListItem>
                            <asp:ListItem Value="Web application for resale"></asp:ListItem>
                            <asp:ListItem Value="Public-facing Website"></asp:ListItem>
                            <asp:ListItem Value="Embedded Device"></asp:ListItem>
                            <asp:ListItem Value="Open Source Project"></asp:ListItem>
                            <asp:ListItem Value="Other"></asp:ListItem>
                        </asp:DropDownList>
<input type="hidden" id="elqCustomerGUID" name="elqCustomerGUID" value="" runat="server" />
<input type="hidden" id="elqCookieWrite" name="elqCookieWrite" value="0" runat="server" />
                    </td>
                  </tr>
                </table>
                <p class="small">* Fields are required. <a class="external" href="http://www.novell.com/company/policies/privacy/">Novell's privacy policy</a>.</p>
                

                    <asp:ImageButton CausesValidation="true" ID="btnDownloadMsi" runat="server" 
                        ImageUrl="~/img/mp-download-2008.png" onclick="btnDownloadMsi_Click" /> or 
                    <asp:ImageButton CausesValidation="true" ID="btnDownloadVsix" runat="server" 
                        ImageUrl="~/img/mp-download-2010.png" onclick="btnDownloadVsix_Click" />

            </div>
    </div>
     
   <div class="grid_12">
      <h2>Requirements</h2>
      <ul>
      <li>Mono Tools for Visual Studio requires Microsoft&trade; Visual Studio&trade; 2008 SP1 Standard,  Professional, or Team Edition, or Microsoft&trade; Visual Studio&trade; 2010 Professional, Premium, or Ultimate.</li>
      <li>To use the remote debugging features of the add-in, you will need a Linux target configured to host Mono's remote debugger.  For convenience, Novell provides a <a href="http://ftp.novell.com/pub/mono/monovs/latest/MonoVS-vm.exe">windows-installable, preconfigured virtual machine</a> for VMware or Virtual PC, and installable packages for openSUSE and SUSE Linux Enterprise.<br/>
      </li>
      </ul>
  <p class="note">Note: <a href="http://www.vmware.com/download/player/" class="external" title="http://www.vmware.com/download/player/" rel="nofollow">VMWare Player</a><span class="urlexpansion">&nbsp;(<i>http://www.vmware.com/download/player/</i>)</span> or <a href="http://www.microsoft.com/windows/virtual-pc/" class="external" title="http://www.microsoft.com/windows/virtual-pc/" rel="nofollow">Windows Virtual PC</a> are required to use the preconfigured virtual machines.</p>
  
      <h2>Detailed Installation Instructions</h2>
      <p>For a step-by-step guide through the installation process, as well as installation options for using Mono Tools for Visual Studio with Linux environments other than the virtual img provided above, please follow the detailed <a href="http://mono-project.com/GettingStartedWithMonoVS">installation instructions</a>.</p>
    <script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqCfg.js"></script>
    <script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqImg.js"></script>
    </div>
</div>
<SCRIPT TYPE='text/javascript' LANGUAGE='JavaScript'><!--//
var elqPPS = '70';
//--></SCRIPT>
<SCRIPT TYPE='text/javascript' LANGUAGE='JavaScript' SRC='http://www.novell.com/common/inc/elqNow/elqScr.js'></SCRIPT>
<SCRIPT TYPE='text/javascript' LANGUAGE='JavaScript'><!--//
window.onload = initPage;
function initPage(){
    if (this.GetElqCustomerGUID) {
        document.getElementById('ctl00_maincontent_elqCustomerGUID').value = GetElqCustomerGUID();
        //document.forms["aspnetForm"].elements["elqCustomerGUID"].value = GetElqCustomerGUID();
    }
}
//--></SCRIPT>
</asp:Content>

