
function loadpage()
{
   //window.status = "Page is loaded";
	/* Unselect other items */
	for (i = 0; i < data.platforms.length; i++)
	{
		document.getElementById("td"+i).style.background = "none";
		document.getElementById("td"+i).style.border = "1px solid #ffffff";
	}

	// Clean out the html for steps after 1
	document.getElementById("step2").innerHTML = "";
	document.getElementById("step3").innerHTML = "";
	document.getElementById("step4").innerHTML = "";
}

function mouseOver(n)
{
	/* Draw a temporary border on any mouseover box that isn't already selected */
	if (document.getElementById("rb"+n)) // && !document.getElementById("rb"+n).checked)
	{
		document.getElementById("td"+n).style.border = "1px solid #aaa";
	}
}

function mouseOut(n)
{
	/* After the mouseover, remove a temporary border on any box that isn't already selected */
	if (document.getElementById("rb"+n) && !document.getElementById("rb"+n).checked)
	//if (document.getElementById("rb"+n))
	{
		document.getElementById("td"+n).style.border = "1px solid #ffffff";
	}
}

function selected(os_num)
{
	/* Highlight and select the chosen item */
	document.getElementById("td"+os_num).style.border = "1px solid #aaa";
	document.getElementById("td"+os_num).style.background = "#eee";

	/* Unselect other items */
	for (i = 0; i < data.platforms.length; i++)
		if (i != os_num)
		{
			document.getElementById("td"+i).style.background = "none";
			document.getElementById("td"+i).style.border = "1px solid #ffffff";
		}

	// Clean out the html for steps after 1
	document.getElementById("step2").innerHTML = "";
	document.getElementById("step3").innerHTML = "";
	document.getElementById("step4").innerHTML = "";

	if (data.platforms[os_num].name != "Other")
	{
		if ((data.platforms[os_num].version.length == 1) &&
		    (data.platforms[os_num].version[0].arch.length == 1))
		{
			download_step("2", os_num, 0, 0);
		}
		else
		{
			version_step(os_num);
		}
	}
	else
	{
		unsupported_step(os_num);
	}
}

function UnsupMouseOver(n)
{
	/* Draw a temporary border on any mouseover box that isn't already selected */
	if (document.getElementById("unsuprb"+n)) // && !document.getElementById("unsuprb"+n).checked)
	{
		document.getElementById("unsuptd"+n).style.border = "1px solid #aaa";
	}
}

function UnsupMouseOut(n)
{
	/* After the mouseover, remove a temporary border on any box that isn't already selected */
	if (document.getElementById("unsuprb"+n) && !document.getElementById("unsuprb"+n).checked)
	//if (document.getElementById("rb"+n))
	{
		document.getElementById("unsuptd"+n).style.border = "1px solid #ffffff";
	}
}

function unsupported_step(os_num)
{
	var html = "<h2>2. Mono for Unsupported or Community-Supported Distribution</h2>";
	html += "<p>Novell does not offer support for your distribution. A number of distributions are supported by their own communities instead. Please select your platform below:</p><table class=\"os\"><tr>";

	for(i=0;i<data.platforms[os_num].version.length;i++)
	{
		html += "<td class='os' id='unsuptd"+i+"'>";
		html += "<div class='os' onMouseOver='UnsupMouseOver("+i+")' onMouseOut='UnsupMouseOut("+i+")' onClick='location.href=\""+data.platforms[os_num].version[i].url+"\"'>";
		html += "<div class='os-rd'><input type='radio' name='os' id='unsuprb"+i+"' onClick='location.href=\""+data.platforms[os_num].version[i].url+"\"'></div>";
		html += "<div class='os-id'><img alt='"+data.platforms[os_num].version[i].name+"' src='"+data.platforms[os_num].version[i].icon+"'><br />"+data.platforms[os_num].version[i].name+"</div>";
		html += "</div></td>";
	}

	html += "</tr></table>";
	document.getElementById("step4").innerHTML = html;
}

function version_step(os_num)
{
	document.getElementById("step3").innerHTML = "";

	var html = "<h2>2. " + data.platforms[os_num].name  + " Version</h2>";
	html += "<br><select size='4' onchange=\"arch_step(" + os_num + ", this.options[this.options.selectedIndex].value)\">";

	for (i=0; i <  data.platforms[os_num].version.length; i++)
	{
		html += "<option value='" + i + "' style='cursor: pointer;'>" + data.platforms[os_num].version[i].name  + "</option>";
	}

	html += "</select><br><br>";
	document.getElementById("step2").innerHTML = html;
}

function arch_step(os_num, os_version)
{
	document.getElementById("step4").innerHTML = "";

	var html = "<h2>3. Processor Architecture</h2>";
	html += "<br><select size='4' onchange='download_step(\"4\", \"" + os_num + "\",\"" + os_version + "\", this.options[this.options.selectedIndex].value)'>";

	for (i=0; i <  data.platforms[os_num].version[os_version].arch.length; i++)
	{
		html += "<option value='" + i + "' style='cursor: pointer;'>" + data.platforms[os_num].version[os_version].arch[i].name + "</option>";
	}

	html += "</select>";
	document.getElementById("step3").innerHTML = html;
}

function download_step(step_number, os_num, ver_num, arch_num)
{
	if (data.platforms[os_num].name == "LiveCD")
		html = "<h2>" + step_number + ". Download Mono "+ data.platforms[os_num].name + "</h2>";
	else
		html = "<h2>" + step_number + ". Download Mono for "+ data.platforms[os_num].name + "</h2>";

	html += "<br><table>";
	if (data.platforms[os_num].version[ver_num].arch[arch_num].desc != "")
	{
		html += "<tr><td colspan='2'>" + data.platforms[os_num].version[ver_num].arch[arch_num].desc + "</tr>";
	}
	html += "<tr><td class='osicon'><img class='osicon' src='" + data.platforms[os_num].dlicon + "'></td><td>";
	html +=  data.platforms[os_num].version[ver_num].arch[arch_num].downloadText;
	//html += "<td>Mono for Windows, Gtk#, and XSP";
	//html += "<ul><li><a href='ftp://www.go-mono.com/archive/1.2.6/windows-installer/4/mono-1.2.6-gtksharp-2.10.2-win32-4.exe'>Mono 1.2.6_4 Setup</a></ul>";
	//html += "Only Gtk# for .NET: <ul><li><a href=' http://forge.novell.com/modules/xfmod/project/?gtks-inst4win'>SDK and Runtime</a></ul>";
	//html += "Mono Migration Analyzer: <ul><li><a href='http://mono-project.com/MoMA'>See the Mono Migration Analyzer page</a></ul>";
	html += "</td></tr></table>";

	document.getElementById("step" + step_number).innerHTML = html;
}
