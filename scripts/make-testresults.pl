#!/usr/bin/perl -w

# Script to run tests in given list of directories and
# create test result files.

system "export LD_LIBRARY_PATH=/home/build/src/install/lib";
system "export PATH=/home/build/src/install/bin:$PATH";

$DATE = `date +'%Y%m%d'`;
#$DATE = 20051019 ;
chomp $DATE ;

$TEST_ROOT = "/home/build/src/$DATE";
#$TEST_ROOT = shift ;

@NUNIT_DIRS = (
               "$TEST_ROOT/mcs/class/Commons.Xml.Relaxng",
               "$TEST_ROOT/mcs/class/Cscompmgd",
               "$TEST_ROOT/mcs/class/corlib",
               "$TEST_ROOT/mcs/class/Microsoft.JScript",
               "$TEST_ROOT/mcs/class/Microsoft.VisualBasic",
               "$TEST_ROOT/mcs/class/Mono.Directory.LDAP",
               "$TEST_ROOT/mcs/class/Mono.Posix",
               "$TEST_ROOT/mcs/class/Mono.Security",
#              "$TEST_ROOT/mcs/class/Mono.Security.Win32",
#              "$TEST_ROOT/mcs/class/Npgsql",
               "$TEST_ROOT/mcs/class/System",
               "$TEST_ROOT/mcs/class/System.Data.OracleClient",
               "$TEST_ROOT/mcs/class/System.ServiceProcess",
               "$TEST_ROOT/mcs/class/System.DirectoryServices",
               "$TEST_ROOT/mcs/class/System.Configuration.Install",
               "$TEST_ROOT/mcs/class/System.Data",
               "$TEST_ROOT/mcs/class/System.Drawing",
               "$TEST_ROOT/mcs/class/System.Runtime.Remoting",
               "$TEST_ROOT/mcs/class/System.Runtime.Serialization.Formatters.Soap",
               "$TEST_ROOT/mcs/class/System.Security",
               "$TEST_ROOT/mcs/class/System.Web.Services",
               "$TEST_ROOT/mcs/class/System.Web",
               "$TEST_ROOT/mcs/class/System.XML",
	       "$TEST_ROOT/mcs/class/Managed.Windows.Forms"
               );

@OTHER_DIRS = (
                  "$TEST_ROOT/mcs/class/System.Web.Services/Test/standalone"
                  );

@COMPILER_DIRS = (
                  "$TEST_ROOT/mcs/tests",
                  "$TEST_ROOT/mcs/errors"
                  );

@RUNTIME_DIRS = (
                 "$TEST_ROOT/mono/mono/tests",
                 "$TEST_ROOT/mono/mono/mini"
                 );

@PROFILES= (
		"default",
		"net_2_0"
	    );


# Scan all dirs and run make to get test resultsfile

#chdir "$TEST_ROOT/mcs/class/System.Runtime.Remoting";
#system "make TEST_HARNESS_FLAG=labels PROFILE=default RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper run-test &" ;

for my $element ( @NUNIT_DIRS )
{
    chdir $element ;
    print $element ;
    for (@PROFILES) {
        system "make TEST_HARNESS_FLAG=labels PROFILE=$_ RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper run-test &" ;
	sleep 5;
    }
}
for my $otherelement ( @OTHER_DIRS )
{
    chdir $otherelement ;
    print $otherelement ;
    for (@PROFILES) {	
        system "make TEST_HARNESS_FLAG=labels PROFILE=$_ RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper test &" ;
        sleep 5;
    }   
}

# Execute C# Compiler tests
chdir "$TEST_ROOT/mono" ;
system "make -k mcs-do-compiler-tests 2>&1" ;

chdir  "$TEST_ROOT/mcs/class/System.Web.Services/Test/standalone" ;
system "make test-clients";

chdir  "$TEST_ROOT/mcs/errors" ;
system "mv mcs.log mcserrortests" ;
system "mv gmcs.log gmcserrortests" ;
    
chdir "$TEST_ROOT/mcs/mbas/Test" ;
system "make MBAS_FLAGS= RUNTIME=$TEST_ROOT/mono/runtime/mono-wrapper run-test" ;

chdir "$TEST_ROOT/mcs/mbas/Test/errors" ;
system "mv TestResults.log  mbas-errors.results" ;

chdir "$TEST_ROOT/mcs/mbas/Test/tests" ;
system "mv TestResults.log  mbas-tests.results" ;

# Execute runtime tests
chdir "$TEST_ROOT/mono/mono/tests" ;
system "make -k check 2>&1 > monotests" ;

chdir "$TEST_ROOT/mono/mono/mini" ;
system "make -k check 2>&1 > minitests";

chdir "$TEST_ROOT/mcs/class/System.Data/Test/DataProviderTests" ;
system "make DATABASE=mssql run-test" ;

chdir "$TEST_ROOT/mcs/class/System.Data/Test/DataproviderTests/dataprovidertests" ;
system "cp TestResult.log mssql-dataprovidertest" ;
chdir "cd $TEST_ROOT/mcs/class/System.Data/Test/DataproviderTests/dataadaptortests" ;
system "cp TestResult.log mssql-dataadaptertest" ;

chdir "$TEST_ROOT/mcs/class/Microsoft.VisualBasic/Test/standalone" ;
system "cp results-default.log msvb-standalone.log" ;
system "cp results-net_2_0.log msvb2-standalone.log" ;
