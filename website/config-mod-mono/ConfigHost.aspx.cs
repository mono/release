using System;
using System.Collections.Generic;
using System.Web;

namespace ModMonoConfig
{
    public partial class ConfigHost : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (Context.Handler is Default)
            {
                Default handler = (Default)Context.Handler;

                HttpContext.Current.Response.ContentType = "application/octet-stream";

                HttpContext.Current.Response.AddHeader(
                  "Content-Disposition",
                  String.Format("inline; filename={0}.conf",
                    handler.IsVirtualHost ? handler.ServerName : handler.ApplicationName));

            }
        }
    }
}
