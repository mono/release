<!--
  This script retrieves data from XML files and displays it on the web
-->
<html>
<head>
	<link rel="stylesheet" href="http://go-mono.com/monologue/monologue.css" type="text/css" />
	<style type=text/css>
		body { margin-top: 5px; margin-left: 12px; background: White;}
		body, p, table, th, tr, td, ol,  ul, li, textarea, option, input { font-family: "Trebuchet MS", Arial, Helvetica, Geneva, Swiss, SunSans-Regular;}
		p, ol,  ul, textarea, option, input {font-size: 0.9em;}
		th {font-size: 1em; margin-bottom: 0.1em;   padding: 1px; color: black; font-weight: bold; letter-spacing: 0.1em; text-align:left; text-indent: 0.5em; background-color: #DFDDDD;}
		body a {color: #039;}
		small {font-size: 0.75em;}

		/* Tab styles */
		.tabblue  {  font-size:  0.8em; color: white; background-color: #6B8899; font-weight: bold; text-align: center; white-space: nowrap; }
        	.tabblue a { text-decoration: none; color: white; }
		.tabputty  {  font-size: 0.8em; color: black; background-color:#DFDDD5; font-weight:bold; text-align:center; white-space: nowrap; }
	        .tabputty a { text-decoration: none;  color: black;}

	</style>
	<title>Mono Test Suite Results</title>
</head>
<body>
<h1>Mono Test Suite Results </h1>
<br>
<h3>Profiles</h3>
<?php
	ini_set("memory_limit", "20M");
	$distro = $_GET['distro'];
	$profile = $_GET['profile'];
	$profile_name = "default";
	if ($distro == "" && $profile == "") {
		$distro = 0;
		$profile = 0;
	}
	//If more distros are added, add more case blocks and add more tabs
#	print "<p><br><div id=1tab>";
	print "<table border=0 cellspacing=0  cellpadding=0><tr><td><img height=1 src=\"spacer.gif\" width=5 border=0></td>";
        switch ($profile) {
           case 0:
			$profile_name = "default";
			$profile = 0;
			//header("Location:");
			print "<td><img src=\"first_left_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap> <font size=2px>Default</td>";
		print "<td><img src=\"overlap_on_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=1&distro=$distro\"><font size=2px>2.0</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";
			break;
           case 1:
			$profile = 1;
			$profile_name = "net_2_0";
                        print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=0&distro=$distro\"><font size=2px>Default</a></td>";
                        print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap height=20><font size=2px>2.0</td><td><img src=\"last_right_on.gif\" border=0 height=20 width=18></td></tr>";
			$profile_name = "net_2_0";
			break;
        }
        print "</tr></table>";
        print "</tr></table><table border=1><tr><td colspan=3>";
	print "<p><br><div id=1tab>";
	print "<table border=0 cellspacing=0  cellpadding=0><tr><td><img height=1 src=\"spacer.gif\" width=5 border=0></td>";
	$distro_name = "Suse";
	switch ($distro) {
		//Default is Suse
		case 0:
		        $distro = 0 ;
			$xml_dir = "/var/www/html/testresults/suse-90-i586/$profile_name/xml/";
			$distro_name = "Suse";
#                        print "<p><br><div id=1tab>";

			print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=3\"><font size=2px>windowsXP</a></td>";
			print "<td><img src=\"overlap_off_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=2\"><font size=2px>Red Hat Linux9</a></td>";
                        print "<td><img src=\"overlap_off_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=1\"><font size=2px>Fedora Core 1</a></td>";
                        print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap height=20><font size=2px>Suse 9</td><td><img src=\"last_right_on.gif\" border=0 height=20 width=18></td></tr>";
                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";
			$filename = "/var/www/html/suse-90-i586-$profile_name.html";
		 	include($filename);

                break;

		case 1:
			$xml_dir = "/var/www/html/testresults/fedora-1-i386/$profile_name/xml/";
			$distro_name = "Fedora Core 1";
 #                       print "<p><br><div id=1tab>";
	                print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=3\"><font size=2px>windowsXP</a></td>";
	                print "<td><img src=\"overlap_off_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=2\"><font size=2px>Red Hat Linux9</a></td>";
                        print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap><font size=2px>Fedora Core 1</td><td><img src=\"overlap_on_off.gif\" border=0 border=0 height=20 width=18></td>";

                        print "<td class=tabputty noWrap height=20><a href=\"?&profile=$profile&distro=0\"><font size=2px>Suse 9</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";
			$filename = "fedora-1-i386-$profile_name.html";
		 	include($filename);
                break;
		case 2:
			$xml_dir = "/var/www/html/testresults/redhat-9-i386/$profile_name/xml/";
			$distro_name = "RedHat Linux 9";
  #                      print "<p><br><div id=1tab>";
	                print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=3\"><font size=2px>windowsXP</a></td>";
			print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap> <font size=2px>Red Hat Linux9</td>";
                        print "<td><img src=\"overlap_on_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=1\"><font size=2px>Fedora Core 1</td><td><img src=\"overlap_off_off.gif\" border=0 border=0 height=20 width=18></td>";

                        print "<td class=tabputty noWrap height=20><a href=\"?&profile=$profile&distro=0\"><font size=2px>Suse 9</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";
			$filename = "redhat-9-i386-$profile_name.html";
		 	include($filename);
                break;
	case 3:
			$xml_dir = "/var/www/html/testresults/windowsXP/$profile_name/xml/";
			$distro_name = "windowsXP";
  #                      print "<p><br><div id=1tab>";
			print "<td><img src=\"first_left_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap> <font size=2px>windowsXP</td>";
                        print "<td><img src=\"overlap_on_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=2\"><font size=2px>Red Hat Linux 9</td><td><img src=\"overlap_off_off.gif\" border=0 border=0 height=20 width=18></td>";
                        print "<td class=tabputty noWrap><a href=\"?&profile=$profile&distro=1\"><font size=2px>Fedora Core 1</td><td><img src=\"overlap_off_off.gif\" border=0 border=0 height=20 width=18></td>";

                        print "<td class=tabputty noWrap height=20><a href=\"?&profile=$profile&distro=0\"><font size=2px>Suse 9</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";
			$filename = "windowsXP-$profile_name.html";
		 	include($filename);
                break;
	}
	
	//Displaying Legend
         print "<p>";
         print "<br><br><b>Color Description</b><br><br>";
         print "<table border=1>";
	 print "<tr><td bgcolor=30b323>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage exactly 100 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage greater that 90 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=yellow>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage between 60 and 90 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=lightgreen>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp</td> <td>&nbsp;&nbsp Pass percentage less that 60 &nbsp;&nbsp</td></tr>";
         print "</table>";
         print "<br><font color= #0000FF > * Frequency of tests : Suse twice a week, Redhat and Fedora once every week </font> </p>";
	 print "<br><font size=2> NOTE: Color displayed for test suite is based on the most recent test result</font>";
         print "</p>";
?>
<a href="http://mono.ximian.com/tests/scripts.tar.gz">[Get the scripts used for running these tests]</a>

</body>
</html>
