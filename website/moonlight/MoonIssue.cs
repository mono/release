// MoonIssue.cs created with MonoDevelop
// User: rhowell at 6:13 PM 4/3/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using System.Collections;

namespace MoonlightStatus
{
	[Serializable]
	public class MoonIssue
    {
        static string bugzilla = "http://bugzilla.novell.com/show_bug.cgi?id=";
		static string greaseMonkeyUrl = "http://mono-project.com/MoonlightQuirks#GreaseMonkey";
        public string Desc;
        public int BugNum;
        public MoonIssue(string desc):this(desc,0)
        {
        }
        public MoonIssue(string desc, int bugNumber)
        {
                Desc = desc;
                BugNum = bugNumber;
        }

        public override string ToString()
        {
                return string.Format("{0} Bug {1}\n",Desc,BugNum);
        }
        public string ToHTML()
        {
			if (this.Desc.Contains("GreaseMonkey")) {
				Desc = Desc.Replace("GreaseMonkey",String.Format("<a href='{0}'>GreaseMonkey</a>",greaseMonkeyUrl));
			}

            string bughtml = string.Empty;
            if (this.BugNum > 0) {
                    //string bug_url = bugzilla + this.BugNum;
                    
                    //Was trying to do a mouse-over-get-bug-title-from-bugzilla thingy
                    //html = string.Format("<li><a href=\"{0}\" onmouseover=\"popUp(event,\'tip{1}\')\"",bug_url,this.BugNum);
                    //html += string.Format("onmouseout=\"popUp(event,\'tip{0}\')\" onclick=return false\">Bug {0}</a>",this.BugNum);
                    //html += string.Format("<div id=\"tip{0}\" class=\"tip\">{1}</div></li>",this.BugNum,this.Desc);
                    
                    bughtml = string.Format("<a href=\"{0}\">Bug {1}</a>",(bugzilla + this.BugNum),this.BugNum);
            }
            return string.Format("<li>{0} {1}</li>",this.Desc,bughtml);
			
        }

    }

}
