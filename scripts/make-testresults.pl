
#!/usr/bin/perl -w

# Script to run tests in given list of directories and 
# create test result files.
#
# Author: Sachin Kumar <skumar1@novell.com>
#         Satya Sudha K (ksathyasudha@novell.com)
#         Ritvik Mayank (mritvik@novell.com)
#

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
#	       "$TEST_ROOT/mcs/class/Mono.Security.Win32",
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

@OTHER_DIRS = (
	       "$TEST_ROOT/mcs/class/System.Web.Services/Test/standalone"
                  );
#@COMPILER_DIRS = (
#		  "$TEST_ROOT/mcs/tests",
#                  "$TEST_ROOT/mcs/errors"
#                  );

#@RUNTIME_DIRS = (
#                 "$TEST_ROOT/mono/mono/tests",
#                 "$TEST_ROOT/mono/mono/mini"
#                 );

# Run the script for the following two profiles
@PROFILES= (
	    "default",
	    "net_2_0"
	    );

# Scan all dirs and run make to get test results file
for my $element (@NUNIT_DIRS){
    			      chdir $element ;
    			      print $element ;
   			      for (@PROFILES) {
        	     			       system "make PROFILE=$_ RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper run-test &" ;
		     			       sleep 5;
    			      }
}

# Execute Standalone tests
for my $otherelement (@OTHER_DIRS){
    				   chdir $otherelement ;
    				   print $otherelement ;
    				   for (@PROFILES) {	
 	             				    system "make PROFILE=$_ RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper test &" ;
                     				    sleep 5;
    				   }   
}

# Execute C# Compiler tests
chdir "$TEST_ROOT/mcs" ;
for (@PROFILES){
		system "make -k compiler-tests 2>&1" ;
		sleep 5;
}

# Execute VB Compiler tests
chdir "$TEST_ROOT/mcs/mbas/Test" ;
system "make MBAS_FLAGS= RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper run-test" ;
sleep 5;

# Execute runtime tests
chdir "$TEST_ROOT/mono/mono/tests" ;
system "make -k test 2>&1 > monotests" ;
sleep 5;
chdir "$TEST_ROOT/mono/mono/mini" ;
system "make -k rcheck 2>&1 > minitests"
												                                                                                                        
																									
