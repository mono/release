#!/usr/bin/perl
use Getopt::Std;
use File::Basename;
use XML::DOM;
use POSIX;
use Switch;
use Getopt::Long;
use strict;


my $usage =<< "END";
Usage : perl generate_charts_consolidated.pl --distro <distro_name> 
                          --profile <profile>
                          --start <start date>
                          [--root <dest dir>]
                          --help 
END

my ($distro_name, $profile, $start_date, $root_dir, $help);

my $result = GetOptions("distro:s"=>\$distro_name,
                        "profile:s"=> \$profile,
                        "start:s"=>\$start_date,
                        "root:s"=>\$root_dir,
                        "help!"=>\$help);
if (!$result || $help) {
  print $usage;
  exit;
}
if (!defined $distro_name || !defined($profile)) {
  print $usage;
  exit;
}

if (!defined $start_date) {
  $start_date = "0";
}
if (!defined $root_dir) {
  $root_dir = "/var/www/html/testresults";
}

my @dates = ();
my %test_suite_names = ();
my ($xml_dir, $chart_dir);

$root_dir .= "/$distro_name/$profile";
if ( !(-e $root_dir) || !(-d $root_dir)) {
   print "Invalid distro name\n";
   exit;
}

$xml_dir = $root_dir."/xml/";
$chart_dir = $root_dir."/charts/";
#$chart_dir = "/var/www/html/new_charts/$distro_name/$profile";

my @filenames = get_sorted_filenames($xml_dir, $start_date,$profile);
my %pass_fail_stats = ();
my %perc_stats = ();
my %total_stats = ();
foreach my $file (@filenames) {
  print "Processing file : $file...\n";
  get_stats ($file, \%pass_fail_stats, \%perc_stats, \%total_stats, \@dates, \%test_suite_names);
}

my $output_file = "$root_dir/testresults.dat";
write_data_to_file(\%pass_fail_stats, \@dates, \%test_suite_names, $output_file, 1 );
generate_charts($output_file, $chart_dir, "individual" );
$output_file = "$root_dir/testresults_perc.dat";
write_data_to_file(\%perc_stats, \@dates, \%test_suite_names, $output_file, 1 );
generate_charts($output_file, $chart_dir, "consolidated" );

$output_file = "$root_dir/total.dat";
write_data_to_file(\%total_stats, $output_file, 0, 0, 0 );
generate_charts($output_file, $chart_dir, "total" );

sub get_sorted_filenames
{
        my ($dir, $start_date, $profile) = (@_);
        opendir(DIR,$dir);
        my $files_count = 0;
        my @files =  readdir(DIR);
        my @sorted_files = ();
        my $file_count = 0;

        foreach my $file(@files) {
            if ($file =~/^testresults\-$profile\-(\d{8}).xml$/) {
            #if ($file =~/^testresults\-(\d{8}).xml$/) {
              my $file_date = $1;
              # Since dates are of teh YYYYMMDD format, we can 
              # safely compare them as numbers
              if ($file_date >= $start_date) {
                $sorted_files[$file_count] = $dir . $file;
                $file_count++;
              }
            }
        }

        @sorted_files = sort(@sorted_files);
        return @sorted_files;
}

sub get_stats {

  my ($filename, $pass_fail_hash, $perc_hash, $total_hash, $dates, $keys) = (@_);
  my $xmlParser = new XML::DOM::Parser();
  my $doc = $xmlParser->parsefile($filename);
  my @testsuites = $doc->getElementsByTagName("testsuite");
  my $date = get_date_from_filename($filename);
  push (@$dates, $date);
  my $num_passes = 0;
  my $num_failures = 0;

  foreach my $testsuite (@testsuites) {
    my $testsuite_name = $testsuite->getAttribute("name");
    $keys->{$testsuite_name}= 1;
    my $testsuite_failures = $testsuite->getAttribute("fail");
    $num_failures += $testsuite_failures;
    $pass_fail_hash->{$testsuite_name}{$date}{"fail"} = $testsuite_failures;
    my $testsuite_passes = $testsuite->getAttribute("pass");
    $num_passes += $testsuite_passes;
    $pass_fail_hash->{$testsuite_name}{$date}{"pass"} = $testsuite_passes;
    my $total = $testsuite_passes + $testsuite_failures ;
    if ($total == 0) {
      next;
    }
    $perc_hash->{$testsuite_name}{$date}{"pass"} = $testsuite_passes/$total * 100;
    $perc_hash->{$testsuite_name}{$date}{"fail"} = $testsuite_failures/$total * 100;
    $total_hash->{$date}{"fail"} = $num_failures;
    $total_hash->{$date}{"pass"} = $num_passes;
    $total_hash->{$date}{"fail_perc"} = $num_failures / ($num_passes + $num_failures) * 100;
    $total_hash->{$date}{"pass_perc"} = $num_passes / ($num_passes + $num_failures) * 100;
  }
}

sub get_date_from_filename {
  my $fullPath = shift;
  my $filename = basename($fullPath);
  my $date = "";
  if ($filename =~ /(\d{8})\.xml$/) {
     $date = $1; 
  } else {
    print "Invalid file name : $filename";
  }
  return $date;
}

sub write_data_to_file {
  my ($hash, $dates, $keys, $file, $flag) = (@_);
  if ( $flag == 1 )
  {
	  open (INFILE, "<$file"); #|| die ("Cannot open file:$file for reading!! \n");
	  my @lines = <INFILE>;
	  close(INFILE); 
	  open (OUTFILE, ">$file") || die ("Cant open file:$file for writing!! \n");

	  my @existing_testsuites_list = split(/\s/,$lines[0]);
	  if ($existing_testsuites_list[0] eq "#") {
	    undef $existing_testsuites_list[0];
	  }
	  for my $test_suite (@existing_testsuites_list) {
	    $keys->{$test_suite} = 0;
	  }

	  my $num_existing_elements = $#existing_testsuites_list;
	  for my $key (keys %$keys) {
	    if ($keys->{$key} == 1) {
	        push (@existing_testsuites_list, $key);
	    }
	  }
	  my $num_new_elements = $#existing_testsuites_list;
	  my $append_string= "";
	  for (my $i = 0; $i < $num_new_elements- $num_existing_elements; $i++) {
	    $append_string .= ";;";
	  }
	                                                                                                    
	  print OUTFILE "# ";
	  foreach my $key (@existing_testsuites_list) {
	    if ($key eq "") {
	      next;
	    }
	    print OUTFILE "$key ";
	  }
	
	  print OUTFILE "\n";
	  for(my $line=1; $line<=$#lines;$line++){
	    chomp ($lines[$line]);
	    print OUTFILE "$lines[$line]$append_string\n";
	  }
	
	  foreach my $date ( sort @$dates) {
	    print OUTFILE "$date;";
	    foreach my $key (@existing_testsuites_list) {
	      if ($key eq "") {
	        next;
	      }
	      if (defined ($hash->{$key}{$date}{"pass"})) {
	        print OUTFILE $hash->{$key}{$date}{"pass"}.";";	
	      } else {
	        print OUTFILE ";";
	      } 
	      if (defined ($hash->{$key}{$date}{"fail"})) {
	        print OUTFILE $hash->{$key}{$date}{"fail"}.";";
	      } else {
	        print OUTFILE ";";
	      } 
	    }
	    print OUTFILE "\n";
	  }
      close OUTFILE;

   }
 
  if ( $flag == 0 )
  {
  	 my $file_exists = 0;
	   if ( -e $output_file) {
	        $file_exists = 1;
	   }
	                                                                                                               
	   open(OUTPUT, ">>$output_file") || die ("Cannot open file for reading");
	   if (!$file_exists) {
	        print OUTPUT "# Passes Fail Pass% Fail%\n";
	   }
	                                                                                                               
	   foreach my $date (sort keys %$hash) {
	     print OUTPUT "$date;";
	     print OUTPUT $hash->{$date}{"pass"} .";";
	     print OUTPUT $hash->{$date}{"fail"} .";";
	     print OUTPUT $hash->{$date}{"pass_perc"} .";";
	     print OUTPUT $hash->{$date}{"fail_perc"} .";";
	     print OUTPUT "\n";
	   }
	   close(OUTPUT);
   }
}   

sub generate_charts {
  my ($filename, $root_dir, $type) = (@_);
  open (INFILE, "<$filename") || die("Cannot open file :$filename for reading");
  my $line = "";
  my @fields = ();
  print "$root_dir";
  if (defined ($line = <INFILE>)) {
    if (substr($line,0,1) != '#') {
      print "Invalid file format\n";
      close(INFILE);
      return;
    } else {
      @fields = split(/\s/, substr($line,1));
    }
  }
  close(INFILE);

  if ($type eq "individual") {
    for (my $i = 1; $i<=$#fields; $i++) {
       my $outfile = "$root_dir/$fields[$i]_pass.png";
       my $title = "Progress Charts for $fields[$i]";
       my $ylabel = "Number Of Passes";
       my $plot_cmd = "plot \"$filename\" using 1:2*$i title \"$title\"  with linespoints lt 2 lw 1 pt 5 ps 1;";
       plot_graph($outfile, $title, $ylabel, $plot_cmd);
       $ylabel = "Number Of Failures";
       $outfile = "$root_dir/$fields[$i]_fail.png";
       $plot_cmd = "plot \"$filename\" using 1:2*$i+1 title \"$title\"  with linespoints lt 1 lw 1 pt 5 ps 1;";
       plot_graph($outfile, $title, $ylabel, $plot_cmd);
    }
  } elsif ($type eq "consolidated") {
    for (my $i = 1; $i<=$#fields; $i++) {
       my $outfile = "$root_dir/$fields[$i]_percent.png";
       my $title = "Progress Charts for $fields[$i]";
       my $ylabel = "Percentage (%)";
       my $plot_cmd = "plot \"$filename\" using 1:2*$i title \"$title - Pass %\"  with linespoints lt 2 lw 1 pt 5 ps 1, \"$filename\" using 1:2*$i+1 title \"$title - Fail %\"  with linespoints lt 1 lw 1 pt 5 ps 1;";
       plot_graph($outfile, $title, $ylabel, $plot_cmd);
    }
  } elsif ($type eq "total") {
    my $outfile = "";
    my $title = "";
    my $ylabel = "";
    my $linetype = "";
    for (my $i = 2; $i <= 3; $i++) {
       if ($i == 2) {
       	 $outfile = "$root_dir/Total_pass.png";
	 $title = "Total number of Passes";
	 $ylabel = "Passes";
	 $linetype = 2;
       } else {
       	 $outfile = "$root_dir/Total_fail.png";
	 $title = "Total number of Failures";
	 $ylabel = "Failures";
	 $linetype = 1;
       }

       my $plot_cmd = "plot \"$filename\" using 1:$i title \"$title\"  with linespoints lt $linetype lw 1 pt 5 ps 1;";

       plot_graph($outfile, $title, $ylabel, $plot_cmd);
    }

    $outfile = "$root_dir/Total_percent.png";
    $title = "Total";
    $ylabel = "Percentage (%)";
    $linetype = 1;
    my $plot_cmd = "plot \"$filename\" using 1:4 title \"$title - Pass %\"  with linespoints lt 2 lw 1 pt 5 ps 1, \"$filename\" using 1:5 title \"$title - Fail %\"  with linespoints lt 1 lw 1 pt 5 ps 1;";
    plot_graph($outfile, $title, $ylabel, $plot_cmd);
  }
  close INFILE;
}

sub plot_graph {
  my ($output_file, $title, $ylabel, $plot_cmd) = (@_);
  
  my $GNUPlot = '/usr/local/bin/gnuplot';
  open ( GNUPLOT, "|$GNUPlot");

  my $cmds = "";
  #print "$plot_cmd\n";

$cmds =<< "gnuplot_Commands";
set terminal png;
set output "$output_file";
set time;
set title "$title";
set datafile separator ";"
set xlabel "Dates" 7,-3;
set ylabel "$ylabel"
set xdata time;
set timefmt "%Y%m%d";
set format x "%Y%m%d";
set key box lw 0.5;
set style line;
set size ratio .50;
set autoscale;
set size ratio 0.55;
$plot_cmd
gnuplot_Commands

print $cmds."\n";
print GNUPLOT $cmds;
close(GNUPLOT);

}
