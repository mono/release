<!--
  This script retrieves data from XML files and displays it on the web
 Author: Sachin Kumar <skumar1@novell.com>
         Satya Sudha K (ksathyasudha@novell.com)
         Ritvik Mayank (mritvik@novell.com)
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
	<?php
		#This function returns the sorted filenames that are of the required format 'testresults-<date>.xml'
		function get_sorted_filenames ($dir, $profile_name)
		{
			$dir_handle = opendir($dir);
			$files_count = 0;
			$files = array();
		        $prefix = "testresults-".$profile_name;
			$prefixLen = strlen($prefix);
			while (($filename = readdir($dir_handle)) != false) {
				if ($filename == "." || $filename == ".." || substr($filename,0,$prefixLen) != $prefix || substr($filename,-3,3) != "xml")
					continue;
				$files[$files_count] = $dir.$filename;
				$files_count++;
			}
			rsort($files);
			return $files;
		}
		#This function returns the set of testsuties from the given file based on the given type.
		#It also stores the testcases of the given status (this is needed to check for regression)
		function fetch_sorted_testsuites ($file,$type_key,$status_key)
		{
			$doc = xmldocfile ($file);
			$root = $doc->root ();
			$testsuites = $root->get_elements_by_tagname("testsuite");
			$sorted_testsuites = array ();
			$testsuite_count = 0;
			foreach ($testsuites as $testsuite) {
				if ($testsuite->get_attribute("type") != $type_key)
					continue;
				$sorted_testsuites[$testsuite_count]["name"] = $testsuite->get_attribute ("name");
				$sorted_testsuites[$testsuite_count]["pass"] = $testsuite->get_attribute ("pass");
				$sorted_testsuites[$testsuite_count]["fail"] = $testsuite->get_attribute ("fail");
				$sorted_testsuites[$testsuite_count]["notrun"] = $testsuite->get_attribute ("notrun");
				$sorted_testsuites[$testsuite_count]["exectime"] = $testsuite->get_attribute ("exectime");
				$sorted_testsuites[$testsuite_count]["date"] = $testsuite->get_attribute("date");
				$sorted_testsuites[$testsuite_count]["type"] = $testsuite->get_attribute("type");

				$testcases = array();
				$testcases = $testsuite->get_elements_by_tagname ("testcase");
				$testcase_count = 0;
                                foreach ($testcases as $testcase) {
                                	if ($testcase->get_attribute ("status") == $status_key) {
	                                	$sorted_testsuites[$testsuite_count]["testcases"][$testcase_count] = $testcase->get_attribute("name");
 	                                	$testcase_count++;
	                                }
                                }				
		
				$testsuite_count++;
			}
			if (count($sorted_testsuites) != 0) {
				foreach ($sorted_testsuites as $key => $row) { 
					//Order by testsuite name
                	                $name[$key] = $row["name"];
                        	}
	                        array_multisort($name, SORT_ASC, $sorted_testsuites);
			}
			return $sorted_testsuites;
		}

		#This function returns the formatted date from the filename
		function get_date_from_filename ($filename) 
		{
			$basename = basename($filename,".xml");
			$datetime = split ("-",$basename,-1);
			//Formatting date to yyyy-mm-dd
			$date = substr($datetime[2],0,4) ."-". substr($datetime[2],4,2) ."-". substr ($datetime[2],6);
			return $date;
		}

		#This function checks two arrays of testcase names for a match and returns the matching testcases
		function fetch_regressed_testcases ($testcases_1,$testcases_2)
		{
	
			$regressed_testcases = array();
			$regression_count = 0;
			//No regression if there are 0 failures for the recent date or 0 passes for the previous date
			if (count($testcases_1) == 0 || count($testcases_2) == 0)	 
				return $regresses_testcases;

			sort($testcases_1);
			sort($testcases_2);
			$testcases_1_count = 0;
			$testcases_2_count = 0;

			//Checking for a match			
			while ($testcases_1_count < count($testcases_1) && $testcases_2_count < count($testcases_2)) {
				if ($testcases_1[$testcases_1_count] == $testcases_2[$testcases_2_count]) {
					$regressed_testcases[$regression_count] = $testcases_1[$testcases_1_count];
					$regression_count++;
					$testcases_1_count++;
					$testcases_2_count++;
				}
				else if($testcases_1[$testcases_1_count] < $testcases_2[$testcases_2_count])
					$testcases_1_count++;
				else if($testcases_1[$testcases_1_count] > $testcases_2[$testcases_2_count])
					$testcases_2_count++;
					
			}
			return $regressed_testcases;
			
		}
	
		//This function displays the given testsuite details onto the web page
		function display_testsuites($distro_name,$new_table_caption,$testsuites_1,$testsuites_2,$files,$date_1,$date_2,$distro,$profile, &$total_array) 
		{
			if ( (count($testsuites_1) == 0) && (count ($testsuites_2) == 0))
				return;
			$new_table = "<table border=2>" .  "<tr><b>" . "<th rowspan=2><center> Sl.No</center></th><th rowspan=2><center> Test Suite (Pass %)</center></th>";
			$new_table = $new_table . "<th colspan=4><center>$date_1</center></th><th colspan=4><center>$date_2</center></th><th rowspan=2><center>Regression</center></th>" . "<tr><th><center>  Pass</center></th><th><center> Fail</center></th><th><center> Not Run</center></th><th><center> Execution Time</center></th><th><center> Pass </center></th><th><center>Fail</center></th><th><center> Not Run</center></th><th><center>Execution Time</center></th>";
			$testsuites_1_count = 0;
			$testsuites_2_count = 0;
			$s_no = 1;
			print "<br><b>" . $new_table_caption . "</b><br><br>".$new_table;

			$regressed_count = 0;
			$total_passes = array();
			$total_failures = array();
			$total_notrun = array();
			$total_exec = array();
			$total_regresses = 0;

			while($testsuites_1_count < count($testsuites_1) || $testsuites_2_count < count($testsuites_2)) {
				//Calculating pass percentage
				if ($testsuites_1[$testsuites_1_count]["name"]==null)
					$recentsuite = $testsuites_2[$testsuites_2_count];
				else
					$recentsuite = $testsuites_1[$testsuites_1_count];
				$total_tests = $recentsuite["pass"] + $recentsuite["fail"] + $recentsuite["notrun"];
				if ($total_tests != 0)
					$percent = ($recentsuite["pass"] * 100)/$total_tests;
				else
				        $percent = 100;
	        		$color = "ff3300";
				if ($percent > 90)
				        $color = "lightgreen";
                		else if($percent > 60)
				        $color = "yellow";
				if ($percent == 100)
					$color = "30b323";
				//Displaying result
				if ($testsuites_1[$testsuites_1_count]["name"] == $testsuites_2[$testsuites_2_count]["name"])
				{	
					//Testsuites that contain entries for both the recent and the previous run
					$regressed_count = 1;
					$total_passes[0] += $testsuites_1[$testsuites_1_count]["pass"];
					$total_passes[1] += $testsuites_2[$testsuites_2_count]["pass"];

					$total_failures[0] += $testsuites_1[$testsuites_1_count]["fail"];
                                        $total_failures[1] += $testsuites_2[$testsuites_2_count]["fail"];

					$total_notrun[0] += $testsuites_1[$testsuites_1_count]["notrun"];
                                        $total_notrun[1] += $testsuites_2[$testsuites_2_count]["notrun"];

					$total_exec[0] += $testsuites_1[$testsuites_1_count]["exectime"];
                                        $total_exec[1] += $testsuites_2[$testsuites_2_count]["exectime"];

					print "<tr><td>$s_no</td>";
	
	                                $testsuite_name = $testsuites_1[$testsuites_1_count]["name"]." (".ceil ($percent) ." %)";
					$link = "displayDetails.php?image=1&testsuite=".$testsuites_1[$testsuites_1_count]["name"]."&profile=$profile&distro=$distro";
					print "<td bgcolor=$color><a href=$link>". $testsuite_name . "</a></td>";
					if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
						print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
					else
						print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";

					 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
	        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";

					 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
	        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
					print "<td>" . $testsuites_1[$testsuites_1_count]["exectime"]. "</td>";
					$testsuites_1_count++;

					if ($testsuites_2[$testsuites_2_count]["pass"] != 0)
						print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
					else
						print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
			
					 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";

					 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";
					print "<td>" . $testsuites_2[$testsuites_2_count]["exectime"]. "</td>";
					
					$testsuite_name = $testsuites_2[$testsuites_2_count]["name"];
					$testsuites_2_count++;		
				}

				else if($testsuites_1[$testsuites_1_count]["name"] != null && (($testsuites_1[$testsuites_1_count]["name"] < $testsuites_2[$testsuites_2_count]["name"]) || ($testsuites_2[$testsuites_2_count]["name"]==null))) {	
					#testsuites that contain an entry for recent run and no entry for previous run
					$regressed_count = 0;

					$total_passes[0] += $testsuites_1[$testsuites_1_count]["pass"];
                                        $total_failures[0] += $testsuites_1[$testsuites_1_count]["fail"];
                                        $total_notrun[0] += $testsuites_1[$testsuites_1_count]["notrun"];
					$total_exec[0] += $testsuites_1[$testsuites_1_count]["exectime"];

					print "<tr><td>$s_no</td>";
                	        	print "<td bgcolor=$color>" . $testsuites_1[$testsuites_1_count]["name"]. " (".ceil ($percent) ." %)". "</td>";

					if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
                                                                                                                             
	        	                 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
                                                                                                                             
	        	                 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
	        	                print "<td>" . $testsuites_1[$testsuites_1_count]["exectime"]. "</td>";
					$testsuite_name = $testsuites_1[$testsuites_1_count]["name"];
                		        $testsuites_1_count++;

                	        	print "<td>&nbsp;</td>";
	        	                print "<td>&nbsp;</td>";
        		                print "<td>&nbsp</td>";
                		        print "<td>&nbsp;</td>";
				}

				else if($testsuites_2[$testsuites_2_count]["name"] != null && (($testsuites_1[$testsuites_1_count]["name"] > $testsuites_2[$testsuites_2_count]["name"]) || ($testsuites_1[$testsuites_1_count]["name"]==null))) {
					#testsuites that contain an entry for previous run and no entry for the recent run
					$regressed_count = 0;

                                        $total_passes[1] += $testsuites_2[$testsuites_2_count]["pass"];
                                        $total_failures[1] += $testsuites_2[$testsuites_2_count]["fail"];
                                        $total_notrun[1] += $testsuites_2[$testsuites_2_count]["notrun"];
                                        $total_exec[1] += $testsuites_2[$testsuites_2_count]["exectime"];

                		        print "<tr><td>$s_no</td>";
					print "<td bgcolor=$color>" . $testsuites_2[$testsuites_2_count]["name"]. "</td>";
					print "<td>&nbsp;</td>";
        		                print "<td>&nbsp;</td>";
                		        print "<td>&nbsp</td>";
                	        	print "<td>&nbsp;</td>";

					if ($testsuites_2[$testsuites_2_count]["pass"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
                	                                                                                                             
	        	                 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                                                                                                                             
	        	                 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";

	        	                print "<td>" . $testsuites_2[$testsuites_2_count]["exectime"]. "</td>";
					$testsuite_name = $testsuites_2[$testsuites_2_count]["name"];
                		        $testsuites_2_count++;
                		}
				$s_no++;

				//Displaying number of regressed testcases
				$regressed_testcases = array ();
				if ($regressed_count != 0) {
					//Checking for number of matches between the testcases that failed in the recent run and passed in the previous run
					$regressed_testcases = fetch_regressed_testcases($testsuites_1[$testsuites_1_count-1]["testcases"],$testsuites_2[$testsuites_2_count-1]["testcases"]);
					$regressed_count = count ($regressed_testcases);
				}
				
				if ($regressed_count != 0) 
					print "<td><a href=displayDetails.php?&testsuite=" . $testsuite_name. "&file=" .substr($files[0],-12,8). "&file1=".substr($files[1],-12,8)."&regression=1&status=4&profile=$profile&distro=$distro>".$regressed_count."</td></tr>";
				else
					print "<td>".$regressed_count."</td></tr>";
				print "</tr>";
				$total_regresses += $regressed_count;
			}

			$total_array[0]["pass"] += $total_passes[0];
			$total_array[0]["fail"] += $total_failures[0];
			$total_array[0]["notrun"] += $total_notrun[0];
			$total_array[1]["pass"] += $total_passes[1];
			$total_array[1]["fail"] += $total_failures[1];
			$total_array[1]["notrun"] += $total_notrun[1];
			print "<tr><td>&nbsp</td><td>Total</td><td>".$total_passes[0]."</td><td>".$total_failures[0]."</td><td>".$total_notrun[0]."</td><td>".$total_exec[0]."</td>";
			print "<td>".$total_passes[1]."</td><td>".$total_failures[1]."</td><td>".$total_notrun[1]."</td><td>".$total_exec[1]."</td><td>".$total_regresses."</td>";
			print "</table>";
		}

	?>
</head>
<body>
<h1>Mono Test Suite Results</h1>
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
			$xml_dir = "/var/www/mono-website/go-mono/tests/testresults/suse-90-i586/$profile_name/xml/";
			$distro_name = "Suse";
#                        print "<p><br><div id=1tab>";

			print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=2\"><font size=2px>Red Hat Linux9</a></td>";
                        print "<td><img src=\"overlap_off_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=1\"><font size=2px>Fedora Core 1</a></td>";
                        print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap height=20><font size=2px>Suse 9</td><td><img src=\"last_right_on.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";

                break;

		case 1:
			$xml_dir = "/var/www/mono-website/go-mono/tests/testresults/fedora-1-i386/$profile_name/xml/";
			$distro_name = "Fedora Core 1";
 #                       print "<p><br><div id=1tab>";

	                print "<td><img src=\"first_left_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=2\"><font size=2px>Red Hat Linux9</a></td>";
                        print "<td><img src=\"overlap_off_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap><font size=2px>Fedora Core 1</td><td><img src=\"overlap_on_off.gif\" border=0 border=0 height=20 width=18></td>";

                        print "<td class=tabputty noWrap height=20><a href=\"?&profile=$profile&distro=0\"><font size=2px>Suse 9</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";

                break;
		case 2:
			$xml_dir = "/var/www/mono-website/go-mono/tests/testresults/redhat-9-i386/$profile_name/xml/";
			$distro_name = "RedHat Linux 9";
  #                      print "<p><br><div id=1tab>";

			print "<td><img src=\"first_left_on.gif\" border=0 height=20 width=18></td><td class=tabblue noWrap> <font size=2px>Red Hat Linux9</td>";

                        print "<td><img src=\"overlap_on_off.gif\" border=0 height=20 width=18></td><td class=tabputty noWrap><a href=\"?&profile=$profile&distro=1\"><font size=2px>Fedora Core 1</td><td><img src=\"overlap_off_off.gif\" border=0 border=0 height=20 width=18></td>";

                        print "<td class=tabputty noWrap height=20><a href=\"?&profile=$profile&distro=0\"><font size=2px>Suse 9</td><td><img src=\"last_right_off.gif\" border=0 height=20 width=18></td></tr>";

                        print "<tr><td class=tabblue colSpan=40 height=5><IMG height=5 src=\"spacer.gif\" width=1 border=0></td>";
                break;
	}
	print "</tr></table><table border=1><tr><td colspan=3>";
        print "<h3>Mono Test Suite Results for $distro_name under Profile $profile_name</h3>";

	$files = get_sorted_filenames ($xml_dir, $profile_name);
	$date_1 = get_date_from_filename ($files[0]); 
	$date_2 = get_date_from_filename ($files[1]);
	
	$new_table_type[0] = "NUnit Test Suite";
        $new_table_type[1] = "Compiler Test Suite";
        $new_table_type[2] = "Runtime Test Suite";
        $new_table_type[3] = "Other Test Suite";
	
	$total_hash = array();
	$total_hash[0]["pass"] = 0;
	$total_hash[0]["fail"] = 0;
	$total_hash[0]["notrun"] = 0;
	$total_hash[1]["pass"] = 0;
	$total_hash[1]["fail"] = 0;
	$total_hash[1]["notrun"] = 0;
	for($i=0; $i<4;$i++) { //foreach type of testsuites, fetching the testsuites and displaying the details
		$testsuites_1 = array();
		$testsuites_2 = array();
		$testsuites_1 = fetch_sorted_testsuites ($files[0],$i,1);
	        $testsuites_2 = fetch_sorted_testsuites ($files[1],$i,0);
		display_testsuites($distro_name,$new_table_type[$i],$testsuites_1,$testsuites_2,$files,$date_1,$date_2,$distro,$profile, &$total_hash);
	}

	print "<br><br>";
	print "<b>Total Pass/Fail Statistics</b><br><br>";
	$link = "displayDetails.php?image=1&testsuite=Total&profile=$profile&distro=$distro";
	print "<table border=2>" .  "<tr>" . "<th rowspan=2><center> Total Statistics</center></th>";
	print "<th width = 300 colspan=3><center>$date_1</center></th><th width = 300 colspan=3><center>$date_2</center></th>" . "<tr><th><center>  Pass</center></th><th><center> Fail</center></th><th><center> Not Run</center></th><th><center> Pass </center></th><th><center>Fail</center></th><th><center> Not Run</center></th>";
	print "</tr>";
	print "<tr><td><center><a href=$link>Total<a></center></td>\n";
	print "<td><center>".$total_hash[0]["pass"]."</center></td>";
	print "<td><center>".$total_hash[0]["fail"]."</center></td>";
	print "<td><center>".$total_hash[0]["notrun"]."</center></td>";
	print "<td><center>".$total_hash[1]["pass"]."</center></td>";
	print "<td><center>".$total_hash[1]["fail"]."</center></td>";
	print "<td><center>".$total_hash[1]["notrun"]."</center></td>";
	print "</td></tr></table>";
	print "</td></tr></table></div>";

	//Displaying Legend
         print "<p>";
         print "<br><br><b>Color Description</b><br><br>";
         print "<table border=1>";
	 print "<tr><td bgcolor=30b323>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage exactly 100 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=lightgreen>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage greater that 90 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=yellow>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>&nbsp;&nbsp Pass percentage between 60 and 90 &nbsp;&nbsp</td></tr>";
         print "<tr><td bgcolor=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp</td> <td>&nbsp;&nbsp Pass percentage less that 60 &nbsp;&nbsp</td></tr>";
         print "</table>";
         print "<br><font size=2> NOTE: Color displayed for test suite is based on the most recent test result</font>";
         print "</p>";
?>
</body>
</html>


