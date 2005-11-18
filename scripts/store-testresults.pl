
#!/usr/bin/perl -w

# Script to read test results stored in files from a given list of 
# files and save results in a single xml file 
# 
#
# Author: Sachin Kumar <skumar1@novell.com>

use XML::DOM;
use File::Basename;

#$DATE=20051017;
$DATE = `date +'%Y%m%d'`;
chomp $DATE ;

# Types of tests
$NUNITTESTS = 0 ;
$MCSTESTS = 1 ;
$RUNTIMETESTS = 2 ;
$OTHERTESTS = 3 ;

$TESTPASS = 0;
$TESTFAIL = 1;
$TESTNOTRUN = 2; 

$MCS_ROOT = "/home/build/src/$DATE/mcs";
$MONO_ROOT = "/home/build/src/$DATE/mono";


@MCS_NUNIT_TESTDIRS = (
                       "$MCS_ROOT/class/Commons.Xml.Relaxng",
                       "$MCS_ROOT/class/Cscompmgd",
                       "$MCS_ROOT/class/Microsoft.JScript",
                       "$MCS_ROOT/class/Microsoft.VisualBasic",
                       "$MCS_ROOT/class/Mono.Directory.LDAP",
                       "$MCS_ROOT/class/Mono.Posix",
                       "$MCS_ROOT/class/Mono.Security",
                       "$MCS_ROOT/class/Managed.Windows.Forms",
#                       "$MCS_ROOT/class/Npgsql",
                       "$MCS_ROOT/class/System",
                       "$MCS_ROOT/class/System.Configuration.Install",
                       "$MCS_ROOT/class/System.Data",
                       "$MCS_ROOT/class/System.Data.OracleClient",
                       "$MCS_ROOT/class/System.DirectoryServices",
                       "$MCS_ROOT/class/System.ServiceProcess",
                       "$MCS_ROOT/class/System.Drawing",
                       "$MCS_ROOT/class/System.Runtime.Remoting",
                       "$MCS_ROOT/class/System.Runtime.Serialization.Formatters.Soap",
                       "$MCS_ROOT/class/System.Security",
                       "$MCS_ROOT/class/System.Web.Services",
                       "$MCS_ROOT/class/System.Web",
                       "$MCS_ROOT/class/System.XML",
                       "$MCS_ROOT/class/corlib",
                       "$MCS_ROOT/class/System.Web.Services/Test/standalone",
                       );

$TESTFILES_ROOT = "/var/www/html/tests/$DATE" ;

@MONO_RUNTIME_TESTFILES = (
			   "$MONO_ROOT/mono/tests/monotests",
			   "$MONO_ROOT/mono/mini/minitests"
			   );

@MCS_TESTFILES = (
		  "$MCS_ROOT/tests"
		  );
		  
@SYS_DATA_PROVIDER_A = (
                        "$MCS_ROOT/class/System.Data/Test/DataProviderTests/dataadaptertests"
                       );

@SYS_DATA_PROVIDER_R = (
                        "$MCS_ROOT/class/System.Data/Test/DataProviderTests/datareadertests"
                       );

@MSVB_STANDALONE = ( 
		    "$MCS_ROOT/class/Microsoft.VisualBasic/Test/standalone"
		   );	


@NEW_MBAS_TESTFILES = (
		   "$MCS_ROOT/mbas/Test/errors/mbas-errors.results",
		   "$MCS_ROOT/mbas/Test/tests/mbas-tests.results",
#		   "$MCS_ROOT/mbas/Tests/dlls/mbas-dlls.results",
		   );

@RERRORS_MBAS = (
		"$MCS_ROOT/mbas/Test/rerrors",
		);

@MCS_ERRORDIR = (
		   "$MCS_ROOT/errors"
		   );

@OTHER_TESTFILES = (
		    "$MCS_ROOT/class/System.Web.Services/Test/standalone"
		    );

@PROFILES = ( "default",
              "net_2_0"
            );      
		

for my $profile (@PROFILES)
{ 
    print "$profile\n";

  # Create a DOM doc root
  $root = new XML::DOM::Document;
  
  #$root->setXMLDecl ($root->createXMLDecl("1.0", "iso8859-1", undef));
  $root->setXMLDecl ($root->createXMLDecl("1.0", "iso-8859-1")); 
  $docRoot = $root->createElement("test-results");

  # wsdl tests
  if ($profile eq "default") {
    for my $element ( @OTHER_TESTFILES )
    { 
      open(FILE, $element."/WsdlTestResult.xml" )|| print "can't open file :$element/WsdlTestResult.xml for reading",next  ;
      print $element."/WsdlTestResult.xml\n" ;
      nunit_results ( $element."/WsdlTestResult.xml", $OTHERTESTS, $profile ) ;
     }
      
    for my $nunitfile( @OTHER_TESTFILES )
    { 
      my $file=$nunitfile ;
    open(FILE, $nunitfile."/TestResult.xml") || print "can't open file:$nunitfile/TestResult.xml for reading",next  ;
    print $nunitfile."/TestResult.xml\n" ;
    nunit_results ( $nunitfile."/TestResult.xml", $NUNITTESTS , $profile) ;
    }

# Scan all mono runtime test files 
   for my $runtime( @MONO_RUNTIME_TESTFILES )
   {
     my $tsresults = get_runtime_test_results ( $runtime , "pass", "failed" ) ;
    #create testsuite element, with current time and date 
     my $testsuite = create_testsuite_element ( $tsresults, $RUNTIMETESTS, 0 , $profile ) ;
     my $log = create_log_element ( @$tsresults[0] ) ;
     $$testsuite->appendChild ( $$log );
     $docRoot->appendChild ( $$testsuite ) ;
   }
 
  # New mbas tests 
   for my $newmbastest( @NEW_MBAS_TESTFILES )
   {
     my ($tsresults, $tcresults) = get_new_mbastest_results ( $newmbastest , "OK", "FAILED" ) ;

   # create testsuite element, with current time and date
     append_testsuite ( $tsresults, $tcresults, $MCSTESTS, 0, $profile ) ;
   }

}

 #mcs  error tests
  
  for my $dir ( @MCS_ERRORDIR )
  {
    my $file=$dir;
    if($profile eq "default") {
      $file.="/mcserrortests";
    } else {
      $file.="/gmcserrortests";
    }
    print $file."\n";
    my ($tsresults, $tcresults) = get_mcserror_test_results ( $file , "OK", "KNOWN" ) ;
    append_testsuite ( $tsresults, $tcresults, $MCSTESTS, 0, $profile ) ;
  }
  
# Mcs test
    for my $testfile ( @MCS_TESTFILES )
   {
     my $file=$testfile;
     if ($profile eq "default") {
        $file.="/mcs.log";
     } else {
        $file.="/gmcs.log";
     }
     print $file."\n";
     my ($tsresults, $tcresults )  = get_mcs_test_results ( $file, "OK", "KNOWN") ;
     append_testsuite ( $tsresults, $tcresults, $MCSTESTS, 0, $profile ) ;
   }
   
# System.Data DataProvider test for adapter
     for my $mydataadapter ( @SYS_DATA_PROVIDER_A )
    {
      my $file=$mydataadapter;
      $file.="/mssql-dataadaptertest.log";
      print $file."\n";
      my ($tsresults, $tcresults )  = get_data_adapter_test_results ($file, "OK", "FAIL") ;
      append_testsuite ( $tsresults, $tcresults, $OTHERTESTS, 0, $profile ) ;
    }

# System.Data DataProvider test for reader
     for my $mydatareader ( @SYS_DATA_PROVIDER_R )
    {
      my $file=$mydatareader;
      $file.="/mssql-datareadertest.log";
      print $file."\n";
      my ($tsresults, $tcresults )  = get_data_reader_test_results ($file, "OK", "FAIL") ;
      append_testsuite ( $tsresults, $tcresults, $OTHERTESTS, 0, $profile ) ;
    }

# MS VB stand alone test
    for my $msvbstandalone ( @MSVB_STANDALONE )
   {
     my $file=$msvbstandalone;
     if ($profile eq "default") {
        $file.="/msvb-standalone.log";
     } else {
        $file.="/msvb2-standalone.log";
     }
     print $file."\n";
     my ($tsresults, $tcresults )  = get_msvb_standalone_results ($file, "PASS", "FAIL") ;
     append_testsuite ( $tsresults, $tcresults, $MCSTESTS, 0, $profile ) ;
   }
 


    for my $nunitfile( @MCS_NUNIT_TESTDIRS )
    { my $file=$nunitfile ;
    open(FILE, $nunitfile."/TestResult-$profile.xml") || print "can't open file:$nunitfile/TestResult-$profile.xml for reading",next  ;
    print $nunitfile."/TestResult-$profile.xml\n" ;
    nunit_results ( $nunitfile."/TestResult-$profile.xml", $NUNITTESTS , $profile) ;
    }

#for mcs/mbas/Test/rerrors
for my $rerrors ( @RERRORS_MBAS )
    {
      open(FILE, $rerrors."/TestResult-$profile.xml" )|| print "can't open file :$rerrors/TestResult-$profile.xml for reading",next  ;
      print $rerrors."/TestResult-$profile.xml\n" ;
      nunit_results ( $rerrors."/TestResult-$profile.xml", $MCSTESTS, $profile ) ;
     }

  $root->appendChild ( $docRoot ) ; 
  $root->printToFile("testresults-$profile-".$DATE.".xml") ;

}

#
sub nunit_results
{
    my ( $file, $type, $profile ) = @_ ;
    my $parser = new XML::DOM::Parser;
    my $doc = $parser->parsefile ( $file );

    # get nunit testsuite results
    my $tsresults = get_nunit_testsuite_results ( $doc );
    
    # get data for each test case run
    my $tcresults = get_nunit_testcase_results ( $doc ,$type);

    my $tsexectime = 0 ;
    $tsexectime += $_->[4]
	foreach @$tcresults;

    $tsexectime = sprintf("%.3f", $tsexectime);

    append_testsuite ( $tsresults, $tcresults, $type, $tsexectime, $profile, $file ) ;
}

sub append_testsuite
{
#    my ( $tsresults, $tcresults, $type, $tsexectime ) = @_ ;
    my ( $tsresults, $tcresults, $type, $tsexectime, $profile, $file ) = @_ ;

    # create testsuite element, with current time and date 
#    my $testsuite = create_testsuite_element ( $tsresults, $type, $tsexectime ) ;
    my $testsuite = create_testsuite_element ( $tsresults, $type, $tsexectime, $profile, $file ) ;
    foreach (@$tcresults )
    {
	my $testcase = create_testcase_element ( $_ ) ;
	$$testsuite->appendChild ( $$testcase );
    }
    $docRoot->appendChild ( $$testsuite ) ;
}

sub get_mcserror_test_results {

    my ( $testresult, $PASS, $FAIL ) = @_ ;
    my @tsresults = ($testresult, 0, 0, 0) ;
    my @tcresults = () ;

    open (FILEHANDLE, $testresult);
    
    # cs-12.cs...INCORRECT ERROR 
    # cs0017.cs...SUCCESS
    while (<FILEHANDLE>) 
    {	
	my $testcase = $_ ;
	my @arr = split ('\.\.\.', $testcase);	

	if ( $testcase =~ /$FAIL/ )
	{
	    $tsresults[2]++ ; # increment count 

	    my $file =  "$MCS_ROOT/errors/$arr[0].log" ;
	    if (open (FILE, $file) != 1) {
		push @tcresults, [ $arr[0], $TESTFAIL, $arr[1], "", 0];
	    }
	    else {
		my $stacktrace = "" ;
		$stacktrace = $stacktrace.$_ foreach (<FILE>);
		push @tcresults, [ $arr[0], $TESTFAIL, $arr[1], $stacktrace, 0] ;  
	    }
	}

	if ( $testcase =~ /$PASS/ )
	{
	    $tsresults[1]++ ; # increment count 
	    push @tcresults, [ $arr[0], $TESTPASS, "", "", 0] ;  
	}
    }
    return (\@tsresults, \@tcresults ) ;
}   

sub get_mcs_test_results {

    my ( $testresult, $PASS, $FAIL ) = @_ ;
    my @tsresults = ($testresult, 0, 0, 0) ;
    my @tcresults = () ;

    open (FILEHANDLE, $testresult);
    
    # cs-12.cs...INCORRECT ERROR 
    # cs0017.cs...SUCCESS
    while (<FILEHANDLE>) 
    {	
	my $testcase = $_ ;
	my @arr = split ('\.\.\.', $testcase);	

	if ( $testcase =~ /$FAIL/ )
	{
	    $tsresults[2]++ ; # increment count 

	    my $file =  "$MCS_ROOT/tests/$arr[0].log" ;
	    if (open (FILE, $file) != 1) {
		push @tcresults, [ $arr[0], $TESTFAIL, $arr[1], "", 0];
	    }
	    else {
		my $stacktrace = "" ;
		$stacktrace = $stacktrace.$_ foreach (<FILE>);
		push @tcresults, [ $arr[0], $TESTFAIL, $arr[1], $stacktrace, 0] ;  
	    }
	}

	if ( $testcase =~ /$PASS/ )
	{
	    $tsresults[1]++ ; # increment count 
	    push @tcresults, [ $arr[0], $TESTPASS, "", "", 0] ;  
	}
    }
    return (\@tsresults, \@tcresults ) ;
}

sub get_data_adapter_test_results
 {
     my ( $testresult, $PASS, $FAIL ) = @_ ;
     my @tsresults = ($testresult, 0, 0, 0) ;
     my @tcresults = () ;
     my $i = 0;

     open (FILEHANDLE, $testresult);

     while (<FILEHANDLE>)
     {
       my $testcase = $_ ;
       my @arr = split (' ', $testcase);

       $arr[1] = substr ($arr[1], 0, -1) if ( $#arr == 2 ) ; # test name

       if ( $testcase =~ /$FAIL/ )
       {
           ($tmp = $testresult) =~ s/.log/-$arr[1].log/ ;
           $tsresults[2]++ ; # increment count
           open (FILE, $tmp);
           my $stacktrace = "" ;
           $stacktrace = $stacktrace.$_ foreach (<FILE>);

           push @tcresults, [ $arr[1], $TESTFAIL, "", $stacktrace, 0] ;
       }
       if ( $testcase =~ /$PASS/ )
       {
           $tsresults[1]++ ; # increment count
           push @tcresults, [ $arr[1], $TESTPASS, "", "", 0] ;
       }
     }
     return (\@tsresults, \@tcresults ) ;
 }

 sub get_data_reader_test_results
 {
     my ( $testresult, $PASS, $FAIL ) = @_ ;
     my @tsresults = ($testresult, 0, 0, 0) ;
     my @tcresults = () ;
     my $i = 0;

     open (FILEHANDLE, $testresult);

     while (<FILEHANDLE>)
     {
       my $testcase = $_ ;
       my @arr = split (' ', $testcase);

       $arr[1] = substr ($arr[1], 0, -1) if ( $#arr == 2 ) ; # test name

       if ( $testcase =~ /$FAIL/ )
       {
           ($tmp = $testresult) =~ s/.log/-$arr[1].log/ ;
           $tsresults[2]++ ; # increment count
           open (FILE, $tmp);
           my $stacktrace = "" ;
           $stacktrace = $stacktrace.$_ foreach (<FILE>);

           push @tcresults, [ $arr[1], $TESTFAIL, "", $stacktrace, 0] ;
       }
       if ( $testcase =~ /$PASS/ )
       {
           $tsresults[1]++ ; # increment count
           push @tcresults, [ $arr[1], $TESTPASS, "", "", 0] ;
       }
     }
     return (\@tsresults, \@tcresults ) ;
 }

sub get_msvb_standalone_results
{
    my ( $testresult, $PASS, $FAIL ) = @_ ;
	print "$testresult\n";
 #   print ("\n LOOKING FOR ". $testresult. "\n" );
    my @tsresults = ($testresult, 0, 0, 0) ;
    my @tcresults = () ;
	
    my @arr = split ('/', $testresult);
    my $dirname = dirname($testresult);
    my $filename = basename($testresult);
                                                                                                                            
    # Removing _test.dll from the testsuite name
    $arr[$#arr] =~ s/_test.dll$//g ;
    #$filename =~ s/_test.dll$//g ;
                                                                                                                            
    # Removing .results from the testsuite name
    $arr[$#arr] =~ s/.results$//g ;
   # $filename =~ s/.results$//g ;

    my $testsuite_name = $arr[$#arr -1 ];
#    print ("\n TESTSUIT ". $testsuite_name . "\n" );
    open (FILEHANDLE, $testresult);
    
    # cs-12.cs...INCORRECT ERROR 
    # cs0017.cs...SUCCESS
    while (<FILEHANDLE>) 
    {	
	my $testcase = $_ ;
	my @arr = split ('\: ', $testcase);
#	print "arr [0] = $arr[0], [1] = $arr[1]\n";
	if ( $testcase =~ /$FAIL/ )
	{
	    $tsresults[2]++ ; # increment count 
            $arr[0] =~ s/[ \t]+$//g;
	    my $testfile_name = $arr[1];
	    my $testfile_name =~ s/^\.\///g ;
	    $arr [0] =~ s/^\.\///g;
	    my $file =  "$arr[1]" ;
	    my $file =  "$MCS_ROOT/class/Microsoft.VisualBasic/Test/standalone/$file" ;
	    $file .= ".log";
	    $arr [0] =~ s/\//:/g ;
	    if (open (FILE, $file) != 1) {
#		print "Couldn't open $file\n";
		push @tcresults, [ $arr[1], $TESTFAIL, "", 0];
	    }
	    else {
		my $stacktrace = "" ;
		$stacktrace = $stacktrace.$_ foreach (<FILE>);
#		print "stacktrace = $stacktrace\n";
		push @tcresults, [ $arr[1], $TESTFAIL, $stacktrace, 0] ;  
	    }
	}

	if ( $testcase =~ /$PASS/ )
	{
	    $tsresults[1]++ ; # increment count 
	    push @tcresults, [ $arr[1], $TESTPASS, "", "", 0] ;  
	}
    }
    return (\@tsresults, \@tcresults ) ;


}

sub get_new_mbastest_results {

    my ( $testresult, $PASS, $FAIL ) = @_ ;
	print "$testresult\n";
#    print ("\n LOOKING FOR ". $testresult. "\n" );
    my @tsresults = ($testresult, 0, 0, 0) ;
    my @tcresults = () ;
	
    my @arr = split ('/', $testresult);
    my $dirname = dirname($testresult);
    my $filename = basename($testresult);
                                                                                                                            
    # Removing _test.dll from the testsuite name
    $arr[$#arr] =~ s/_test.dll$//g ;
    #$filename =~ s/_test.dll$//g ;
                                                                                                                            
    # Removing .results from the testsuite name
    $arr[$#arr] =~ s/.results$//g ;
   # $filename =~ s/.results$//g ;

    my $testsuite_name = $arr[$#arr -1 ];
#	print ("\n TESTSUIT ". $testsuite_name . "\n" );
    open (FILEHANDLE, $testresult);
    
    # cs-12.cs...INCORRECT ERROR 
    # cs0017.cs...SUCCESS
    while (<FILEHANDLE>) 
    {	
	my $testcase = $_ ;
	my @arr = split ('\: ', $testcase);	
	if ( $testcase =~ /$FAIL/ )
	{
	    $tsresults[2]++ ; # increment count 
            $arr[0] =~ s/[ \t]+$//g;
	    my $testfile_name = $arr[0];
	    my $testfile_name =~ s/^\.\///g ;
	    $arr [0] =~ s/^\.\///g;
	    my $file =  "$arr[0]" ;
	    my $file =  "$MCS_ROOT/mbas/Test/$testsuite_name/$file" ;
	    $file .= ".log";
	    $arr [0] =~ s/\//:/g ;
	    if (open (FILE, $file) != 1) {
		push @tcresults, [ $arr[0], $TESTFAIL, "", 0];
	    }
	    else {
		my $stacktrace = "" ;
		$stacktrace = $stacktrace.$_ foreach (<FILE>);
		push @tcresults, [ $arr[0], $TESTFAIL, $stacktrace, 0] ;  
	    }
	}

	if ( $testcase =~ /$PASS/ )
	{
	    $tsresults[1]++ ; # increment count 
	    push @tcresults, [ $arr[0], $TESTPASS, "", "", 0] ;  
	}
    }
    return (\@tsresults, \@tcresults ) ;
}   


sub get_runtime_test_results
{
    my ( $testresult, $PASS, $FAIL ) = @_ ;
    my @tsresults = ($testresult, 0, 0, 0) ;
    
    open (FILEHANDLE, $testresult);
    if ( $testresult =~ /minitests/ )
    {
	while (<FILEHANDLE>) 
	{
	    if( /^Results/ ) 
	    {
		my @arr = split (' ', $_);
		$arr[3] = substr ($arr[3], 0, -1);
		$arr[5] = substr ($arr[5], 0, -1);
		$tsresults[1] += ($arr[3] - $arr[5]) ;
		$tsresults[2] += $arr[5] ;
	    }
	}
    }
    else
    {
	while (<FILEHANDLE>) 
	{
	    $tsresults[1]++ if /$PASS/ ;
	    $tsresults[2]++ if /$FAIL/ ;
	}
    }
    
    return \@tsresults ;
    
}

sub get_nunit_testsuite_results
{
    my $doc = shift ;
    my @attrs = ( 'name', 'total', 'failures', 'not-run' ) ;
    my @tsresults = () ;
    
    my $nodes = $doc->getElementsByTagName ("test-results");
    my $len = $nodes->getLength;
    
    if($nodes->getLength != 1)
    {
	print "Unexpected doc: may have more number of test-result tags";
	return \@tsresults;
    }
    
    my $node = $nodes->item ( 0 );
    my $i = 0 ;
    for (@attrs)
    {
	my $n = $node->getAttributeNode ( $_ ) ;
	$tsresults[$i++] = $n->getValue ;
    }
    
    $tsresults[1] -= $tsresults[2] ; # pass = total - fail 
    return \@tsresults;
}   

sub get_nunit_testcase_results
{
    my ($doc, $type) = @_ ;
    my @attrs = ( 'name', 'executed', 'success', 'time' ) ;
    my @tcresults = () ;
    
    my $tcname ;        # list contains names of each testcase
    my $tcstatus ;     # status: pass, fail, not run
    my $tcmessage ;    # messages for each test case, if any, else empty
    my $tcstacktrace ; # stack traces for each test case, else empty
    my $tcexectime ;
    
    for my $node ($doc->getElementsByTagName ("test-case"))
    {
	# intializing with default values
	$tcexectime = 0 ;
	$tcmessage = "" ;
	$tcstacktrace = "" ;
	
	$tcname = ($node->getAttributeNode($attrs[0]))->getValue ;
	if ($type != $OTHERTESTS) {
		$tcname =~ s/\w*\.// ;
	}
	if(($node->getAttributeNode($attrs[1]))->getValue ne "False")
	{
	    if(($node->getAttributeNode($attrs[2]))->getValue eq "False")
	    {
		$tcstatus = $TESTFAIL ;
		
		my $msglist = $node->getElementsByTagName ("message");
		my $msg = $msglist->item(0) ;

		my $stlist = $node->getElementsByTagName ("stack-trace");
		my $st = $stlist->item(0) ;
		if ( $st->hasChildNodes == 1)
		{
		    $tcstacktrace = ($st->getFirstChild)->getNodeValue ;
		}
		if ( $msg->hasChildNodes == 1)
		{
			$msg_value = ($msg->getFirstChild)->getNodeValue;
		}
		push @tcresults, [ $tcname, $TESTFAIL, $msg_value, $tcstacktrace, $tcexectime ];
	    }
	    
	    else
	    {
		push @tcresults, [ $tcname, $TESTPASS, "", "", ($node->getAttributeNode ($attrs[3]))->getValue ];
	    }
	}
	else
	{
	    my $msglist = $node->getElementsByTagName ("message");
	    my $msg = $msglist->item(0) ;
	    push @tcresults, [ $tcname, $TESTNOTRUN, ($msg->getFirstChild)->getNodeValue, "", $tcexectime ];
	}
    }
    return \@tcresults ;
}   

sub create_testsuite_element
{
    my ( $tsresults, $type, $tsexectime, $profile, $file ) = @_;

    my @arr = split ('/', @$tsresults[0]);
     
    # Removing _test.dll from the testsuite name
    if ( $file =~ /rerrors\/TestResult\-default\.xml/ ) 	   
    	{
	   $arr[$#arr] =~ s/_btest.dll$//g ;
	   $arr[$#arr] =~ s/_btest_default.dll$//g ;
	}
    else
    	{
	   $arr[$#arr] =~ s/_test.dll$//g ;
	   $arr[$#arr] =~ s/_test_$profile.dll$//g ;
	}   
    # Removing .log from the testsuite name
    $arr[$#arr] =~ s/.log$//g ;

    # Removing .results from the testsuite name
    $arr[$#arr] =~ s/.results$//g ;

    my $testsuite = $root->createElement("testsuite");
    
    $testsuite->setAttribute("name" , $arr[$#arr] ) ;
    $testsuite->setAttribute("pass" , @$tsresults[1] ) ;
    $testsuite->setAttribute("fail" , @$tsresults[2] ) ;
    $testsuite->setAttribute("notrun" , @$tsresults[3] ) ;
    $testsuite->setAttribute("exectime" , $tsexectime ) ;
    $testsuite->setAttribute("type" , $type ) ;
    $testsuite->setAttribute("date" , $DATE ) ;
    return \$testsuite ;
}

sub create_log_element
{
    $logfile = shift ;
    open (FILEHANDLE, $logfile);
    my $str = "";
    $str = $str.$_ foreach (<FILEHANDLE>) ;

   # my $str = <FILEHANDLE> ;
   # print $str ;

    my $log = $root->createElement("testsuite-log");
    my $logdata = $root->createCDATASection($str);
    $log->appendChild ( $logdata ) ;
    return \$log ;
}

sub create_testcase_element
{
    my $tcresult = shift ;
    
    # create testcase element and set it's attributes
    my $testcase = $root->createElement("testcase");
    
    $testcase->setAttribute( "name" , $tcresult->[0] ) ;
    $testcase->setAttribute( "status" , $tcresult->[1] ) ;
    $testcase->setAttribute( "date" , $DATE ) ;

    if( $tcresult->[1] != $TESTNOTRUN )
    {
	$testcase->setAttribute( "exectime" , $tcresult->[4] ) ;
    }
    
    if ( $tcresult->[1] == $TESTNOTRUN || $tcresult->[1] == $TESTFAIL )
    {
	my $message = $root->createElement("message");
	my $messagedata = $root->createCDATASection($tcresult->[2]);
	$message->appendChild ( $messagedata ) ;
	$testcase->appendChild ( $message ) ;
    }
    
    if ( $tcresult->[1] == $TESTFAIL )
    {
	my $stacktrace = $root->createElement("stacktrace");
	my $stdata = $root->createCDATASection($tcresult->[3]);
	$stacktrace->appendChild ( $stdata ) ;
	$testcase->appendChild ( $stacktrace ) ;
    }
    
    return \$testcase ;
}
