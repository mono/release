<!--
  This script retrieves data from XML files and displays it on the web
-->
<html>
<head>
	<title>Mono Test Suite Results</title>
	<?php
		#This function returns the sorted filenames that are of the required format 'testresults-<date>.xml'
		function get_sorted_filenames ($dir) 
		{
			$dir_handle = opendir($dir);
			$files_count = 0;
			$files = array();
			
			while (($filename = readdir($dir_handle)) != false) {
				if ($filename == "." || $filename == ".." || substr($filename,0,12) != "testresults-" || substr($filename,-3,3) != "xml")
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
			$date = substr($datetime[1],0,4) ."-". substr($datetime[1],4,2) ."-". substr ($datetime[1],6);
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
		function display_testsuites($new_table_caption,$testsuites_1,$testsuites_2,$files,$date_1,$date_2) 
		{
			$new_table = "<table border=2>" .  "<tr><b>" . "<th rowspan=2> S.No </th><th rowspan=2> Test Suite </th>";
			$new_table = $new_table . "<th colspan=4>$date_1 </th><th colspan=4>$date_2</th><th rowspan=2>Regression</th>" . "<tr><th>Pass</th><th>Fail</th><th>Not Run</th><th>Execution Time</th><th>Pass</th><th>Fail</th><th>Not Run</th><th>Execution Time</th>";
			print "<br>\n";
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
	
					print "<td bgcolor=$color>" . $testsuites_1[$testsuites_1_count]["name"]. "</td>";
					if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
						print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
					else
						print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";

					 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
	        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";

					 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
                	        	        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
	        	                else
        		                        print "<td>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
					print "<td>" . $testsuites_1[$testsuites_1_count]["exectime"]. "</td>";
					$testsuites_1_count++;

					if ($testsuites_2[$testsuites_2_count]["pass"] != 0)
						print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
					else
						print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
			
					 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";

					 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";
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
                	        	print "<td bgcolor=$color>" . $testsuites_1[$testsuites_1_count]["name"]. "</td>";

					if ($testsuites_1[$testsuites_1_count]["pass"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=0>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["pass"].  "</td>";
                                                                                                                             
	        	                 if ($testsuites_1[$testsuites_1_count]["fail"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=1>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
                		        else
                	        	        print "<td>" . $testsuites_1[$testsuites_1_count]["fail"].  "</td>";
                                                                                                                             
	        	                 if ($testsuites_1[$testsuites_1_count]["notrun"] != 0)
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_1[$testsuites_1_count]["name"]. "&file=" .substr($files[0],-12,8). "&status=2>" . $testsuites_1[$testsuites_1_count]["notrun"].  "</td>";
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
        		                        print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=0>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["pass"]. "</td>";
                	                                                                                                             
	        	                 if ($testsuites_2[$testsuites_2_count]["fail"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=1>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                		        else
                	        	        print "<td>" . $testsuites_2[$testsuites_2_count]["fail"]. "</td>";
                                                                                                                             
	        	                 if ($testsuites_2[$testsuites_2_count]["notrun"] != 0)
        		                         print "<td><a href=displayDetails.php?&testsuite=" . $testsuites_2[$testsuites_2_count]["name"]. "&file=" .substr($files[1],-12,8). "&status=2>" . $testsuites_2[$testsuites_2_count]["notrun"]. "</td>";
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
					print "<td><a href=displayDetails.php?&testsuite=" . $testsuite_name. "&file=" .substr($files[0],-12,8). "&file1=".substr($files[1],-12,8)."&regression=1&status=4>".$regressed_count."</td></tr>";
				else
					print "<td>".$regressed_count."</td></tr>";
				print "</tr>";
				$total_regresses += $regressed_count;
			}
			print "<tr><td>".$s_no."</td><td>Total</td><td>".$total_passes[0]."</td><td>".$total_failures[0]."</td><td>".$total_notrun[0]."</td><td>".$total_exec[0]."</td>";
			print "<td>".$total_passes[1]."</td><td>".$total_failures[1]."</td><td>".$total_notrun[1]."</td><td>".$total_exec[1]."</td><td>".$total_regresses."</td>";
			print "</table>";
		}

	?>
</head>
<body>
<h2>Mono Test Suite Results</h2>
<?php
	$files = get_sorted_filenames ("testresults/xml/");
	$date_1 = get_date_from_filename ($files[0]); 
	$date_2 = get_date_from_filename ($files[1]);
	
	$new_table_type[0] = "NUnit Test Suite";
        $new_table_type[1] = "Compiler Test Suite";
        $new_table_type[2] = "Runtime Test Suite";
	
	for($i=0; $i<3;$i++) { //foreach type of testsuites, fetching the testsuites and displaying the details
		$testsuites_1 = array();
		$testsuites_2 = array();
		$testsuites_1 = fetch_sorted_testsuites ($files[0],$i,1);
	        $testsuites_2 = fetch_sorted_testsuites ($files[1],$i,0);
		display_testsuites($new_table_type[$i],$testsuites_1,$testsuites_2,$files,$date_1,$date_2);
	}

	//Displaying Legend
         print "<p>";
         print "<br><br><b>Color Description</b><br><br>";
         print "<table border=1>";
	 print "<tr><td bgcolor=30b323>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>Pass percentage exactly 100</td></tr>";
         print "<tr><td bgcolor=lightgreen>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>Pass percentage greater that 90</td></tr>";
         print "<tr><td bgcolor=yellow>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp </td> <td>Pass percentage between 60 and 90</td></tr>";
         print "<tr><td bgcolor=red>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp</td> <td>Pass percentage less that 60</td></tr>";
         print "</table>";
         print "<br><font size=2> NOTE: Color displayed for test suite is based on the most recent test result</font>";
         print "</p>";

?>
</body>
</html>

