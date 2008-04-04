// MoonlightStatus.aspx.cs created with MonoDevelop
// User: rhowell at 6:03 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Web;
using System.Web.UI;
using System.Collections;

namespace MoonlightStatus
{
	
	
	public partial class MoonlightStatus : System.Web.UI.Page
	{
        //protected System.Web.UI.HtmlControls.HtmlGenericControl MoonContent;

        protected void Page_Load(object sender, EventArgs e)
        {
                //string filename = "data.txt";
                string url = "http://anonsvn.mono-project.com/source/trunk/moon/demo-status.txt";

                ArrayList sites = MoonParser.ParseURL(url);


                string html = getHeader();
                foreach(MoonSite site in sites)
                {
                        html += site.ToHtml();
                }

                html += getFooter();

                MoonContent.InnerHtml = html;


        }

        private string getHeader()
        {
                string html = "<table class=\"wikitable\" border=\"1\" cellpadding=\"0\">";
                html += "<tr > <th width=\"100\"> Rating </th><th width=\"200\"> Name </th><th class=\"unsortable\"";
                html += "width=\"600\"> Issues </th></tr>";


                return html;
        }
        private string getFooter()
        {
                return "</table>\n";
        }

    }

}
