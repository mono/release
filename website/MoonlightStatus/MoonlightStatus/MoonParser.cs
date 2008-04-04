// MoonParser.cs created with MonoDevelop
// User: rhowell at 6:13 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Collections;
using System.IO;
using System.Net;
using System.Text;

namespace MoonlightStatus
{
	
	public class MoonParser
        {
                private static ArrayList lines = null;
                private static int cur = 0;

                private static string NextLine()
                {
                        if (cur < lines.Count)
                                return (string)lines[cur++];
                        else
                                return string.Empty;
                }
                private static string PeekLine()
                {
                        if (cur < lines.Count)
                                return (string)lines[cur];
                        else
                                return string.Empty;
                }

                public MoonParser()
                {

                }
                public static ArrayList ParseURL(string url)
                {
                        WebRequest req = HttpWebRequest.Create(url);
                        WebResponse resp = req.GetResponse();

                        Encoding encode = System.Text.Encoding.GetEncoding("utf-8");
                        StreamReader reader = new StreamReader(resp.GetResponseStream(),encode);

                        return ParseStream(reader);

                }

                public static ArrayList ParseFile(string filename)
                {
                        StreamReader reader = new StreamReader(filename);

                        return ParseStream(reader);
                }
                private static ArrayList ParseStream(StreamReader reader)
                {
                        string line = reader.ReadToEnd();
                        reader.Close();

                        lines = new ArrayList();
                        lines.AddRange(line.Split('\n'));
                        ArrayList newlines = new ArrayList();

                        //int curline = 0;
                        foreach(string s in lines)
                        {
                                if (s.Trim() != string.Empty)
                                {
                                        newlines.Add(s.Trim());
                                }
                        }
                        lines = newlines;


                        ArrayList sites = new ArrayList();

                        cur = 0;
                        while(PeekLine() != string.Empty)
                        {
                                sites.Add(ParseSite());
                        }

                        Console.WriteLine("Sites read: {0}",sites.Count);
                        return sites;
                }


                private static MoonSite ParseSite()
                {

                        string name = NextLine().Trim();
                        if (!name.ToLower().StartsWith("site:"))
                        {
                                Console.WriteLine("expected 'site:' but got {0}",name);
                        }

                        name = name.Substring(5).Trim();


                        string url = NextLine().Trim();
                        if (!url.ToLower().StartsWith("url:"))
                        {
                                Console.WriteLine("expected 'url:' but got {0}",url);
                        }
                        url = url.Substring(4).Trim();

                        string line = NextLine().Trim();
                        if (!line.ToLower().StartsWith("rating:"))
                        {
                                Console.WriteLine("expected 'rating:' but got {0}",line);
                        }
                        line = line.Substring(7);


                        //Console.WriteLine(line);
                        int rating = Convert.ToInt32(line.Trim());

                        //Console.WriteLine("creating new MoonSite");

                        MoonSite newsite = new MoonSite(name,url,rating);
                        while(PeekLine().Trim().StartsWith("*"))
                        {
                                newsite.Issues.Add(ParseIssue());
                        }

                        return newsite;
                }

                private static MoonIssue ParseIssue()
                {
                        //MoonIssue newissue = null;
                        int bugnum = 0;
                        string desc = NextLine().Trim();
                        if (!desc.StartsWith("*"))
                        {
                                Console.WriteLine("expected '*' but got {0}",desc);
                        }
                        desc = desc.Substring(1).Trim();
                        if(desc.IndexOf("Bug") >= 0)
                        //if (desc.Contains("Bug"))
                        {
                                string tmps = string.Empty;
                                try
                                {
                                        tmps = desc.Substring(desc.LastIndexOf("Bug") + 3);
                                        desc = desc.Substring(0,desc.LastIndexOf("Bug"));
                                        tmps = tmps.Trim();

                                        bugnum = Convert.ToInt32(tmps);
                                }
                                catch(Exception ex)
                                {
                                        Console.WriteLine(desc);
                                        Console.WriteLine(tmps);
                                        Console.WriteLine(ex);
                                        bugnum = 0;
                                }

                        }

                        return new MoonIssue(desc,bugnum);
                }

        }

}
