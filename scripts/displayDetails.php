<!--
  This script displays testcase results for a particular testsuite
-->
<html>
<head>
	<title>Mono TestCase Results</title>
	<?php
		function fetch_testcases($testsuite_key,$status_key,$file) 
		{
			$doc = xmldocfile ($file);
                        $root = $doc->root ();
			$testsuites = $root->get_elements_by_tagname("testsuite");
                        $sorted_testsuites = array ();
                        $testsuite_count = 0;
			$sorted_testcases = array ();
			$testcases_count = 0;
                        foreach ($testsuites as $testsuite) {
				if ($testsuite->get_attribute("name") == $testsuite_key) {
					$logfile = $testsuite->get_elements_by_tagname("testsuite-log");
	                                if (count($logfile) > 0) {
						//If testsuite contains logfile details, return the log message
						$sorted_testcases[0] = "0";
						$log_content = preg_replace('"<"','&lt;',$logfile[0]->get_content());
						$sorted_testcases[1] = $log_content;
						return $sorted_testcases;
					}
					$testcases = $testsuite->get_elements_by_tagname("testcase");
					foreach ($testcases as $testcase) {
						if($testcase->get_attribute("status") == $status_key) {
							$sorted_testcases [$testcases_count]["name"] = $testcase->get_attribute("name");
							$sorted_testcases [$testcases_count]["exectime"] = $testcase->get_attribute("exectime");
							$sorted_testcases [$testcases_count]["regression"] = $testcase->get_attribute("regression");
							$message = $testcase->get_elements_by_tagname("message");
							print $temp;
							if (count ($message) > 0) {
								$message_content = preg_replace('"<"','&lt;',$message[0]->get_content());
								$sorted_testcases [$testcases_count]["message"] = $message_content;
							}
							$stacktrace = $testcase->get_elements_by_tagname("stacktrace");
                                                        if (count ($stacktrace) > 0)
                                                                $sorted_testcases [$testcases_count]["stacktrace"] = $stacktrace[0]->get_content ();
							$testcases_count++;
						}
					}			
					break;
				}
				
			}
			sort ($sorted_testcases);
			return $sorted_testcases;
		}
		function fetch_regressed_testcases ($testsuite_name,$file_1,$file_2)
                {
                        $doc_1 = xmldocfile ($file_1);
                        $doc_2 = xmldocfile ($file_2);
                        $root_1 = $doc_1->root ();
                        $root_2 = $doc_2->root ();
                                                                                                                             
                        $testsuites_1 = $root_1->get_elements_by_tagname("testsuite");
                        $testsuites_2 = $root_2->get_elements_by_tagname("testsuite");
                        $testcases_1 = array ();
                        $testcases_2 = array ();
                                                                                                                             
                        $regressed_testcases = array ();
                        $testflag = 0;
                        $testcases_1_count = 0;
                        foreach ($testsuites_1 as $testsuite_1) {
                                if ($testsuite_1->get_attribute("name") == $testsuite_name) {
                                        $testcases = array();
                                        $testcases = $testsuite_1->get_elements_by_tagname ("testcase");
                                        foreach ($testcases as $testcase) {
                                                if ($testcase->get_attribute ("status") == "1") {
                                                        $testcases_1[$testcases_1_count] = $testcase->get_attribute("name");
                                                        $testcases_1_count++;
                                                }
                                        }
                                        $testflag = 1;
                                        break;
                                }
                        }
                        if ($testflag == 0)
                                return $regressed_testcases; //return empty array
			$testflag = 0;
                        $testcases_2_count = 0;
                        foreach ($testsuites_2 as $testsuite_2) {
                                if ($testsuite_2->get_attribute("name") == $testsuite_name) {
                                        $testcases = array ();
                                        $testcases = $testsuite_2->get_elements_by_tagname("testcase");
                                        foreach ($testcases as $testcase) {
                                                if ($testcase->get_attribute ("status") == "0") {
                                                        $testcases_2[$testcases_2_count] = $testcase->get_attribute("name");
                                                        $testcases_2_count++;
                                                }
                                        }
                                        $testflag = 1;
                                        break;
                                }
                        }
                        if ($testflag == 0)
                                return $regressed_testcases; //return empty array

			if (count($testcases_1) == 0 || count($testcases_2) == 0)
                                return $regresses_testcases; //return empty array
                                                                                                                             
                        sort($testcases_1);
                        sort($testcases_2);
                        $testcases_1_count = 0;
                        $testcases_2_count = 0;
			$regression_count = 0;
                                                                                                                             
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
			sort ($regressed_testcases);
                        return $regressed_testcases;
                                                                                                                             
                }
	?>
</head>
                                                                                                                          
<body>
	<?php 

		$testsuite_key = $_GET['testsuite'];
		$status_key = $_GET['status'];
		$file = $_GET['file'];
		$file_1 = $_GET['file1'];

		$date = `date +"%Y%m%d"`;
                $chart_url = "TestResults/Charts/$testsuite_key/$date.png";

		if ($_GET['regression'] == 1) {
			print "<h3>REGRESSED TESTCASES FOR " .  $_GET['testsuite'] . "&nbsp;<a href=\"$chart_url\"><font size=\"2\" color=\"blue\">&lt;View Progress Chart></font></a></h3>";
			$testcases = fetch_regressed_testcases($testsuite_key,$file,$file_1);
			print "<table border=1><tr><th>S.No.</th><th>Test Case Name</th><th></tr>";	
			$count = 1;
			foreach ($testcases as $testcase) {
				print "<tr><td>$count</td><td>" . $testcase . "</td></tr>";
				$count++;
			}
			return;
		}
		$testcases = fetch_testcases($testsuite_key,$status_key,$file);
		if ($testcases[0] == "0") {
			//Displaying log message
			print "<h3>TESTCASE RESULTS FOR " .  $_GET['testsuite'] . "&nbsp;<a href=\"$chart_url\"><font size=\"2\" color=\"blue\">&lt;View Progress Chart></font></a></h3>";
			print "<pre>".$testcases[1]."</pre>";
			return;
		}
		if ($status_key == 0) //Pass Tests
		{
			print "<h3>PASSED TESTCASES FOR " .  $_GET['testsuite'] . "&nbsp;<a href=\"$chart_url\"><font size=\"2\" color=\"blue\">&lt;View Progress Chart></font></a></h3>";
			print "<table border=1><tr><th>S.No.</th><th>Test Case Name</th><th>Execution Time</th></tr>";
			$count = 1;
			foreach ($testcases as $testcase) {
				print "<tr><td>$count</td><td>" . $testcase["name"] . "</td><td>" . $testcase["exectime"] . "</td></tr>";	
				$count++;
			}
			print "<table>";
		}
		
		else if ($status_key == 2) //Not Run Tests
		{
			print "<h3>NOT RUN TESTCASES FOR " .  $_GET['testsuite'] . "&nbsp;<a href=\"$chart_url\"><font size=\"2\" color=\"blue\">&lt;View Progress Chart></font></a></h3>";
			print "<table border=1><tr><th>S.No.</th><th>Test Case Name</th><th>Message</th></tr>";
			$count = 1;
                        foreach ($testcases as $testcase) {
                                print "<tr><td>$count</td><td>" . $testcase["name"] . "</td><td>" . $testcase["message"] . "</td></tr>";
                                $count++;
                        }
			print "</table>";
		}
		
		else if ($status_key == 1) //Failed Test Case
		{
			print "<h3>FAILED TESTCASES FOR " .  $_GET['testsuite'] . "&nbsp;<a href=\"$chart_url\"><font size=\"2\" color=\"blue\">&lt;View Progress Chart></font></a></h3>";
			print "<table border =1><tr><th><b>S.No.</th></b><th><b>Test Case Name</b></th><th><b>Message</b></th></tr>";
			$count = 1;
			foreach ($testcases as $testcase) {
				print "<tr><td>$count </td><td bgcolor=$color><a href=#".$count.">" . $testcase["name"]. "</a></td><td>".$testcase["message"]."</td><tr>";
				$count++;
			}
			print "</table>";

			$count = 1;
			foreach ($testcases as $testcase) {
				print "<p>" . $count . ".";
				print "<b id=$count><font size=4>&nbsp;&nbsp;&nbsp;&nbsp;Test Case Name: "  . $testcase["name"] . "</font></b><br><br>";
				if ($testcase ["message"] != null)
                                          print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Message:</b>&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<pre>" . $testcase["message"] . "</pre><br>";
				if ($testcase ["stacktrace"] != null)
					print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Stack Trace:</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<pre>" . $testcase["stacktrace"] . "</pre></p>";
				$count++;
			}
		}
		if ($count == 1)
                        print "<font color=red><b> No Testcase Details Available! </b></font>";	
                                                                                                                             
	?>
</body>
</html>
