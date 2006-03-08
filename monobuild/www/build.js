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

