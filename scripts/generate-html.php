#!/usr/bin/php
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
	$filename = "$distro_name-$profile.html";
	
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

				print "<tr><td>$s_no</td>\n";

                                $testsuite_name = $testsuites_1[$testsuites_1_count]["name"]." (".ceil ($percent) ." %)";
				$link = "displayDetails.php?image=1&testsuite=".$testsuites_1[$testsuites_1_count]["name"]."&profile=$profile&distro=$distro";
				print "<td bgcolor=$color><a href=$link>". $testsuite_name . "</a></td>\n";
				if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
					print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>\n";
				else
					print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>\n";

				 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>\n";
        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>\n";

				 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>\n";
        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>\n";
				print "<td>" . $testsuites_1[$testsuites_1_count]["exectime"]. "</td>\n";
				$testsuites_1_count++;

				if ($testsuites_2[$testsuites_2_count]["pass"] != 0)
					print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>\n";
				else
					print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>\n";
		
				 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>\n";

				 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>\n";
				print "<td>" . $testsuites_2[$testsuites_2_count]["exectime"]. "</td>\n";
				
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

				print "<tr><td>$s_no</td>\n";
                	        	print "<td bgcolor=$color>" . $testsuites_1[$testsuites_1_count]["name"]. " (".ceil ($percent) ." %)". "</td>\n";

				if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>\n";
                                                                                                                             
        	                 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>\n";
                                                                                                                             
        	                 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>\n";
        	                print "<td>" . $testsuites_1[$testsuites_1_count]["exectime"]. "</td>\n";
				$testsuite_name = $testsuites_1[$testsuites_1_count]["name"];
                		        $testsuites_1_count++;

                	        	print "<td>&nbsp;</td>\n";
        	                print "<td>&nbsp;</td>\n";
        		                print "<td>&nbsp</td>\n";
                		        print "<td>&nbsp;</td>\n";
			}

			else if($testsuites_2[$testsuites_2_count]["name"] != null && (($testsuites_1[$testsuites_1_count]["name"] > $testsuites_2[$testsuites_2_count]["name"]) || ($testsuites_1[$testsuites_1_count]["name"]==null))) {
				#testsuites that contain an entry for previous run and no entry for the recent run
				$regressed_count = 0;

                                        $total_passes[1] += $testsuites_2[$testsuites_2_count]["pass"];
                                        $total_failures[1] += $testsuites_2[$testsuites_2_count]["fail"];
                                        $total_notrun[1] += $testsuites_2[$testsuites_2_count]["notrun"];
                                        $total_exec[1] += $testsuites_2[$testsuites_2_count]["exectime"];

                		        print "<tr><td>$s_no</td>\n";
				print "<td bgcolor=$color>" . $testsuites_2[$testsuites_2_count]["name"]. "</td>\n";
				print "<td>&nbsp;</td>\n";
        		                print "<td>&nbsp;</td>\n";
                		        print "<td>&nbsp</td>\n";
                	        	print "<td>&nbsp;</td>\n";

				if ($testsuites_2[$testsuites_2_count]["pass"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>\n";
                	                                                                                                             
        	                 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                                                                                                                             
        	                 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2&profile=$profile&distro=$distro>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>\n";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>\n";

        	                print "<td>" . $testsuites_2[$testsuites_2_count]["exectime"]. "</td>\n";
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
				print "<td><a href=displayDetails.php?&testsuite=" . $testsuite_name. "&file=" .substr($files[0],-12,8). "&file1=".substr($files[1],-12,8)."&regression=1&status=4&profile=$profile&distro=$distro>".$regressed_count."</td></tr>\n";
			else
				print "<td>".$regressed_count."</td></tr>\n";
			print "</tr>\n";
			$total_regresses += $regressed_count;
		}

		$total_array[0]["pass"] += $total_passes[0];
		$total_array[0]["fail"] += $total_failures[0];
		$total_array[0]["notrun"] += $total_notrun[0];
		$total_array[1]["pass"] += $total_passes[1];
		$total_array[1]["fail"] += $total_failures[1];
		$total_array[1]["notrun"] += $total_notrun[1];
		print "<tr><td>&nbsp</td><td>Total</td><td>".$total_passes[0]."</td><td>".$total_failures[0]."</td><td>".$total_notrun[0]."</td><td>".$total_exec[0]."</td>\n";
		print "<td>".$total_passes[1]."</td><td>".$total_failures[1]."</td><td>".$total_notrun[1]."</td><td>".$total_exec[1]."</td><td>".$total_regresses."</td>";
		print "</table>\n";
	}

	ini_set("memory_limit", "20M");
	$usage = "php generate-html.php --profile <profile> --distro <distro> --help\n";
	if (($argc < 3) || in_array("--help", $argv)) {
		print "$usage";
		exit;
	}

	$distro_name = "suse-90-i586";
	$profile_name = "default";

	for ( $i = 1; $i<=2 ; $i++) {
		$name_value = array();
		$name_value = split('=', $argv[$i]);
		if ($name_value[0] == "--profile") {
			$profile_name = $name_value[1];
		} else if ($name_value[0] == "--distro") {
			$distro_name = $name_value[1];
		} else {
			print "$usage";
			exit;
		}
	}

	if (false == in_array($distro_name, array('suse-90-i586', 'redhat-9-i386', 'fedora-1-i386'))) {
		print "Invalid distro!!\n";
		exit;
	}

	if (false == in_array($profile_name, array('default', 'net_2_0'))) {
		print "Invalid profile!!\n";
		exit;
	}

	$distros = array(0 => 'suse-90-i586', 1 => 'fedora-1-i386', 2 => 'redhat-9-i386');
	$profiles = array(0 => 'default', 1 => 'net_2_0');

	$distro = array_search($distro_name, $distros);
	$profile = array_search($profile_name, $profiles);

	$xml_dir ="/var/www/html/testresults/$distro_name/$profile_name/xml/";

	print "</tr></table><table border=1><tr><td colspan=3>";
        print "<h3>Mono Test Suite Results for $distro_name under Profile $profile_name</h3>\n";

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

	print "<br><br>\n";
	print "<b>Total Pass/Fail Statistics</b><br><br>\n";
	$link = "displayDetails.php?image=1&testsuite=Total&profile=$profile&distro=$distro";
	print "<table border=2>" .  "<tr>" . "<th rowspan=2><center> Total Statistics</center></th>\n";
	print "<th width = 300 colspan=3><center>$date_1</center></th><th width = 300 colspan=3><center>$date_2</center></th>" . "<tr><th><center>  Pass</center></th><th><center> Fail</center></th><th><center> Not Run</center></th><th><center> Pass </center></th><th><center>Fail</center></th><th><center> Not Run</center></th>\n";
	print "</tr>\n";
	print "<tr><td><center><a href=$link>Total<a></center></td>\n\n";
	print "<td><center>".$total_hash[0]["pass"]."</center></td>\n";
	print "<td><center>".$total_hash[0]["fail"]."</center></td>";
	print "<td><center>".$total_hash[0]["notrun"]."</center></td>";
	print "<td><center>".$total_hash[1]["pass"]."</center></td>";
	print "<td><center>".$total_hash[1]["fail"]."</center></td>";
	print "<td><center>".$total_hash[1]["notrun"]."</center></td>";
	print "</td></tr></table>";
	print "</td></tr></table></div>";

?>
