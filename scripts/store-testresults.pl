#!/usr/bin/perl -w

# Script to read test results stored in files from a given list of 
# files and save results in a single xml file 
# 
#
# Author: Sachin Kumar <skumar1@novell.com>

use XML::DOM;

$DATE = `date +'%Y%m%d'`;
chomp $DATE ;

# Types of tests
$NUNITTESTS = 0 ;
$MCSTESTS = 1 ;
$RUNTIMETESTS = 2 ;

$TESTPASS = 0;
$TESTFAIL = 1;
$TESTNOTRUN = 2; 

$MCS_ROOT = "/home/skumar/monobuild/working/mcs";

# Create a DOM doc root

$root = new XML::DOM::Document;

$root->setXMLDecl ($root->createXMLDecl("1.0", "utf-8", undef));

$docRoot = $root->createElement("test-results");


@MCS_NUNIT_TESTDIRS = (
		       "$MCS_ROOT/class/Commons.Xml.Relaxng",
		       "$MCS_ROOT/class/Cscompmgd",
		       "$MCS_ROOT/class/Microsoft.JScript",
		       "$MCS_ROOT/class/Microsoft.VisualBasic",
		       "$MCS_ROOT/class/Mono.Directory.LDAP",
		       "$MCS_ROOT/class/Mono.Security",
		       "$MCS_ROOT/class/Mono.Security.Win32",
		       "$MCS_ROOT/class/Npgsql",
		       "$MCS_ROOT/class/System",
		       "$MCS_ROOT/class/System.Configuration.Install",
		       "$MCS_ROOT/class/System.Data",
		       "$MCS_ROOT/class/System.Drawing",
		       "$MCS_ROOT/class/System.Runtime.Remoting",
		       "$MCS_ROOT/class/System.Runtime.Serialization.Formatters.Soap",
		       "$MCS_ROOT/class/System.Security",
		       "$MCS_ROOT/class/System.Web.Services",
		       "$MCS_ROOT/class/System.XML",
		       "$MCS_ROOT/class/corlib"
		       );


$TESTFILES_ROOT = "/var/www/html/tests/$DATE" ;

@MONO_RUNTIME_TESTFILES = (
			   "$TESTFILES_ROOT/monotests",
			   "$TESTFILES_ROOT/minitests"
			   );

# Scan all mono runtime test files
for ( @MONO_RUNTIME_TESTFILES )
{
    my $tsresults = get_runtime_test_results ( $_ , "pass", "failed" ) ;

    # create testsuite element, with current time and date 
    my $testsuite = create_testsuite_element ( $tsresults, $RUNTIMETESTS, 0 ) ;
        
    my $log = create_log_element ( @$tsresults[0] ) ;

    $$testsuite->appendChild ( $$log );
    $docRoot->appendChild ( $$testsuite ) ;
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

for ( @MCS_NUNIT_TESTDIRS )
{
    my $parser = new XML::DOM::Parser;
    my $doc = $parser->parsefile ( $_."/TestResult.xml" );
    
    # get nunit testsuite results
    my $tsresults = get_nunit_testsuite_results ( $doc );
    
    # get data for each test case run
    my $tcresults = get_nunit_testcase_results ( $doc );

    my $tsexectime = 0 ;
    $tsexectime += $_->[4]
	foreach @$tcresults;

    # create testsuite element, with current time and date 
    my $testsuite = create_testsuite_element ( $tsresults, $NUNITTESTS, $tsexectime ) ;
    
    foreach (@$tcresults )
    {
	my $testcase = create_testcase_element ( $_ ) ;
	$$testsuite->appendChild ( $$testcase );
    }
    $docRoot->appendChild ( $$testsuite ) ;
}

$root->appendChild ( $docRoot ) ; 
$root->printToFile("testresults-".$DATE.".xml") ;

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
    my $doc = shift ;
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
		push @tcresults, [ $tcname, $TESTFAIL, ($msg->getFirstChild)->getNodeValue, $tcstacktrace, $tcexectime ];
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
    my ( $tsresults, $type, $tsexectime ) = @_;

    my @arr = split ('/', @$tsresults[0]);
     
    # Removing _test.dll from the testsuite name
    $arr[$#arr] =~ s/_test.dll$//g ;
    
    # create testsuite element and set it's attributes
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
    print $str ;

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
