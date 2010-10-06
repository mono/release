<%@ Page Title="" Language="C#" MasterPageFile="~/FeaturePage.master" AutoEventWireup="true"
    CodeFile="Default.aspx.cs" Inherits="contact_Default" %>
<%@ Register TagPrefix="recaptcha" Namespace="Recaptcha" Assembly="Recaptcha" %>

<asp:Content ID="Content1" ContentPlaceHolderID="title" runat="Server">
    Mono Tools for Visual Studio - Contact
</asp:Content>
<asp:Content ID="Content3" ContentPlaceHolderID="featurecontent" runat="Server">
    <div class="grid_10" style="width: 600px;">
        <h1>
            Contact Mono Tools Team</h1>
        <asp:RequiredFieldValidator ControlToValidate="email" ID="rqdEmail" runat="server"
            Display="Dynamic" ErrorMessage="Please enter an email address"></asp:RequiredFieldValidator>
        <asp:RegularExpressionValidator ControlToValidate="email" ID="regexEmail" runat="server"
            Display="Dynamic" ErrorMessage="Please enter a valid email address" ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
        <div id="contact-form-container">
            <br />
            <table id="contact-form">
                <tr>
                    <th>
                        Email Address:
                    </th>
                    <td>
                        <asp:TextBox name="email" ID="email" runat="server" Style="width: 300px" />
                    </td>
                </tr>
                <tr>
                    <th>
                        Subject:
                    </th>
                    <td>
                        <asp:DropDownList ID="subjectctl" runat="server" Style="width: 300px">
                            <asp:ListItem>General Comment</asp:ListItem>
                            <asp:ListItem>Product Activation Issue</asp:ListItem>
                            <asp:ListItem>Problem Report</asp:ListItem>
                            <asp:ListItem>Web Site Issues</asp:ListItem>
                            <asp:ListItem>Licensing</asp:ListItem>
                            <asp:ListItem>Enterprise Support</asp:ListItem>
                            <asp:ListItem>Suggestion</asp:ListItem>
                            <asp:ListItem>Consulting and Tech Support</asp:ListItem>
                            <asp:ListItem>Criticism</asp:ListItem>
                        </asp:DropDownList>
                    </td>
                </tr>
                <tr class="message-box">
                    <th class="top-align">
                        Message:
                    </th>
                    <td>
                        <asp:TextBox style="height: 200px;width:500px;" name="msg" ID="msg" TextMode="Multiline" runat="server" />
                    </td>
                </tr>
                <tr>
                    <th class="top-align" style="padding-top: 15px">
                        Are you<br />
                        human?
                    </th>
                    <td style="padding-top: 15px">
                        <recaptcha:recaptchacontrol id="recaptcha" runat="server" theme="clean" publickey="6Lf03LsSAAAAAMGKxtRtNeIoapcrsEp6HpjiB_la"
                            privatekey="6Lf03LsSAAAAAGscd1W_uKhiDjKPOY1_noznZ8GJ" />
                    </td>
                </tr>
                <tr>
                    <th>
                        &nbsp;
                    </th>
                    <td style="padding-top: 15px">
                        <asp:Button Text="Send Inquiry" runat="server" ID="btnSubmit" 
                            onclick="btnSubmit_Click" />
                        <asp:Label ID="report" runat="server" />
                    </td>
                </tr>
            </table>
        </div>
    </div>
</asp:Content>
