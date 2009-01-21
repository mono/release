// MoonlightStatus.aspx.cs created with MonoDevelop
// User: rhowell at 6:03 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Web;
using System.Web.UI;
using System.Collections;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;


namespace MoonlightStatus
{
	
	
	public partial class MoonlightStatus : System.Web.UI.Page
	{
		static string timeStampFile = "MoonlightStatus_timestamp";
		static string cacheFile = "MoonlightStatus_cache";
		static string url1 = "http://anonsvn.mono-project.com/source/branches/moon-1-0/demo-status.txt";
		static string url2 = "http://anonsvn.mono-project.com/source/trunk/moon/demo-status.txt";
		string url = string.Empty;
		//static string url = "http://rhowell.provo.novell.com/demo-status.txt";
		string version = "1.0";

        protected void Page_Load(object sender, EventArgs e)
        {
			url = url1;
			
			if (Request["v"] == "2") {
				url = url2;
				version = "2.0";
				Console.WriteLine("Using 2.0");
			}

			Console.WriteLine("using url = " + url);
			ArrayList sites = null;
			DateTime now = DateTime.Now;
			//if (GetLastUpdateTime().AddMinutes(30) > now) // If cache is newer than 30 mins, use it.
			//{
			//	Console.WriteLine("Reading data from cache");
			//	sites = GetDataFromFile();
			//}
			//else
			//{
				Console.WriteLine("Reading data from url");
				//UpdateTimeStamp(now);
				sites = MoonParser.ParseURL(url);
				//WriteDataToFile(sites);
				
			//}
			

            string html = getHeader();
            foreach(MoonSite site in sites)
            {
                    html += site.ToHtml();
            }

            html += getFooter();

            MoonContent.InnerHtml = html;


        }

		private DateTime GetLastUpdateTime()
		{
			DateTime lastupdate = DateTime.MinValue;
			
			if (File.Exists(timeStampFile))
			{
				Console.WriteLine("Found timestamp file");
				StreamReader reader = new StreamReader(timeStampFile);
				string line = reader.ReadLine();
				reader.Close();
				line = line.Trim();
				
				lastupdate = new DateTime(Convert.ToInt64(line));
			}
			else
			{
				Console.WriteLine("no timestamp file exists");
			}
			return lastupdate;
		}

		//This method reads serialized data (an ArrayList) from file. Data is not cached as text!
		private ArrayList GetDataFromFile()
		{
			ArrayList list = null;
			if (File.Exists(cacheFile))
			{
			
				FileStream reader = new FileStream(cacheFile,FileMode.Open,FileAccess.Read);
				IFormatter formatter = new BinaryFormatter();
				list = (ArrayList)formatter.Deserialize(reader);
				reader.Close();
			}
			else
			{
				//get data from url
				UpdateTimeStamp(DateTime.Now);
				list = MoonParser.ParseURL(url);
				WriteDataToFile(list);
			}
			
			return list;
			
		}
		
		//This method serializes the ArrayList to file. Data is not cached as text!
		private void WriteDataToFile(ArrayList list)
		{
			try
			{
				FileStream writer = new FileStream(cacheFile,FileMode.Create,FileAccess.Write,FileShare.None);
				IFormatter formatter = new BinaryFormatter();
				formatter.Serialize(writer,list);
				writer.Close();
			}
			catch
			{
				//don't cache
			}
			
		}
		private void UpdateTimeStamp(DateTime time)
		{
			try
			{
				
				StreamWriter writer = new StreamWriter(timeStampFile);
				writer.WriteLine(time.Ticks);
				writer.Close();
			}
			catch
			{
			}
			
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
