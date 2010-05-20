using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class _default : System.Web.UI.MasterPage
{
    protected void Page_Load(object sender, EventArgs e)
    {
        
        if (Request.ServerVariables["SCRIPT_NAME"] == "/Default.aspx") {
          header.Visible = false; 
          footer.Visible = true;
        } else if (Request.QueryString["nc"]!="") { //headers called inline with fancybox
          header.Visible = false; 
          footer.Visible = false;
        }
        
        
        if (!Page.IsPostBack)
        {
            HttpCookie refCookie = Request.Cookies["mt_ref"];
            if (refCookie == null || String.IsNullOrEmpty(refCookie.Value))
            {
                string referrer = Request.ServerVariables["HTTP_REFERER"] ?? "";

                if (!referrer.Contains("go-mono.com"))
                {
                    Response.Cookies.Add(new HttpCookie("mt_ref", referrer));
                }
            }

            HttpCookie urlCookie = Request.Cookies["mt_url"];
            if (urlCookie == null || String.IsNullOrEmpty(urlCookie.Value))
            {
                Response.Cookies.Add(new HttpCookie("mt_url", Request.Url.ToString()));
            }
        }
    }
}
