function selected32bitnightly ()
{
	document.getElementById ("nightlyi686row").style.display = '';
	document.getElementById ("nightlyx86_64row").style.display = 'none';
}

function selected64bitnightly ()
{
	document.getElementById ("nightlyi686row").style.display = 'none';
	document.getElementById ("nightlyx86_64row").style.display = '';
}

function selected32bit ()
{
	document.getElementById ("i586row").style.display = '';
	document.getElementById ("x86_64row").style.display = 'none';
}

function selected64bit ()
{
	document.getElementById ("i586row").style.display = 'none';
	document.getElementById ("x86_64row").style.display = '';
}

function selectchrome ()
{
	document.getElementById ("nightlyi686rowfirefox").style.display = 'none';
	document.getElementById ("nightlyx86_64rowfirefox").style.display = 'none';
}

function selectfirefox ()
{
	document.getElementById ("nightlyi686rowchrome").style.display = 'none';
	document.getElementById ("nightlyx86_64rowchrome").style.display = 'none';
}

