#!/usr/bin/perl
use XML::DOM;
use POSIX;

$max = 10;
$root_dir = "./";
$dir = $root_dir."TestResults/Xml/";

$chart_dir = $root_dir."TestResults/Charts/";

system("mkdir ". $chart_dir);

@files = get_sorted_filenames ($dir); 
$percent_count = 1;
foreach $file(@files) {
	print "\nProcessing file ".$file."...\n";
	get_percent_values($file);
	if($percent_count >= $max) {
	    last ;
	}
	$percent_count++;
}
@testsuite_names = keys(%testsuites_status);

$current_date = `date +'%Y%m%d'`;
chomp $current_date;

@testsuite_keys = keys(%percent);
foreach $testsuite_key(@testsuite_keys) {
	
	system("mkdir ".$chart_dir.$testsuite_key);

	open (FILE,">temp.dat");
	@date_keys = keys(%{$percent{$testsuite_key}});
	@date_keys = sort(@date_keys);
	foreach $date_key(@date_keys) {
		print FILE $date_key . "\t".$percent{$testsuite_key}{$date_key}{0}."\t".$percent{$testsuite_key}{$date_key}{1}."\n";
	}
	close (FILE);
	$first_date = $date_keys[0];
	$last_date = $date_keys[scalar(@date_keys)-1];
	$output_file = $chart_dir.$testsuite_key ."/".$current_date. ".png";
	plot_current_data ($output_file,$testsuite_key,$first_date,$last_date);

}
unlink("temp.dat");

sub plot_current_data
{
	print "\nPlotting to file ".$_[0]."...\n";
	my $output_file = $_[0];
	my $testsuite_name = $_[1];
	my $first_date = $_[2];
	my $last_date = $_[3];
	my $GNUPlot = '/usr/bin/gnuplot';
        open ( GNUPLOT, "|$GNUPlot");

print GNUPLOT << "gnuplot_Commands";
set terminal png;
set output "$output_file";
set time;
set title "Progess Chart For $testsuite_name";
set xlabel "Dates" 7,-3;
set ylabel "Percentage %" -2,5;
set xdata time;
set yrange [0:120];
set timefmt "%Y-%m-%d";
set format x "%Y-%m-%d";
set key box lw 0.5;
set xtics rotate;
set nomxtics;
set xtics "$first_date",86400,"$last_date";
plot "temp.dat" using 1:2 title 'Pass Percent' with linespoints lt 2 lw 1 pt 1 ps 2, "temp.dat" using 1:3 title 'Fail Percent' with linespoints lt 1 lw 1 pt 1 ps 2;
gnuplot_Commands
    close(GNUPLOT);
}

sub get_percent_values 
{
	my $file = $_[0];
	my $parser = new XML::DOM::Parser;
	my $doc = $parser->parsefile ($file);
	my @testsuites = $doc->getElementsByTagName("testsuite");
	$date = get_date_from_filename($file);
	foreach $testsuite(@testsuites) {
		if ($testsuites_status{$testsuite->getAttribute("name")} != 1) {
			$testsuites_status{$testsuite->getAttribute("name")} = 1;
		}
		$total_tests = $testsuite->getAttribute("pass") + $testsuite->getAttribute("fail");
		if ($total_tests == 0) {
		    next;
		}
		else {
			$pass_percent_value = ceil(($testsuite->getAttribute("pass")*100)/$total_tests);
			$fail_percent_value = floor(($testsuite->getAttribute("fail")*100)/$total_tests);
			
		}
		$percent{$testsuite->getAttribute("name")}{$date}{"0"} = $pass_percent_value;
		$percent{$testsuite->getAttribute("name")}{$date}{"1"} = $fail_percent_value;
		
	}
}
sub get_sorted_filenames
{
	opendir($dir_handle,$_[0]);
	my $files_count = 0;
	my @files =  readdir($dir_handle);
	my @sorted_files = ();
	my $file_count = 0;

	foreach $file(@files) {
		if((substr($file,0,12) eq "testresults-") && (substr($file,-3,3) eq "xml")) {
			$sorted_files[$file_count] = $dir . $file;
			$file_count++;
		}
	}
 	 
	@sorted_files = sort(@sorted_files);
	@sorted_files = reverse @sorted_files;
	return @sorted_files;
}
sub get_date_from_filename
{
	my $date = $_[0];
	$strip_str = $dir."testresults-";
	$date =~ s/$strip_str//i;	
	$date =~ s/.xml//i;

	$date = substr($date,0,4) ."-". substr($date,4,2) ."-". substr ($date,6);
	return $date;
}
