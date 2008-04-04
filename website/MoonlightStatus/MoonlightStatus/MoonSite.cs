// MoonSite.cs created with MonoDevelop
// User: rhowell at 6:13 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Collections;

namespace MoonlightStatus
{
	
	public class MoonSite
        {
                public string Name;
                public string URL;
                public int Rating;
                public ArrayList Issues = null;

                static string star = "<img src=\"http://www.mono-project.com/files/2/2e/Star.png\"/>";
                static string accept = "<img src=\"http://www.mono-project.com/files/2/22/Accept.png\"/>";
                static string help ="'<img src=\"http://www.mono-project.com/files/a/aa/Help.png\"/>";
                static string delete = "<img src=\"http://www.mono-project.com/files/8/8c/Delete.png\"/>";


                public MoonSite(string name, string url, int rating)
                {
                        Name = name;
                        URL = url;
                        Rating = rating;
                        Issues = new ArrayList();

                }
                public override string ToString ()
                {
                        string s = Name;
                        foreach (MoonIssue issue in Issues)
                        {
                                s += issue.ToString();
                        }
                        return s;
                }
                private string GetRating()
                {
                        string images = string.Empty;
                        switch(this.Rating)
                        {
                                case 0:
                                        images = delete;
                                break;
                                case 1:
                                images = star;
                                break;
                        case 2:
                                images = star + star;
                                break;
                        case 3:
                                images = star + star + star;
                                break;
                        case 4:
                                images = accept;
                                break;
                        default:
                                images = help;
                                break;

                        }

                        string html = string.Format("<td> {0} {1} </td>",this.Rating, images);
                        return html;


                }

                public string ToHtml()
                {
                        string html = string.Format("\n<tr>{0}\n",GetRating());
                        html += string.Format("<td><a href=\"{0}\" class=\"external\" title=\"{0}\" rel=\"nofollow\">{1}</a></td>\n",URL,Name);
                        html += "<td><ul>\n";
                        foreach (MoonIssue issue in Issues)
                        {
                                html += issue.ToHTML();
                        }
                        html += "</ul></td></tr>\n";
                        return html;
                }
        }

}
