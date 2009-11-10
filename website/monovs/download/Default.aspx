<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits="download_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" Runat="Server">
    Mono Tools for Visual Studio - Download
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" Runat="Server">
    <img src='<%= ResolveClientUrl("~/Images/MonoVS_Menu_cropped.png") %>' style="float:right;padding:0px 20px 20px 20px;">
<img src='<%= ResolveClientUrl("~/Images/vs-partner_293.png") %>' style="float:right;width:293px;clear:both;padding:20px;">
    <p><b>Download a free, fully-functional 30-day trial of Mono Tools for Visual Studio.</b>  At any point you may <a href="http://mono-project.com/Store">purchase Mono Tools for Visual Studio from Novell</a> to receive an activation code which removes the time limitations from your installed add-in.</p>
      
  
            <div>
                <table id="tblForm" style="width:500px" runat="server">
                  <tr>
                    <td colspan="3"><h3>Registration</h3>
  <p>Please enter your registration information and click 'Download' to start 
  your trial of Mono Tools for Visual Studio.  </p>
                        <asp:ValidationSummary ID="ValidationSummary1" runat="server" />
  </td></tr>
                  <tr>
                    <td width="30">&nbsp;</td>
                    <td align="right"><label for="txtEmail">Email Address<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtEmail" style="width:250px;" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdEmail" runat="server" 
                        ErrorMessage="Email Address is required" 
                        Display="None" ControlToValidate="txtEmail"></asp:RequiredFieldValidator>
                    <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server" 
                        ErrorMessage="Email Address is invalid"
                        Display="None" ControlToValidate="txtEmail" 
                            ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator></td>
                  </tr>
                  <tr>
                    <td>&nbsp;</td>
                    <td align="right">
                    <label for="txtFirstName">First Name<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtFirstName" style="width:250px;" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdFirstName" runat="server" 
                        ErrorMessage="First Name is required" 
                        Display="None" ControlToValidate="txtFirstName"></asp:RequiredFieldValidator></td>
                  </tr>
                  <tr>
                    <td>&nbsp;</td>
                    <td align="right">
                    <label for="txtLastName">Last Name<span style="color:red;">*</span>:</label></td>
                    <td><asp:TextBox ID="txtLastName" style="width:250px;" runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator ID="rqdLastName" runat="server" 
                        ErrorMessage="Last Name is required" 
                        Display="None" ControlToValidate="txtLastName"></asp:RequiredFieldValidator></td>
                  </tr>
                  <tr>
                    <td>&nbsp;</td>
                    <td align="right"><label for="txtOrg">Organization:</label></td>
                    <td><asp:TextBox ID="txtOrg" style="width:250px;" runat="server"></asp:TextBox></td>
                  </tr>
                  <tr>
                    <td>&nbsp;</td>
                    <td align="right"><label for="ddlAppType">What are you interested in building?</label></td>
                    <td>
                        <asp:DropDownList ID="ddlAppType" runat="server" style="width:255px;">
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
                  <tr>
                    <td colspan="3" align="right"><span style="color:red;">*</span>Fields are required.<br /><a class="external" href="http://www.novell.com/company/policies/privacy/">Novell's privacy policy</a></td></tr>
                </table><div style="width:500px;text-align:center">
                    <br/>
                    <asp:ImageButton CausesValidation="true" ID="btnDownload" runat="server" 
                        ImageUrl="~/Images/mp-download-blue.png" onclick="btnDownload_Click" />
                    </div>
            </div>
  
  <h3>Requirements</h3>
  <ul>
  <li>Mono Tools for Visual Studio require Microsoft&trade; Visual Studio&trade; 2008 SP1 Standard,  Professional, or Team Edition.</li>
  <li>To use the remote debugging features of the add-in, you will need a Linux target configured to host Mono's remote debugger.  For convenience, Novell provides a <a href="http://ftp.novell.com/pub/mono/monovs/latest/MonoVS-vm.exe">windows-installable, preconfigured virtual machine</a> for VMware or Virtual PC, and installable packages for openSUSE and SUSE Linux Enterprise.<br/><p style="margin-left: 1em; margin-top: 0pt;"><i>(Note: <a href="http://www.vmware.com/download/player/" class="external" title="http://www.vmware.com/download/player/" rel="nofollow">VMWare Player</a><span class="urlexpansion">&nbsp;(<i>http://www.vmware.com/download/player/</i>)</span> or <a href="http://www.microsoft.com/windows/virtual-pc/" class="external" title="http://www.microsoft.com/windows/virtual-pc/" rel="nofollow">Windows Virtual PC</a> are required to use the preconfigured virtual machines.)</i></p></li>
  </ul>
  
  <h3>Detailed Installation Instructions</h3>
  <p>For a step-by-step guide through the installation process, as well as installation options for using Mono Tools for Visual Studio with Linux environments other than the virtual images provided above, please follow the detailed <a href="http://mono-project.com/GettingStartedWithMonoVS">installation instructions</a>.</p>
<script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqCfg.js"></script>
<script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqImg.js"></script>


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

