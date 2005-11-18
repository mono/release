<!--
  This script displays testcase results for a particular testsuite
-->
<html>
<head>
	<title>Mono TestCase Results</title>
	<link rel="stylesheet" href="http://go-mono.com/monologue/monologue.css" type="text/css" />
	<?php
		#This function fetches testcases from the given XML file based on the given testsuite and status
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
						#If testsuite contains logfile details, return an array containing 0 and the log message
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
		# This function fetches the failed testcases of the recent run and the passed test cases of the previous run
		# Those testcases that passed in the previous run and failed in the recent run are returned
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
					#Store those testcases that failed in the recent run
                                        foreach ($testcases as $testcase) {
                                                if ($testcase->get_attribute ("status") == "1") {
                                                        $testcases_1[$testcases_1_count]["name"] = $testcase->get_attribute("name");
							$message = $testcase->get_elements_by_tagname("message");
                                                        if (count ($message) > 0) {
                                                                $message_content = preg_replace('"<"','&lt;',$message[0]->get_content());
                                                                $testcases_1[$testcases_1_count]["message"] = $message_content;
                                                        }
                                                        $stacktrace = $testcase->get_elements_by_tagname("stacktrace");
                                                        if (count ($stacktrace) > 0)
                                                                $testcases_1[$testcases_1_count]["stacktrace"] = $stacktrace[0]->get_content ();
                                                        $testcases_1_count++;
                                                }
                                        }
                                        $testflag = 1;
                                        break;
                                }
                        }
                        if ($testflag == 0)
                                return $regressed_testcases; #return empty array if no entry is present for the recent run
			$testflag = 0;
                        $testcases_2_count = 0;
                        foreach ($testsuites_2 as $testsuite_2) {
                                if ($testsuite_2->get_attribute("name") == $testsuite_name) {
                                        $testcases = array ();
                                        $testcases = $testsuite_2->get_elements_by_tagname("testcase");
					#Store those testcases that passed in the previous run
                                        foreach ($testcases as $testcase) {
                                                if ($testcase->get_attribute ("status") == "0") {
                                                        $testcases_2[$testcases_2_count]["name"] = $testcase->get_attribute("name");
                                                        $testcases_2_count++;
                                                }
                                        }
                                        $testflag = 1;
                                        break;
                                }
                        }
                        if ($testflag == 0)
                                return $regressed_testcases; #return empty array if no entry is present for the previous run

			if (count($testcases_1) == 0 || count($testcases_2) == 0)
                                return $regresses_testcases; #return empty array

                        sort($testcases_1);
                        sort($testcases_2);

                        $testcases_1_count = 0;
                        $testcases_2_count = 0;
			$regression_count = 0;

                        
			#Checking for regression
                        while ($testcases_1_count < count($testcases_1) && $testcases_2_count < count($testcases_2)) {
                                if ($testcases_1[$testcases_1_count]["name"] == $testcases_2[$testcases_2_count]["name"]) {
                                        $regressed_testcases[$regression_count]["name"] = $testcases_1[$testcases_1_count]["name"];
					$regressed_testcases[$regression_count]["message"] = $testcases_1[$testcases_1_count]["message"];
					$regressed_testcases[$regression_count]["stacktrace"] = $testcases_1[$testcases_1_count]["stacktrace"];
                                        $regression_count++;
                                        $testcases_1_count++;
                                        $testcases_2_count++;
                                }
                                else if($testcases_1[$testcases_1_count]["name"] < $testcases_2[$testcases_2_count]["name"])
                                        $testcases_1_count++;
                                else if($testcases_1[$testcases_1_count]["name"] > $testcases_2[$testcases_2_count]["name"])
                                        $testcases_2_count++;
                                                                                                                             
                        }
			sort ($regressed_testcases);
                        return $regressed_testcases;
                                                                                                                             
                }
		#This function makes sure the input file names are correct 
		function sanitize ($filename) {
			if (!is_numeric($filename)) {
				print "<b><font color = red>Wrong Filename</b></font>";
				exit;
			}
			
		}
	?>
</head>
                                                                                                                          
<body>
	<?php 
		$testsuite_key = $_GET['testsuite'];
		$distro = $_GET['distro'];
         	$profile = $_GET['profile'];
		$distroPath = "suse-90-i586";
		$profilePath = "default";
		if ($distro == 0 && $profile == 0){ # suse and default
			$root = "/var/www/html/testresults/suse-90-i586/default/";
			}
		else if ($distro == 1 && $profile == 0){ # fedora-1-i386 and default
			$distroPath = "fedora-1-i386";
			$profilePath = "default";
			$root = "/var/www/html/testresults/fedora-1-i386/default/";
			}
		else if ($distro == 2 && $profile == 0){ # redhat default 
			$distroPath = "redhat-9-i386";
			$profilePath = "default";
		        $root = "/var/www/html/testresults/redhat-9-i386/default/";
			}
		else if ($distro == 3 && $profile == 0){ # Windows Xp default
			$distroPath = "windowsXP";
			$profilePath = "default";
			$root = "/var/www/html/testresults/windowsXP/default/";	
			}
        	else if ($distro == 0 && $profile == 1){ # suse-90-i586 net 2
			$distroPath = "suse-90-i586";
			$profilePath = "net_2_0";
			$root = "/var/www/html/testresults/suse-90-i586/net_2_0/";
			}
         	else if ($distro == 1 && $profile == 1){ # fedora net 2  
			$distroPath = "fedora-1-i386";
			$profilePath = "net_2_0";
			$root = "/var/www/html/testresults/fedora-1-i386/net_2_0/";
			}
        	else if ($distro == 2 && $profile == 1){ # redhat net 2  
			$distroPath = "redhat-9-i386";
			$profilePath = "net_2_0";
			$root = "/var/www/html/testresults/redhat-9-i386/net_2_0/";
			} 
		else if ($distro == 3 && $profile == 1){ # Windows Xp  net 2  
			$distroPath = "windowsXP";
			$profilePath = "net_2_0";
			$root = "/var/www/html/testresults/windowsXP/net_2_0/";
			}



         $dir = $root."xml/";
		$chart_location_1 = "testresults/$distroPath/$profilePath/charts/".$testsuite_key."_percent.png";
		$chart_location_2 = "testresults/$distroPath/$profilePath/charts/".$testsuite_key."_pass.png";
		$chart_location_3 = "testresults/$distroPath/$profilePath/charts/".$testsuite_key."_fail.png";

		#Displaying Charts
		if($_GET['image']==1) {
			print "$chart_location_1;";
			print "<h1>Progress Charts</h1>";
			print "<p><h4> Pass and Fail Percentages</h4><img src=\"$chart_location_1\"></p>";
			print "<p><h4>Number of Passes</h4><img src=\"$chart_location_2\"></p>";
			print "<p><h4>Number of Failures</h4><img src=\"$chart_location_3\"></p>";
			return;
		}
		
		$status_key = $_GET['status'];
		$file = $_GET['file'];
		if ($profile==0)
		$profilePath="default";
		else
		$profilePath="net_2_0";
			
		#Checking whether the input file is correct
		sanitize ($file);

		#Prepending the base directory and appending .xml to the input filename
		$file = $dir . "testresults-$profilePath-" .$file . ".xml";

		#Obtaining location of the recent chart for the particular testsuite
		$chart_url = "displayDetails.php?image=1&testsuite=$testsuite_key&profile=$profile&distro=$distro";

		#Displaying regressed testcases
		if ($_GET['regression'] == 1) {

			$file_1 = $_GET['file1'];
			sanitize ($file_1);//Checking whether input file1 is correct
			$file_1 = $dir ."testresults-". $profilePath."-".$file_1 . ".xml";

			print "<h1>Regressed testcases for " .  $_GET['testsuite'] . "</h1>";
			$testcases = fetch_regressed_testcases($testsuite_key,$file,$file_1);
			print "<br><a href=\"$chart_url\"><b><font size=\"2\">&lt;View Progress Charts></b></font></a><br><br><table border=1><tr><th><center>Sl.No.</center></th><th><center>Test Case Name</center></th><th><center>Message</center></th></tr>";	
			$count = 1;
			foreach ($testcases as $testcase) {
				 print "<tr><td>$count </td><td bgcolor=$color><a href=#".$count.">" . $testcase["name"]. "</a></td><td><pre>".$testcase["message"]."</pre></td><tr>";
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
			return;
		}

		$testcases = fetch_testcases($testsuite_key,$status_key,$file);
		if ($testcases[0] == "0") {

			#Displaying log message
			print "<h1>Testcase results for " .  $_GET['testsuite'] . "</h1><br>&nbsp;<a href=\"$chart_url\"><font size=\"2\"><b>&lt;View Progress Charts></b></font></a><br><br>";
			print "<pre>".$testcases[1]."</pre>";
			return;
		}
			
		#Displaying passed testcases
		if ($status_key == 0)
		{
			print "<h1>Passed testcases for " .  $_GET['testsuite'] . "</h1><br>&nbsp;<a href=\"$chart_url\"><font size=\"2\" ><b>&lt;View Progress Charts></b></font></a><br><br>";
			print "<table border=1><tr><th><center>Sl.No.</center></th><th><center>Test Case Name</center></th><th><center>Execution Time</center></th></tr>";
			$count = 1;
			foreach ($testcases as $testcase) {
				print "<tr><td>$count</td><td>" . $testcase["name"] . "</td><td>" . $testcase["exectime"] . "</td></tr>";	
				$count++;
			}
			print "<table>";
		}
		
		#Displaying not run testcases
		else if ($status_key == 2) 
		{
			print "<h1>Not run testcases for " .  $_GET['testsuite'] . "</h1><br>&nbsp;<a href=\"$chart_url\"><font size=\"2\" ><b>&lt;View Progress Charts></b></font></a><br><br>";
			print "<table border=1><tr><th><center>Sl.No.</center></th><th><center>Test Case Name</center></th><th><center>Message</center></th></tr>";
			$count = 1;
                        foreach ($testcases as $testcase) {
                                print "<tr><td>$count</td><td>" . $testcase["name"] . "</td><td><pre>" . $testcase["message"] . "</pre></td></tr>";
                                $count++;
                        }
			print "</table>";
		}
		
		#Displaying failed testcases
		else if ($status_key == 1) 
		{
			print "<h1>Failed testcases for " .  $_GET['testsuite'] . "</h1><br>&nbsp;<a href=\"$chart_url\"><font size=\"2\" ><b>&lt;View Progress Charts></b></font></a><br><br>";
			print "<table border =1><tr><th><b><center>Sl.No.</center></th></b><th><b><center>Test Case Name</center></b></th><th><b><center>Message</center></b></th></tr>";
			$count = 1;
			foreach ($testcases as $testcase) {
				print "<tr><td>$count </td><td bgcolor=$color><a href=#".$count.">" . $testcase["name"]. "</a></td><td><pre>".$testcase["message"]."</pre></td><tr>";
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

