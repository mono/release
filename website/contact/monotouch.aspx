<%@ Page Language="C#" Src="core.cs" %>
<%@ Import Namespace="System.Net.Mail" %>
<%@ Register TagPrefix="recaptcha" Namespace="Recaptcha" Assembly="Recaptcha" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" dir="ltr">
  <head>
    <script src="http://www.google-analytics.com/urchin.js" type="text/javascript"> </script>
    <script type="text/javascript">
        _uacct = "UA-76510-1";
        urchinTracker();
    </script>

    <link rel="stylesheet" href='MonoTouchForm.css' type="text/css" media="screen" /> 
  </head>
  <body>
<script runat="server">
void btnSubmit_OnClick (object o, EventArgs a)
{
   if (!Page.IsValid)
      return;

   SmtpClient c = new SmtpClient ("localhost");
   string from = email.Text;
   string to   = "monotouch@novell.com"; 
   string body = String.Format ("Sender: {0}\nIP: {1}\n\nMessage:\n\n{2}", email.Text, Request.UserHostAddress, msg.Text);
   string subject = String.Format ("MonoTouch {0} from {1}", subjectctl.SelectedItem.Text, email.Text);

   MailMessage mail_message = new MailMessage (from, to, subject, body);
   try {
       mail_message.ReplyTo = new MailAddress (email.Text);
   } catch {}

   c.Send (mail_message);
   Server.Transfer ("thankyou-monotouch.aspx");
}
   
</script>

<form runat="server">
  <asp:RequiredFieldValidator ControlToValidate="email" ID="rqdEmail" runat="server"  Display="Dynamic" 
    ErrorMessage="Please enter an email address"></asp:RequiredFieldValidator>
  <asp:RegularExpressionValidator ControlToValidate="email" ID="regexEmail" runat="server" Display="Dynamic"
    ErrorMessage="Please enter a valid email address" ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
  <div id="contact-form-container">
  <br /> 
  <table id="contact-form">
    <tr>
      <th>Email Address:</th>
      <td><asp:TextBox name="email" id="email" runat="server" style="width: 300px"/></td>
    </tr>
    <tr>
      <th>Subject:</th>
      <td>
        <asp:DropDownList ID="subjectctl" runat="server" style="width: 300px">
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
      <th class="top-align">Message:</th>
      <td><asp:TextBox name="msg" id="msg" TextMode="Multiline" runat="server"/></td>
    </tr>
    <tr>
      <th class="top-align" style="padding-top: 15px">Are you<br/>human?</th>
      <td style="padding-top: 15px">
        <recaptcha:RecaptchaControl
            ID="recaptcha"
            runat="server"
            Theme="clean"
            PublicKey="6LevKgMAAAAAAFBU2BuqpQOkn2fUnJE_PLVTNj0u"
            PrivateKey="6LevKgMAAAAAAI4NimISmjEd4FabHTNLwhTBu4gW" />
	
      </td>
    </tr>
    <tr>
      <th>&nbsp;</th>
      <td style="padding-top: 15px"> 
        <asp:Button Text="Send Inquiry" runat="server" ID="btnSubmit" OnClick="btnSubmit_OnClick" />
        <asp:Label id="report" runat="server"/>
      </td>
    </tr>
  </table>
  </div>
</form>

</body>
</html>




