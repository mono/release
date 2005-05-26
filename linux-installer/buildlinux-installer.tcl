#!/usr/bin/tclsh


# Some history on this script...
################################
# Daniel Lopez used this script to create installers for Mono
#
# I then revamped some of it so it would dynamically get the latest packages that were built locally
# 
# It may be easier to convert it to bash or perl later if the tcl is a pain to maintain
# 


# This script will build with the latest rpms, but it needs the release version of mono
set version [ lindex $argv 0]

if { $version == "" } then {
	puts "Usage: buildlinux-installer.tcl <mono release version>"
	puts "  example: buildlinux-installer.tcl 1.1.7-1"
	exit 1
}

puts "Version: $version"

# Install the installer if it's not installed...
if { ![file exists ~/installbuilder-2.4.1/bin/builder] } {

	set installer installbuilder-multiplatform-2.4.1-linux-installer.bin

	# Download it if it doesn't exist
	if { ![file exists installbuilder-multiplatform-2.4.1-linux-installer.bin ] } {
		puts "Downloading the Bitrock installer..."
		catch {exec wget http://164.99.120.153/linux-installer/bitrock/$installer } results
		puts $results
	}

	# Script will die here if the file can't be found...
	file attributes $installer -permission 0755

	puts "Installing the Bitrock installer..."
	exec ./$installer --mode unattended 
}

# Get the current working directory, the tcl way :)
set prefix [file normalize [file dirname [info script]]]

array set ::opts \
    [list buildroot $prefix/build \
    external_rpms $prefix/thirdparty/external_rpms \
    mono_rpms $prefix/../packaging/packages]

# Some clean up
file mkdir $opts(buildroot)
file delete -force $opts(buildroot)/usr $opts(buildroot)/etc

file delete -force $prefix/output/packages_used.txt
set packages_used_text "RPMS used to create this build:\n"

namespace eval maui::util {
    proc substituteParametersInFile {filename substitutionParams} {
        set text [maui::file::read $filename]
        maui::file::write $filename [substituteParameters $text $substitutionParams]
    }

    proc substituteParameters {text substitutionParams} {
        return [string map $substitutionParams $text]
        set result {}
        foreach line [split $text \n] {
            foreach {name value} $substitutionParams {
                regsub -all $name $line $value line
            }
            lappend result $line
        }
	return [join $result \n]
    }
}

namespace eval ::maui::file {

    proc write {dest text} {
        set f [open $dest w]
        puts -nonewline $f $text
        close $f
    }

    proc read {dest} {
        set f [open $dest r]
        set r [::read $f]
        close $f
        return $r
    }
}

# Takes a full path to an rpm, and will extract it into the buildroot
proc extract {file} {

    global prefix
    global opts
    global packages_used_text

    set cwd [exec pwd]
    cd $opts(buildroot)
    
    puts "Extracting $file"
    exec echo "$file" >> $prefix/output/packages_used.txt
    append packages_used_text [file tail $file ] "\n"
    exec rpm2cpio $file > kk
    catch {exec cpio --extract --make-directories < kk} kk
    file delete -force kk

    # Print out results
    puts $kk

    cd $cwd

}

proc extractRPMs {base rpmList} {

    foreach f $rpmList {

	# ls has version sorting (-v), use that to get the latest version from the directory
	set latest_version [ exec ls -vr $base | head -n1 ]

	foreach file [glob $base/$latest_version/${f}*] {
	    extract $file
	}
    }
}



# http://ftp.ximian.com/pub/mono/redhat-9-i386/libicu26-2.6.2-1.ximian.6.0.i386.rpm
# ftp://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/libstdc++-3.2.2-5.i386.rpm
# ftp://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/linc-1.0.1-1.i386.rpm
# ftp://fr.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/pkgconfig-0.14.0-3.i386.rpm
# ftp://ftp.ximian.com/pub/ximian-evolution/redhat-9-i386/libgal2.0_6-1.99.11-0.ximian.6.1.i386.rpm


# some stock os rpms
set external_rpms_list {
	http://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/libstdc++-3.2.2-5.i386.rpm
	http://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/linc-1.0.1-1.i386.rpm
	http://fr.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/pkgconfig-0.14.0-3.i386.rpm
}

# Stuff from older releases
set custom_rpms_list {
	http://www.go-mono.com/archive/1.0.5/redhat-9-i386/libgtkhtml3.0_4-3.0.10-0.ximian.6.1.i386.rpm
	http://www.go-mono.com/archive/1.0.6/redhat-9-i386/gtksourceview-sharp-0.5-1.ximian.6.1.i386.rpm
	http://www.go-mono.com/archive/1.0.5/redhat-9-i386/gtksourceview-1.0.1-0.ximian.6.1.i386.rpm
	http://www.go-mono.com/archive/1.0.6/redhat-9-i386/gecko-sharp-0.6-1.ximian.6.1.i386.rpm
	ftp://ftp.ximian.com/pub/ximian-evolution/redhat-9-i386/libgal2.0_6-1.99.11-0.ximian.6.1.i386.rpm
}


# Download the sotck and custom rpms if they don't exist already and then extract them
cd $opts(external_rpms)
foreach rpm [ concat $external_rpms_list $custom_rpms_list ] {

	if { ![file exists [file tail $rpm]] } {
		puts "Downloading: $rpm";
		catch { exec wget $rpm }

		# If it still doesn't exists, die
		if { ![file exists [file tail $rpm]] } {
			puts "Failed to download: $rpm"
			exit 1
		}

	} else {
		#puts "File already exists!"
	}
	
	# Get a full path to the rpm in the cwd based on the url name
	set full_path_to_rpm [file normalize [file tail $rpm]]

	extract $full_path_to_rpm
}


# Get a list of rpms that we want in this install from the local builds
#  The first option is a directory of where to look for the rpms
#    It will pick a subdirectory with the best latest version
#    and then glob the files beginning with the second arg (list)


foreach {base rpmList} \
    [list $opts(mono_rpms)/x86/mono-1.1/ {
	mono-extras mono-jscript mono-ikvm mono-core
	mono-devel mono-winforms
	bytefx-data-mysql mono-basic
	mono-locale-extras mono-data
	mono-complete ibm-data-db2 mono-web
    } $opts(mono_rpms)/redhat-9-i386/mod_mono {
	mod_mono
    } $opts(mono_rpms)/redhat-9-i386/gtk-sharp {
	gtk-sharp
    } $opts(mono_rpms)/redhat-9-i386/libgdiplus-1.1 {
	libgdiplus
    } $opts(mono_rpms)/noarch/boo {
	boo
    } $opts(mono_rpms)/noarch/xsp {
	xsp
    } $opts(mono_rpms)/noarch/ikvm {
	ikvm
    } $opts(mono_rpms)/noarch/monodoc {
	monodoc
    } $opts(mono_rpms)/noarch/monodevelop/ {
	monodevelop
    } $opts(mono_rpms)/noarch/gecko-sharp-2.0/ {
	gecko-sharp-2.0
    } $opts(mono_rpms)/noarch/gtksourceview-sharp-2.0/ {
	gtksourceview-sharp-2.0
    } $opts(mono_rpms)/suse-93-i586/gtk-sharp-2.0/ {
	gtk-sharp2
    }] {
	extractRPMs $base $rpmList		  
    }


proc recurseDirectories {path} {
    file attributes $path -permissions 0755
    foreach f [glob -nocomplain -types d -- $path/*] {
	recurseDirectories $f
    }
}


set p [file normalize $opts(buildroot)]

# Susbtitute binary with template that sets up environment
file rename -force $opts(buildroot)/usr/bin/mono $opts(buildroot)/usr/bin/mono.bin
file copy -force $p/../mono.template $opts(buildroot)/usr/bin/mono

# Set of symbolic links
foreach d [list 1.0 2.0 gtk-sharp gecko-sharp] {
    if {![file exists [file join $p usr lib mono $d]]} {
	puts "Skipping $d"
	continue
    }
    cd [file join $p usr lib mono $d]

    foreach f [glob *.dll] {
	if {[file type $f] != "link"} {
	    puts "skipping $f"
	    continue
	}
	set target [file readlink $f]
	set target ../[string range $target [string first gac $target] end]
	file delete $f
	puts "$f $target"
	#file link $f $target                                                                                                                                                                                 
	exec ln -s $target $f
    }
}

cd $p
file delete -force usr/etc
file rename etc usr/etc

# Disable monodevelop for now
# monodevelop
# Why?
set lista {
    monodoc mod webshot mcs asp-state dbsessmgr mod-mono-server xsp
    resgen makecert mbas monodocer monodocs2html monodocs2slashdoc
    gconfsharp2-schemagen gapi-codegen gapi2-codegen gapi2-fixup gapi2-parser
    monodevelop
}

foreach f [glob $p/usr/lib/pkgconfig/*.pc] {
    maui::util::substituteParametersInFile $f \
	[list /usr @@BITROCK_MONO_ROOTDIR@@]
    puts "Substituting $f"
}
foreach f [concat [glob -nocomplain $p/usr/bin/*.exe] [glob -nocomplain $p/usr/lib/mono/*/*.exe]]  {
    set f [file root [file tail $f]]
    if {[file exists $p/usr/bin/$f]} {
	if {[lsearch -exact $lista $f] == -1} {
	    lappend lista $f
	}
    }
}

foreach f $lista {  
    if {[file exists $p/usr/bin/$f]} {
	maui::util::substituteParametersInFile $p/usr/bin/$f \
	    [list /usr @@BITROCK_MONO_ROOTDIR@@ \
		 {exec mono} {exec @@BITROCK_MONO_ROOTDIR@@/bin/mono} \
		 {mono --debug mod.exe} {exec @@BITROCK_MONO_ROOTDIR@@/bin/mono --debug mod.exe}] 
	puts "Substituting $f"
    } else {
	puts "***Not found $f***"
    }
}

maui::util::substituteParametersInFile $p/usr/bin/gacutil \
    [list gacutil.exe "gacutil.exe -gacdir @@BITROCK_MONO_ROOTDIR@@"]


maui::util::substituteParametersInFile $p/usr/lib/mono/gac/monodoc/1.0.0.0__0738eb9f132ed756/monodoc.dll.config \
    [list /usr @@BITROCK_MONO_ROOTDIR@@]


#maui::util::substituteParametersInFile $p/usr/lib/mono/gac/gtkhtml-sharp/1.0.0.0__35e10195dab3c99f/gtkhtml-sharp.dll.config [list .4 .2]
#maui::file::write $p/usr/bin/setenv.sh "export PATH=\$PATH:$p/bin/ export LD_LIBRARY_PATH=$p/lib:$p/lib/monodoc"

file copy -force $p/../projects/mono.xml $p
maui::util::substituteParametersInFile $p/mono.xml [list @@VERSION@@ $version]

file copy -force $p/../projects/mono/readme.gif $p/usr/share/pixmaps
file copy -force $p/../projects/mono/monourl.gif $p/usr/share/pixmaps
file copy -force $p/../projects/mono/monotm48x48.png $p/usr/share/pixmaps
file copy -force $p/../projects/mono/License.txt $p/usr/share/doc
# Need to figure out another way to get this version specific file...
#file copy -force $p/../projects/mono/Readme-1.1.7.txt $p/usr/share/doc/Readme.txt
# Get the readme for this version if it's there, otherwise don't worry about it
if { [ catch { exec wget http://go-mono.com/archive/$version -o $p/usr/share/doc/Readme.txt } ] } {
	# If there was an error, zero out the Readme file
	maui::file::write $p/usr/share/doc/Readme.txt "No release notes for this build..."
	maui::file::write $p/usr/share/doc/Readme.txt $packages_used_text

}

file mkdir $p/html
# TODO: Here's another file that changes with each release... need to update it manually for now
file copy -force $p/../projects/mono/html/index.html $p/html
file copy -force $p/../projects/mono/html/mono.css $p/html
file copy -force $p/../projects/mono/html/bitrock.png $p/html

# Build automatically mono.xml
set result {}
lappend lista mono
foreach l $lista {
    append result */bin/${l}\;
}
set result [string trimright $result {;}]
append result {;*/monodoc.dll.config;*/*.pc}

maui::util::substituteParametersInFile $p/mono.xml \
    [list @@SUBST_FILES@@ $result]

# Fix RPM directory permissions
recurseDirectories $p/usr/

# Do some safe cleanup
file delete ~/installbuilder-2.4.1/output/mono-$version-installer.bin
file delete $prefix/output/mono-$version-installer.bin

# Run the install
puts [exec ~/installbuilder-2.4.1/bin/builder build $p/mono.xml]

# Move file to the current directory
file rename ~/installbuilder-2.4.1/output/mono-$version-installer.bin $prefix/output


