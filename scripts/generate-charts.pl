#!/usr/bin/perl
use XML::DOM;
use POSIX;
use Switch;

$max = 10;
$root_dir = "./";
$dir = $root_dir."testresults/xml/";

$chart_dir = $root_dir."testresults/charts/";

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
	
#	system("mkdir ".$chart_dir.$testsuite_key);

	open (FILE,">temp.dat");
	open (FILE1,">temp1.dat");
	open (FILE2,">temp2.dat");
	@date_keys = keys(%{$percent{$testsuite_key}});
	@date_keys = sort(@date_keys);
	$max_pass = 0;
	$max_fail = 0;
	foreach $date_key(@date_keys) {
		print FILE $date_key . "\t".$percent{$testsuite_key}{$date_key}{0}."\t".$percent{$testsuite_key}{$date_key}{1}."\n";
		print FILE1 $date_key . "\t".$percent{$testsuite_key}{$date_key}{2}."\n";
		print FILE2 $date_key . "\t".$percent{$testsuite_key}{$date_key}{3}."\n";
		if ($max_pass < $percent{$testsuite_key}{$date_key}{2}){
			$max_pass =  $percent{$testsuite_key}{$date_key}{2};
		}
		if ($max_fail < $percent{$testsuite_key}{$date_key}{3}) {
                        $max_fail =  $percent{$testsuite_key}{$date_key}{3};
		}
	}
	close (FILE);
	close (FILE1);
	close (FILE2);

	$first_date = $date_keys[0];
	$last_date = $date_keys[scalar(@date_keys)-1];
	print $max_pass . "\t" . $max_fail."\n";
#	$output_file = $chart_dir.$testsuite_key ."/".$current_date. ".png";
#	$output_file = $chart_dir.$testsuite_key . ".png";

#	plot_current_data ($output_file,$testsuite_key,$first_date,$last_date,$plot_file,$type,$max);
	plot_current_data ($chart_dir.$testsuite_key . "_percent.png",$testsuite_key,$first_date,$last_date,0,120); # percent chart
	plot_current_data ($chart_dir.$testsuite_key . "_pass.png",$testsuite_key,$first_date,$last_date,1,$max_pass); # pass number chart
	plot_current_data ($chart_dir.$testsuite_key . "_fail.png",$testsuite_key,$first_date,$last_date,2,$max_fail); # fail number chart

}
unlink("temp.dat");

sub plot_current_data
{
	print "\nPlotting to file ".$_[0]."...\n";
	my $output_file = $_[0];
	my $testsuite_name = $_[1];
	my $first_date = $_[2];
	my $last_date = $_[3];
	my $type = $_[4];
	my $max = $_[5];
	switch ($type) {
		case 0 {
			$title = "Progress Chart(%) For $testsuite_name";
			$ylabel = "Percentage %";
			$yrange = "set yrange [0:120]";
			$plot = "\"temp.dat\" using 1:2 title 'Pass Percent' with linespoints lt 2 lw 1 pt 1 ps 2, \"temp.dat\" using 1:3 title 'Fail Percent' with linespoints lt 1 lw 1 pt 1 ps 2";
		}
		case 1 {
			$title = "Progress Chart For $testsuite_name";
                        $ylabel = "Number of passes";
			$yrange = "";
                        $plot = "\"temp1.dat\" using 1:2 title 'Number of passes' with linespoints lt 2 lw 1 pt 1 ps 2";
		}
		case 2	{
			$title = "Progress Chart For $testsuite_name";
                        $ylabel = "Number of failures";
			$yrange = "";
                        $plot = "\"temp2.dat\" using 1:2 title 'Number of failures' with linespoints lt 1 lw 1 pt 1 ps 2";
		}
	}
	my $GNUPlot = '/usr/bin/gnuplot';
        open ( GNUPLOT, "|$GNUPlot");

print GNUPLOT << "gnuplot_Commands";
set terminal png;
set output "$output_file";
set time;
set title "$title";
set xlabel "Dates" 7,-3;
set ylabel "$ylabel" -2,5;
set xdata time;
$yrange;
set timefmt "%Y-%m-%d";
set format x "%Y-%m-%d";
set key box lw 0.5;
set xtics rotate;
set nomxtics;
set xtics "$first_date",86400,"$last_date";
plot $plot;
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
		$percent{$testsuite->getAttribute("name")}{$date}{"2"} = $testsuite->getAttribute("pass");
                $percent{$testsuite->getAttribute("name")}{$date}{"3"} = $testsuite->getAttribute("fail");
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
