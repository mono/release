using System;
using System.Collections.Generic;
using System.Collections.Specialized;
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
    protected void btnDownload_Click(object sender, ImageClickEventArgs e)
    {
        Page.Validate();
        if (Page.IsValid)
        {
           try
           {
                EnsureFileNamesAndConfig (Request);
                StoreFormData ();

                PostToEloqua();
            }
            catch (Exception ex)
            {
                //should probably log something
                throw;
            }
            finally
            {
                //but we'll try to let people download anyways.
                HttpResponse response = Response;
                response.ContentType = "application/octet-stream";
                response.AppendHeader("Content-Disposition", 
                    String.Format("attachment; filename={0}", dl_name));
                response.TransmitFile (real_path);
                response.End();
            }
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


    void StoreFormData()
    {
        using (IDbConnection cnc = new MySqlConnection())
        {
            cnc.ConnectionString = cnc_string;
            cnc.Open();
            IDbCommand cmd = cnc.CreateCommand();
            cmd.CommandText = "INSERT INTO trial_emails (trial_id, email, first_name, last_name, organization, app_type, IP, ts) VALUES (null, ?email, ?first_name, ?last_name, ?organization, ?app_type, ?ip, null)";
            
            AddParameter(cmd, "email", txtEmail.Text.Trim());
            AddParameter(cmd, "first_name", txtFirstName.Text.Trim());
            AddParameter(cmd, "last_name", txtLastName.Text.Trim());
            AddParameter(cmd, "organization", txtOrg.Text.Trim());
            AddParameter(cmd, "app_type", ddlAppType.SelectedValue);
            AddParameter(cmd, "ip", Request.UserHostAddress);

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


    static DateTime last_modif;
    static string cnc_string;
    static string dl_name;
    static string real_path;
    static object _lock = new object();
    static void EnsureFileNamesAndConfig(HttpRequest request)
    {
        lock (_lock)
        {
            string path = request.MapPath("~/download/version.txt");
            DateTime dt = File.GetLastWriteTime(path);
            if (last_modif < dt)
            {
                NameValueCollection col = System.Configuration.ConfigurationManager.AppSettings;
                cnc_string = col["MonoVsDB"];
                if (String.IsNullOrEmpty(cnc_string))
                    throw new ApplicationException("Missing connection string from configuration file.");
                last_modif = dt;
                string version = null;
                using (StreamReader reader = new StreamReader(path))
                {
                    version = reader.ReadToEnd().Trim();
                }
                real_path = request.MapPath(String.Format("~/download_area/monovs_{0}.msi", version));
                dl_name = String.Format("monovs_{0}.msi", version);
            }
        }
    }



}
