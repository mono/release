#!/usr/bin/tclsh

# Can this somehow get set from an environment variable?
set version 1.1.7


set prefix [file normalize [file dirname [info script]]]

array set ::opts \
    [list buildroot $prefix/build \
    tarballs $prefix/thirdparty/tarballs]

file mkdir $opts(buildroot)
file delete -force $opts(buildroot)/usr $opts(buildroot)/etc


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

proc extract {file} {
    exec rpm2cpio $file > kk
    catch {exec cpio --extract --make-directories < kk} kk
    puts $kk
}

proc extractRPMs {base rpmList} {
    foreach f $rpmList {
	foreach file [glob $base/${f}*] {
	    puts "Extracting $file"
	    extract $file
	}
    }
}


cd $opts(buildroot)

foreach {base rpmList} \
    [list $opts(tarballs)/www.go-mono.com/archive/1.0.5/redhat-9-i386/ {
	libgtkhtml gtksourceview-1
    } $opts(tarballs)/www.go-mono.com/archive/1.0.6/redhat-9-i386/ {
	gtksourceview cairo gecko libpixman
    } $opts(tarballs)/www.go-mono.com/archive/$version/redhat-9-i386/ {
	mono-core mono-devel mono-locale mono-web mono-data bytefx ibm-data
	mono-basic mono-ikvm mono-winforms mono-extras libgdiplus mono-jscript
	gtk-sharp xsp mod_mono monodoc
    } $opts(tarballs)/www.go-mono.com/archive/$version/suse-93-i586 {
	gtk-sharp2
    } $opts(tarballs)/ftp.ximian.com/pub/mono/redhat-9-i386/ {
	libicu libstdc linc libgal pkgconfig
    }] {	 
	extractRPMs $base $rpmList		  
	
    }

# http://ftp.ximian.com/pub/mono/redhat-9-i386/libicu26-2.6.2-1.ximian.6.0.i386.rpm
# ftp://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/libstdc++-3.2.2-5.i386.rpm
# ftp://fr2.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/linc-1.0.1-1.i386.rpm
# ftp://fr.rpmfind.net/linux/redhat/9/en/os/i386/RedHat/RPMS/pkgconfig-0.14.0-3.i386.rpm
# ftp://ftp.ximian.com/pub/ximian-evolution/redhat-9-i386/libgal2.0_6-1.99.11-0.ximian.6.1.i386.rpm

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
set lista {
    monodoc mod webshot mcs asp-state dbsessmgr mod-mono-server xsp
    resgen makecert mbas monodocer monodocs2html monodocs2slashdoc
    gconfsharp2-schemagen gapi-codegen gapi2-codegen gapi2-fixup gapi2-parser
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
file copy -force $p/../projects/mono/Readme-$version.txt $p/usr/share/doc/Readme.txt

file mkdir $p/html
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

puts [exec ~/installbuilder-2.4.1/bin/builder build $p/mono.xml]

