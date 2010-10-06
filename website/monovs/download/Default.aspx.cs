using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Configuration;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.Common;
using System.IO;
using MySql.Data.MySqlClient;

public partial class download_Default : System.Web.UI.Page
{

    protected void Page_Load(object sender, EventArgs e)
    {
        if ("1" == (Request.QueryString["partner"] ?? ""))
        {
            tblForm.Visible = false;
        }
    }

    protected void btnDownloadMsi_Click(object sender, EventArgs e)
    {
        StartDownload("msi");
    }

    protected void btnDownloadVsix_Click(object sender, EventArgs e)
    {
        StartDownload("vsix");
    }


    private void StartDownload(string installerType)
    {

        Page.Validate();
        if (Page.IsValid)
        {
            string filename = ConfigurationManager.AppSettings[string.Format("MonoTools_{0}", installerType)];
            if (tblForm.Visible)
            {
                StoreFormData(filename);

                try
                {
                    PostToEloqua();
                }
                catch (Exception ex)
                {
                    //should probably log something
                }
            }

            //but we'll try to let people download either way
            HttpResponse response = Response;
            response.ContentType = "application/octet-stream";
            response.AppendHeader("Content-Disposition",
                String.Format("attachment; filename={0}", filename));
            response.TransmitFile(Request.MapPath(String.Format("~/download_area/{0}", filename)));
            response.End();
        }
    }

    private void PostToEloqua()
    {
        PostSubmitter post = new PostSubmitter();

        post.Type = PostSubmitter.PostTypeEnum.Post;
        post.Url = "http://now.eloqua.com/e/f2.aspx";
        post.PostItems.Add("elqFormName", "MTVSForm");
        post.PostItems.Add("elqSiteID", "1163");
        post.PostItems.Add("Email", txtEmail.Text.Trim());
        post.PostItems.Add("FirstName", txtFirstName.Text.Trim());
        post.PostItems.Add("LastName", txtLastName.Text.Trim());
        post.PostItems.Add("Org", txtOrg.Text.Trim());
        post.PostItems.Add("AppType", ddlAppType.SelectedValue);
        post.PostItems.Add("elqCustomerGUID", elqCustomerGUID.Value);
        post.PostItems.Add("elqCookieWrite", elqCookieWrite.Value);

        // Add more fields here           

        string result = post.Post();
    }


    void StoreFormData(string filename)
    {
        using (IDbConnection cnc = new MySqlConnection())
        {
            cnc.ConnectionString = ConfigurationManager.AppSettings["MonoVsDB"];
            cnc.Open();
            IDbCommand cmd = cnc.CreateCommand();
            cmd.CommandText = "INSERT INTO trial_emails (trial_id, email, first_name, last_name, organization, app_type, IP, referrer, url, filename, ts) VALUES (null, ?email, ?first_name, ?last_name, ?organization, ?app_type, ?ip, ?referrer, ?url, ?filename, null)";
            
            AddParameter(cmd, "email", txtEmail.Text.Trim());
            AddParameter(cmd, "first_name", txtFirstName.Text.Trim());
            AddParameter(cmd, "last_name", txtLastName.Text.Trim());
            AddParameter(cmd, "organization", txtOrg.Text.Trim());
            AddParameter(cmd, "app_type", ddlAppType.SelectedValue);
            AddParameter(cmd, "ip", Request.UserHostAddress);
            AddParameter(cmd, "referrer", Request.Cookies["mt_ref"] != null ? Request.Cookies["mt_ref"].Value : "");
            AddParameter(cmd, "url", Request.Cookies["mt_url"] != null ? Request.Cookies["mt_url"].Value : "");
            AddParameter(cmd, "filename", filename);

            cmd.ExecuteNonQuery();
        }
    }

    static IDataParameter AddParameter(IDbCommand cmd, string name, object val)
    {
        IDataParameter p = cmd.CreateParameter();
        p.ParameterName = name;
        p.Value = val;
        cmd.Parameters.Add(p);
        return p;
    }
}
