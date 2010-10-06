using System;
using System.Collections.Generic;
using System.Text;
using System.Web;

namespace ModMonoConfig
{
    public partial class Config : System.Web.UI.UserControl
    {
        public Config()
        {
            serverAliases = new List<string>();
        }

        public string ServerAdmin { get; set; }
        public string ServerName { get; set; }
        public string ApplicationName { get; set; }
        public string DocumentRoot { get; set; }
        public string MonoServerAlias { get; set; }

        public bool EnablePlatformAbstraction { get; set; }
        public bool EnableDebug { get; set; }
        public bool EnableModDeflate { get; set; }
        public bool IsVirtualHost { get; set; }

        private List<string> serverAliases;

        public void AddServerAlias(string serverAlias) {
            if (!serverAliases.Contains(serverAlias))
                serverAliases.Add(serverAlias);
        }

        public void RemoveServerAlias(string serverAlias)
        {
            if (serverAliases.Contains(serverAlias))
                serverAliases.Remove(serverAlias);
        }

        protected string FormattedServerAliases() 
        {
            StringBuilder sb = new StringBuilder();
            foreach (string alias in serverAliases) {
                sb.AppendFormat("\n  ServerAlias {0}", alias.Trim());
            }
            return sb.ToString();
        }

        protected override void Render(System.Web.UI.HtmlTextWriter writer)
        {
            base.Render(writer);
        }

        protected void Page_Load(object sender, EventArgs e)
        {
            if (Context.Handler is Default) {
                Default handler = (Default)Context.Handler;

                this.IsVirtualHost = handler.IsVirtualHost;
                if (this.IsVirtualHost)
                {
                    this.ServerAdmin = handler.ServerAdmin;
                    this.serverAliases.AddRange(handler.ServerAliases);
                    this.ServerName = handler.ServerName;
                }
                else
                {
                    this.ApplicationName = handler.ApplicationName;
                }
                this.DocumentRoot = handler.DocumentRoot;

                this.EnablePlatformAbstraction = handler.EnablePlatformAbstraction;
                this.EnableDebug = handler.EnableDebug;
                this.EnableModDeflate = handler.EnableModDeflate;

                if (String.IsNullOrEmpty(this.MonoServerAlias)) this.MonoServerAlias = this.ApplicationName;
                if (String.IsNullOrEmpty(this.MonoServerAlias)) this.MonoServerAlias = this.ServerName;
            }
        }
    }
}