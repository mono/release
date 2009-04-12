<%@ Page 
    Language="C#" 
    MasterPageFile="~/Mono.Master" 
    AutoEventWireup="true" 
    CodeBehind="Default.aspx.cs" 
    Inherits="ModMonoConfig.Default"
    Title="Untitled Page" %>
<%@ Register src="Config.ascx" tagname="Config" tagprefix="uc1" %>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
    Configure Apache Mod_Mono
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">
    <link rel="stylesheet" type="text/css" href="Default.css" />
    <script language="javascript" type="text/javascript" src="Default.js"></script>
          
        <p>
            mod_mono is an Apache 2.0/2.2 module that provides 
            <a href="http://mono-project.com/ASP.NET" title="ASP.NET">ASP.NET</a> 
            support for the web's favorite server, 
            <a href="http://httpd.apache.org" class="external" title="http://httpd.apache.org" rel="nofollow">Apache</a>.
        </p> 
        <p>

        Use the form below to generate an Apache mod_mono configuration file suitable for use on SUSE and openSUSE. 
        </p>
        
    
    <h2>Configuration Type</h2>
    <table class="details">
        <tr>
            <td>
                <asp:RadioButton ID="radVhost" runat="server" Text="Virtual Host" GroupName="grpApplicationType" Checked="true" onclick="radApplicationType_Click(this);" />
            </td>
        </tr>
        <tr>
            <td>
                <label class="info">Configure a name-based 
                    <a href="http://httpd.apache.org/docs/2.0/vhosts/" title="Virtual Host" target="_blank">Virtual Host</a> 
                    to host an ASP.NET application.
                </label>
            </td>
        </tr>
        <tr>
            <td>
                <asp:RadioButton ID="radApplication" runat="server" Text="Application" GroupName="grpApplicationType" onclick="radApplicationType_Click(this);" />
            </td>
        </tr>
        <tr>
            <td>
                <label class="info">Configure a new ASP.NET application (i.e., virtual directory).<br />This configuration is suitable for adding an application to an existing host or virtual host.</label>
            </td>
        </tr>
    </table>
            
    <div id="divVhost" class="vhost">
        <h2>Server Details</h2>
            
        <table class="details">
            <tr>
                <td colspan="2">          
                    <label for="<%= this.txtServerName.ClientID %>" class="textfield">
                        Server Name<span class="required">*</span></label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox 
                        ID="txtServerName"
                        ValidationGroup="grpVhost" 
                        CssClass="textfield" 
                        runat="server"></asp:TextBox>
                </td>
                <td width="100%">
                    <label for="<%= this.txtServerName.ClientID %>" class="info">
                        e.g. <em>go-mono.com</em></label>
                    <asp:RequiredFieldValidator 
                        ID="rqdServerName" 
                        ValidationGroup="grpVhost" 
                        ControlToValidate="txtServerName" 
                        ErrorMessage="Server Name is Required"
                        Display="None"
                        runat="server"></asp:RequiredFieldValidator>
                </td>
            </tr>
            <tr>
                <td colspan="2">  
                    <label for="<%= this.txtServerAliases.ClientID %>" class="textfield">
                        Server Aliases</label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox 
                        ID="txtServerAliases" 
                        ValidationGroup="grpVhost" 
                        CssClass="textfield" 
                        style="display:none"
                        runat="server"></asp:TextBox>
                    <asp:TextBox 
                        ID="txtSeverAlias" 
                        ValidationGroup="grpVhost" 
                        CssClass="textfield" 
                        runat="server"
                        onkeydown="return txtServerAlias_keypress(this, event);"></asp:TextBox><br />
                    <input 
                        style="float:right" 
                        type="button" 
                        id="btnAddServerAlias" 
                        onclick="btnAddServerAlias_click();" 
                        value="Add" />
                </td>
                <td valign="top">
                    <label for="<%= this.txtServerAliases.ClientID %>" class="info">
                        Alternative names for this host,<br />e.g. <em>go-mono.net,go-mono.org,www.go-mono.com</em></label>
                    <asp:CompareValidator
                        ID="cmpSeverAlias" 
                        runat="server" 
                        ValidationGroup="grpVhost" 
                        ErrorMessage="Not all server aliases have been added.  Click the 'Add' button to include server alias."
                        ControlToValidate="txtSeverAlias"
                        Operator="Equal"
                        Display="None"
                        ValueToCompare=""></asp:CompareValidator>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div 
                        id="lstServerAliases" 
                        sourcefield="<%= this.txtSeverAlias.ClientID %>" 
                        valuesfield="<%= this.txtServerAliases.ClientID %>"></div>
                    <table id="tblServerAliases" border="0" cellpadding="1" cellspacing="0">
                    
                    </table>
                </td>
            </tr>
            <tr>
                <td colspan="2">  
                    <label for="<%= this.txtServerAdmin.ClientID %>" class="textfield">
                        Server Admin</label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox 
                        ID="txtServerAdmin" 
                        ValidationGroup="grpVhost" 
                        CssClass="textfield" 
                        runat="server"></asp:TextBox>
                </td>
                <td>
                    <label for="<%= this.txtServerAdmin.ClientID %>" class="info">
                        Email address server will include in error messages</label>
                    <asp:RegularExpressionValidator
                        ID="regexServerAdmin" 
                        ValidationGroup="grpVhost"
                        ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*" 
                        ControlToValidate="txtServerAdmin" 
                        ErrorMessage="Server Admin must be a valid Email Address" 
                        Display="None"
                        runat="server"></asp:RegularExpressionValidator>
                </td>
            </tr>
            <tr>
                <td colspan="2">  
                    <label for="<%= this.txtVhostDocumentRoot.ClientID %>" class="textfield">
                        Path to Document Root<span class="required">*</span></label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox 
                        ID="txtVhostDocumentRoot" 
                        ValidationGroup="grpVhost" 
                        CssClass="textfield" 
                        runat="server"></asp:TextBox>
                </td>
                <td>
                    <label for="<%= this.txtVhostDocumentRoot.ClientID %>" class="info">
                        Physical path to ASP.NET application</label>
                    <asp:RequiredFieldValidator 
                        ID="rqdVhostDocumentRoot" 
                        ValidationGroup="grpVhost" 
                        ControlToValidate="txtVhostDocumentRoot" 
                        ErrorMessage="Path to Document Root is Required"
                        Display="None"
                        runat="server"></asp:RequiredFieldValidator>
                </td>
            </tr>
        </table>
            
    </div>  
    
    <div id="divApplication" class="application">
        <h2>Application Details</h2>
        
        <table class="details">
            <tr>
                <td colspan="2">          
                    <label for="<%= this.txtApplicationName.ClientID %>" class="textfield">
                        Application Name<span class="required">*</span></label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox  
                        ID="txtApplicationName" 
                        ValidationGroup="grpApplication"
                        CssClass="textfield" 
                        runat="server"></asp:TextBox>
                    <asp:RequiredFieldValidator  
                        ID="rqdApplicationName" 
                        ValidationGroup="grpApplication"
                        ControlToValidate="txtApplicationName" 
                        ErrorMessage="Application Name is Required" 
                        Display="None"
                        runat="server"></asp:RequiredFieldValidator>
                </td>
                <td width="100%">&nbsp;</td>
            </tr>
            <tr>
                <td colspan="2">          
                    <label for="<%= this.txtAppDocumentRoot.ClientID %>" class="textfield">
                        Path to Document Root<span class="required">*</span></label>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <asp:TextBox 
                        ID="txtAppDocumentRoot"  
                        ValidationGroup="grpApplication"
                        CssClass="textfield" 
                        runat="server"></asp:TextBox>
                </td>
                <td>
                    <label for="<%= this.txtAppDocumentRoot.ClientID %>" class="info">
                        Physical path to ASP.NET application</label>
                    <asp:RequiredFieldValidator 
                        ID="rqdAppDocumentRoot"  
                        ValidationGroup="grpApplication"
                        ControlToValidate="txtAppDocumentRoot" 
                        ErrorMessage="Path to Document Root is Required" 
                        Display="None"
                        runat="server"></asp:RequiredFieldValidator>
                </td>
            </tr>
        </table>
                 
    </div>    
    
    <div class="section">
        <h2>Application Options</h2>
        <table class="details">
            <tr>
                <td>
                    <asp:CheckBox ID="chkDebug" runat="server" Text="Run Mono with debugging enabled" Checked="true" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="<%= this.chkDebug.ClientID %>" class="info">
                        Enables Mono to display line numbers in ASP.NET stack traces.  (Debug compilation must also be enabled in Web.config or page directive.)</label>
                </td>
            </tr>
            <tr>
                <td>
                    <asp:CheckBox ID="chkIomap" runat="server" Text="Enable Platform Abstraction" Checked="true" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="<%= this.chkIomap.ClientID %>" class="info">
                        Enable Mono's platform abstraction layer for file IO.  Makes file access case insensitive and treats backslashes (\) as slashes (/).<br />
                        (<em>Warning: Leaving platform abstraction enabled will negatively imapact performance</em>.)</label>
                </td>
            </tr>
            <tr>
                <td>
                    <asp:CheckBox ID="chkModDeflate" runat="server" Text="Enable mod_deflate" Checked="true" />
                </td>
            </tr>
            <tr>
                <td>
                    <label for="<%= this.chkModDeflate.ClientID %>" class="info">
                        Configure Apache mod_deflate to compress content before sending it to the client.</label>
                </td>
            </tr>
        </table>
    </div>
          
    <div class="section">  
        <h2>Generate mod_mono Configuration</h2> 
        <asp:ValidationSummary ID="ValidationSummary1" ValidationGroup="grpVhost" runat="server" />
        <asp:ValidationSummary ID="ValidationSummary2" ValidationGroup="grpApplication" runat="server" />   
        When the above form is complete, use the buttons below to preview and download your mod_mono configuration.
    </div>
    <div class="section"> 
        <asp:Button 
            ID="btnPreviewVhost" 
            CausesValidation="true" 
            ValidationGroup="grpVhost" 
            Text="Preview" 
            CssClass="vhost"
            onclick="btnPreview_Click" 
            runat="server" />
        <asp:Button 
            ID="btnPreviewApplication" 
            CausesValidation="true" 
            ValidationGroup="grpApplication" 
            Text="Preview" 
            CssClass="application"
            onclick="btnPreview_Click" 
            runat="server" />
        <span class="instructions">
            this configuration.</span>
            
        <asp:UpdateProgress ID="UpdateProgress1" runat="server">
            <ProgressTemplate>
                <span class="progress">Generating preview...</span>
            </ProgressTemplate>
        </asp:UpdateProgress>
            
        <asp:UpdatePanel ID="UpdatePanel1" runat="server" UpdateMode="Conditional" >
            <Triggers>
                <asp:AsyncPostBackTrigger ControlID="btnPreviewVhost" />
                <asp:AsyncPostBackTrigger ControlID="btnPreviewApplication" />
            </Triggers>
            <ContentTemplate>
                <asp:Panel ID="panelPreview" runat="server" Visible="false">
                    <textarea 
                        ID="textarea1" 
                        cols="200"
                        class="preview"
                        wrap="hard"><uc1:Config ID="Config1" runat="server" /></textarea><br />
                    <label class="info">
                        Copy and paste the preview configuration into an existing host or virtual host configuration file, or
                    </label>
                </asp:Panel>
            </ContentTemplate>
        </asp:UpdatePanel> 
    </div>
          
    <div class="section">              
        <asp:Button 
            ID="btnDownloadVhost" 
            CausesValidation="true" 
            ValidationGroup="grpVhost" 
            CssClass="vhost" 
            Text="Download" 
            onclick="btnDownload_Click"
            runat="server" />
        <asp:Button 
            ID="btnDownloadApplication" 
            CausesValidation="true" 
            CssClass="application" 
            Text="Download" 
            ValidationGroup="grpApplication" 
            runat="server" 
            onclick="btnDownload_Click" />
        <span class="instructions">
            this configuration to your apache config folder.<br />
            <label class="info">
                ( <em>/etc/apache2/conf.d/</em> on SUSE and openSUSE )</label>
        </span>
    </div>
    
</asp:Content>
