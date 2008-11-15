// Set a cookie for the users timezone

var today = new Date ()
var inaweek = new Date ()

// In seconds
var monobuild_tzo = today.getTimezoneOffset()*60*(-1)

inaweek.setTime (today.getTime () + (1000 * 60 * 60 * 24 * 7))
var expires = "; expires=" + inaweek.toGMTString ()

document.cookie = "monobuild_tzo=" + monobuild_tzo + expires

// Testing...
//document.write(monobuild_tzo)


// Figure out which set of check boxes to toggle and then toggle them all
function toggleCheckBoxes(checkboxName)
{
	var i = 0;

	var checkBox;

	if(checkboxName == document.buildform.build) {
		checkBox = document.buildform.linux;
	} 

	// If more than one build is selected
	if(checkboxName.length)
	{
		for(i = 0; i < checkboxName.length; i++)
		{
			checkboxName[i].checked = checkBox.checked;
		}
	}
	// Only one build is selected
	else
	{
		checkboxName.checked = checkBox.checked;
	}

}

