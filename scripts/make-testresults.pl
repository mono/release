#!/usr/bin/perl -w

# Script to run tests in given list of directories and 
# create test result files.
#
# Author: Sachin Kumar <skumar1@novell.com>

$DATE = `date +'%Y%m%d'`;
chomp $DATE ;

$TEST_ROOT = "/tmp/snapshot/$DATE";
#$TEST_ROOT = shift ;

$DOCROOT = "/var/www/html/tests/$DATE" ;

@NUNIT_DIRS = (
	       "$TEST_ROOT/mcs/class/Commons.Xml.Relaxng",
	       "$TEST_ROOT/mcs/class/Cscompmgd",
	       "$TEST_ROOT/mcs/class/Microsoft.JScript",
	       "$TEST_ROOT/mcs/class/Microsoft.VisualBasic",
	       "$TEST_ROOT/mcs/class/Mono.Directory.LDAP",
	       "$TEST_ROOT/mcs/class/Mono.Security",
	       "$TEST_ROOT/mcs/class/Mono.Security.Win32",
	       "$TEST_ROOT/mcs/class/Npgsql",
	       "$TEST_ROOT/mcs/class/System",
	       "$TEST_ROOT/mcs/class/System.Configuration.Install",
	       "$TEST_ROOT/mcs/class/System.Data",
	       "$TEST_ROOT/mcs/class/System.Drawing",
	       "$TEST_ROOT/mcs/class/System.Runtime.Remoting",
	       "$TEST_ROOT/mcs/class/System.Runtime.Serialization.Formatters.Soap",
	       "$TEST_ROOT/mcs/class/System.Security",
	       "$TEST_ROOT/mcs/class/System.Web.Services",
	       "$TEST_ROOT/mcs/class/System.XML",
	       "$TEST_ROOT/mcs/class/corlib"
	       );

@COMPILER_DIRS = (
		  "$TEST_ROOT/mcs/tests",
		  "$TEST_ROOT/mcs/errors"
		  );

@RUNTIME_DIRS = (
		 "$TEST_ROOT/mono/mono/tests",
		 "$TEST_ROOT/mono/mono/mini"
		 );

# create directory in doc root, for date when tests were executed
$res = mkdir "$DOCROOT" ;

=head

if (!$res)
{
    print $! ;
    exit;
}
# Scan all dirs and run make to get test resultsfile

# FIXME: make run-test hangs in one dir itself, 
# so does not execute tests in other dir
for ( @NUNIT_DIRS )
{
    chdir $_ ;
    system "make run-test-local" ;
}

=cut

# Execute C# Compiler tests
chdir "$TEST_ROOT/mcs/tests" ;
system "make run-test 2>&1 > $DOCROOT/mcstests" ;

chdir "$TEST_ROOT/mcs/errors" ;
system "make run-test 2>&1 > $DOCROOT/mcserrortests" ;

# Execute VB.NET tests
chdir "$TEST_ROOT/mcs/btests" ;
system "make run-test" ;
system "cp results.out $DOCROOT/mbastests" ;

# Execute runtime tests
chdir "$TEST_ROOT/mono/mono/tests" ;
system "make test 2>&1 > $DOCROOT/monotests" ;

chdir "$TEST_ROOT/mono/mono/mini" ;
system "make rcheck 2>&1 > $DOCROOT/minitests" ;
