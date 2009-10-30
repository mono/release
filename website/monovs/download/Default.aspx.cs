using System;
using System.Collections.Generic;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

public partial class download_Default : System.Web.UI.Page
{
    protected void Page_Load(object sender, EventArgs e)
    {
        if ("1" == (Request.QueryString["partner"] ?? ""))
        {
            tblForm.Visible = false;
        }
    }
}
