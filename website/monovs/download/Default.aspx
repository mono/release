<%@ Page Title="" Language="C#" MasterPageFile="~/Default.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="download_Default" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Download
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="head" runat="Server">
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="maincontent" runat="Server">
    <div class="container_12">
        <div class="grid_7">
            <p>
                <b>Download a free, fully-functional 30-day trial of Mono Tools for Visual Studio.</b>
                At any point you may <a href="http://mono-project.com/Store">purchase Mono Tools for
                    Visual Studio from Novell</a> to receive an activation code which removes the
                time limitations from your installed add-in.</p>
            <h1>
                Registration</h1>
            <p>
                Please enter your registration information and click 'Download' to start your trial
                of Mono Tools for Visual Studio.
            </p>
        </div>
        <div class="grid_5">
            <img id="partner" src='<%= ResolveClientUrl("~/img/vs_partner_2010_293.png") %>'>
        </div>
        <div class="grid_12 clear">
            <table id="tblForm" runat="server">
                <tr>
                    <td colspan="2">
                        <asp:ValidationSummary ID="ValidationSummary1" runat="server" />
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="ctl00_maincontent_txtEmail">
                            Email Address<span style="color: red;">*</span>:</label>
                    </td>
                    <td>
                        <asp:TextBox ID="txtEmail" runat="server"></asp:TextBox>
                        <asp:RequiredFieldValidator ID="rqdEmail" runat="server" ErrorMessage="Email Address is required"
                            Display="None" ControlToValidate="txtEmail"></asp:RequiredFieldValidator>
                        <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server" ErrorMessage="Email Address is invalid"
                            Display="None" ControlToValidate="txtEmail" ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="ctl00_maincontent_txtFirstName">
                            First Name<span style="color: red;">*</span>:</label>
                    </td>
                    <td>
                        <asp:TextBox ID="txtFirstName" runat="server"></asp:TextBox>
                        <asp:RequiredFieldValidator ID="rqdFirstName" runat="server" ErrorMessage="First Name is required"
                            Display="None" ControlToValidate="txtFirstName"></asp:RequiredFieldValidator>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="ctl00_maincontent_txtLastName">
                            Last Name<span style="color: red;">*</span>:</label>
                    </td>
                    <td>
                        <asp:TextBox ID="txtLastName" runat="server"></asp:TextBox>
                        <asp:RequiredFieldValidator ID="rqdLastName" runat="server" ErrorMessage="Last Name is required"
                            Display="None" ControlToValidate="txtLastName"></asp:RequiredFieldValidator>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="ctl00_maincontent_txtOrg">
                            Organization:</label>
                    </td>
                    <td>
                        <asp:TextBox ID="txtOrg" runat="server"></asp:TextBox>
                    </td>
                </tr>
                <tr>
                    <td class="label">
                        <label for="ctl00_maincontent_ddlAppType">
                            What are you interested in building?</label>
                    </td>
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
        </div>
        <div class="grid_7 prefix_5 clear">
            <p class="small">
                * Fields are required. <a class="external" href="http://www.novell.com/company/policies/privacy/">
                    Novell's privacy policy</a>.</p>
        </div>
        <div class="grid_7 prefix_5 clear">
            <asp:LinkButton CausesValidation="true" class="button" ID="btnDownloadMsi" runat="server"
                Text="Download for VS 2008" OnClick="btnDownloadMsi_Click" />
            or
            <asp:LinkButton CausesValidation="true" class="button" ID="btnDownloadVsix" runat="server"
                Text="Download for VS 2010" OnClick="btnDownloadVsix_Click" />
        </div>
        <div class="grid_12">
            <h2>
                Requirements</h2>
            <ul style="margin-left:25px">
                <li>Mono Tools for Visual Studio requires Microsoft&trade; Visual Studio&trade; 2008
                    SP1 Standard, Professional, or Team Edition, or Microsoft&trade; Visual Studio&trade;
                    2010 Professional, Premium, or Ultimate.</li>
                <li>To use the remote debugging features of the add-in, you will need a target configured
                    to host Mono's remote debugger. Please use one of the links below to download one
                    or more of the Mono environments that works best for you:
                    <ul style="margin-left:25px">
                        <li>The most recent <a href="http://ftp.novell.com/pub/mono/monotools/latest/mono-windows.exe"
                            class="external" title="http://ftp.novell.com/pub/mono/monotools/latest/mono-windows.exe"
                            rel="nofollow">Mono for Windows</a>
                        </li>
                        <li>The most recent <a href="http://ftp.novell.com/pub/mono/monotools/latest/monotools-server.dmg"
                            class="external" title="http://ftp.novell.com/pub/mono/monotools/latest/monotools-server.dmg"
                            rel="nofollow">MonoTools Server for Mac OS X</a>
                            (required to debug Mono on Mac OS X)
                            <ul style="margin-left:25px">
                                <li>Requires the most recent <a href="http://ftp.novell.com/pub/mono/monotools/latest/MonoFramework-x86.dmg"
                                    class="external" title="http://ftp.novell.com/pub/mono/monotools/latest/MonoFramework-x86.dmg"
                                    rel="nofollow">Mono for Mac OS X</a>
                                </li>
                            </ul>
                        </li>
                        <li>Linux
                            <ul style="margin-left:25px">
                                <li><a href="http://ftp.novell.com/pub/mono/monotools/latest/MonoTools-vmx.zip" class="external"
                                    title="http://ftp.novell.com/pub/mono/monotools/latest/MonoTools-vmx.zip" rel="nofollow">
                                    Preconfigured MonoTools Server openSUSE VMware image</a>
                                    (500MB) - or - </li>
                                <li><a href="http://ftp.novell.com/pub/mono/monotools/latest/MonoTools-vpc.zip" class="external"
                                    title="http://ftp.novell.com/pub/mono/monotools/latest/MonoTools-vpc.zip" rel="nofollow">
                                    Preconfigured MonoTools Server openSUSE VirtualPC image</a>
                                    (500MB) - or - </li>
                                <li>Use Yum to install monotools-addon-server from <a href="http://ftp.novell.com/pub/mono/download-stable/RHEL_5/"
                                    class="external" title="http://ftp.novell.com/pub/mono/download-stable/RHEL 5/"
                                    rel="nofollow">the RedHat/CentOS Mono repo</a>
                                    - or - </li>
                                <li>Use the openSUSE 1click from your existing Linux system: </li>
                            </ul>
                        </li>
                    </ul>
                    <p style="margin-left:75px">
                        <a href="http://ftp.novell.com/pub/mono/monotools/monotools.ymp"
                            class="external" title="http://ftp.novell.com/pub/mono/monotools/monotools.ymp"
                            rel="nofollow"><img src="http://mono-project.com/files/2/2b/Monovs-1click.png" alt="Monovs-1click.png"></a>
                    </p>
                    <ul style="margin-left:25px">
                        <li>Other platforms will need to build from the <a href="http://ftp.novell.com/pub/mono/monotools/latest/monotools-server-2.0.tar.bz2"
                            class="external" title="http://ftp.novell.com/pub/mono/monotools/latest/monotools-server-2.0.tar.bz2"
                            rel="nofollow">Mono Tools 2.0 Server sources</a>
                        </li>
                    </ul>
                    <br />
                </li>
            </ul>
            <p class="note">
                Note: <a href="http://www.vmware.com/download/player/" class="external" title="http://www.vmware.com/download/player/"
                    rel="nofollow">VMWare Player</a><span class="urlexpansion">&nbsp;(<i>http://www.vmware.com/download/player/</i>)</span>
                or <a href="http://www.microsoft.com/windows/virtual-pc/" class="external" title="http://www.microsoft.com/windows/virtual-pc/"
                    rel="nofollow">Windows Virtual PC</a> are required to use the preconfigured
                virtual machines.</p>
            <h2>
                Detailed Installation Instructions</h2>
            <p>
                For a step-by-step guide through the installation process, as well as installation
                options for using Mono Tools for Visual Studio with Linux environments other than
                the virtual image provided above, please follow the detailed <a href="http://mono-project.com/GettingStartedWithMonoVS">
                    installation instructions</a>.</p>
            <script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqCfg.js"></script>
            <script type="text/javascript" src="http://www.novell.com/common/inc/elqNow/elqImg.js"></script>
        </div>
    </div>
    <script type='text/javascript'><!--        //
        var elqPPS = '70';
//--></script>
    <script type='text/javascript' src='http://www.novell.com/common/inc/elqNow/elqScr.js'></script>
    <script type='text/javascript'><!--        //
        window.onload = initPage;
        function initPage() {
            if (this.GetElqCustomerGUID) {
                document.getElementById('ctl00_maincontent_elqCustomerGUID').value = GetElqCustomerGUID();
                //document.forms["aspnetForm"].elements["elqCustomerGUID"].value = GetElqCustomerGUID();
            }
        }
//--></script>
</asp:Content>
