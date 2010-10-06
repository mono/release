using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Net.Mail;

public partial class contact_Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {

    }
    protected void btnSubmit_Click(object sender, EventArgs e)
    {
        if (!Page.IsValid)
            return;

        SmtpClient c = new SmtpClient("localhost");
        string from = email.Text;
        string to = "monotools@novell.com";
        string body = String.Format("Sender: {0}\nIP: {1}\n\nMessage:\n\n{2}", email.Text, Request.UserHostAddress, msg.Text);
        string subject = String.Format("Mono Tools {0} from {1}", subjectctl.SelectedItem.Text, email.Text);

        MailMessage mail_message = new MailMessage(from, to, subject, body);
        try
        {
            mail_message.ReplyTo = new MailAddress(email.Text);
        }
        catch { }

        c.Send(mail_message);
        Server.Transfer("ThankYou.aspx");
    }
}