using System;
using System.Net.Mail;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.HtmlControls;

namespace ModMonoConfig
{
    public partial class Default : System.Web.UI.Page
    {

        public string ServerAdmin { get { return txtServerAdmin.Text.Trim(); } }
        public string ServerName { get { return txtServerName.Text.Trim(); } }


        public string[] ServerAliases { 
            get { 
                return this.txtServerAliases.Text.Split(",".ToCharArray(), StringSplitOptions.RemoveEmptyEntries); 
            } 
        }

        public string ApplicationName { get { return this.txtApplicationName.Text.Trim(); } }
        
        public string DocumentRoot { 
            get 
            { 
                return this.IsVirtualHost ?
                    this.txtVhostDocumentRoot.Text.Trim() : this.txtAppDocumentRoot.Text.Trim();
            }
        }

        public bool EnablePlatformAbstraction { get { return chkIomap.Checked; } }
        public bool EnableDebug { get { return chkDebug.Checked; } }
        public bool IsVirtualHost { get { return this.radVhost.Checked; } }
        public bool EnableModDeflate { get { return chkModDeflate.Checked; } }
        public bool IsDownload { get; set; }

        protected void Page_Load(object sender, EventArgs e) {
            this.txtServerName.Attributes["onchange"] = String.Format(
                "txtServerName_Changed('{0}', '{1}', '{2}')",
                this.txtServerName.ClientID,
                this.txtServerAdmin.ClientID,
                this.txtVhostDocumentRoot.ClientID);

            this.txtApplicationName.Attributes["onchange"] = String.Format(
                "txtApplicationName_Changed('{0}', '{1}')",
                this.txtApplicationName.ClientID,
                this.txtAppDocumentRoot.ClientID);

            this.Page.ClientScript.RegisterStartupScript(
                Page.GetType(),
                "setAppType",
                String.Format(
                    "<script language=\"javascript\" type=\"text/javascript\">rebuildAliasList();radApplicationType_Click(document.getElementById('{0}'));</script>",
                    this.radVhost.ClientID));
        }

        protected void btnDownload_Click(object sender, EventArgs e) {
            if (sender is Button)
            {
                Button b = (Button)sender;
                Page.Validate(b.ValidationGroup);
                if (this.Page.IsValid)
                {
                    Server.Transfer("~/ConfigHost.aspx");
                }
            }
        }

        protected void btnPreview_Click(object sender, EventArgs e) {
            if (sender is Button)
            {
                Button b = (Button)sender;
                Page.Validate(b.ValidationGroup);
                if (this.Page.IsValid)
                {
                    this.panelPreview.Visible = true;
                }
            }
        }
    }
}
