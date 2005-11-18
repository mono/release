#!/usr/bin/perl

## Script to generate html page with latest rpm packages

$max_days = 4;
$root_dir = "./";
$package_dir = $root_dir."packages/";
#When adding more distros add them to this list. Also add the appropriate header and index filename to the 'headers' and 'index' lists 
@distros = ( [ "redhat-9-i386", "Red Hat Linux 9", "rhindex.html" ],
	     [ "fedora-1-i386", "Fedora Core 1/x86", "fedindex.html" ],
	     [ "suse-90-i586", "SUSE 9/x86", "susindex.html" ]
            );

#Generating a html page for each distro 
for (@distros) {
	@datedirs = ();

	my ($distro, $title, $index) = @$_;
	my $dir = $package_dir.$distro."/";

	open(FILE,">$dir$index");
	print "\nWriting to file:$dir$index";
	#Writing the header information to the html file
	print FILE "<html>\n<head>\n<title>Mono Daily Packages for $title</title>\n";
	print FILE "<link rel=\"stylesheet\" href=\"http://www.go-mono.com/monologue/monologue.css\" type=\"text/css\" />";
	print FILE "<style type=\"text/css\">p {margin-left: 2em; }</style>\n</head>";
	print FILE "\n<body>\n<h1>Mono Packages for $title</h1>";

	#Obtaining the $max_days recent filenames
	@datedirs = get_recent_files($dir,$max_days);

	print "\n_______ ".$distro." ________\n";

	#displaying the lists of rpm's for $max_days recent days
	display_contents($dir);

	print FILE "\n</body></html>";
	close(FILE);
}

# Returns the $max recent files/directories from the $dir directory 
# and deletes the rest of the files/directories
sub get_recent_files
{
	my $dir = $_[0];
	my $max = $_[1];

	opendir($dir_handle,$dir);
	my @files = ();
	@files = readdir($dir_handle);
        my @sorted_files = ();
	my $cnt = 0;
	foreach $file(@files) {
		if($file ne "." && $file ne ".." && substr($file,-4,4) ne "html" ) {
			print "\n*$file\n";
			$sorted_files[$cnt] = $file;
			$cnt++;
		}
	}

	@sorted_files = sort(@sorted_files);
	@sorted_files = reverse(@sorted_files);

	#Deleting old directories and keeping only $max_days entries
	
	close($dir_handle);
	my @retval = splice @sorted_files, 0, $max;
	foreach $deleted_file (@sorted_files) {
		print "\nDeleting $dir$deleted_file ...";
		system ("rm -rf $dir$deleted_file");
	}
	return @retval;
}

sub display_contents
{
	my $dir = $_[0];
        print scalar(@datedirs);     
	foreach $datedir(@datedirs) {
		#formatting date to "yyyy mm dd"
		$date = substr($datedir,0,4) ." ". substr($datedir,4,2) ." ". substr ($datedir,6);

		print FILE "\n<h3>$date </h3>\n<blockquote>";
		opendir($dir_handle,$dir.$datedir);
		my @files = ();
		@files = readdir($dir_handle);	
		#Displaying list of rpm's for each date
		foreach $file(@files) {
			if($file ne "." && $file ne "..") {
				print "\n\t".$file;
				print FILE "\n<a href=$datedir/$file>$file</a><br>";
			}
		}
		print FILE "\n</blockquote>";
	}
}
