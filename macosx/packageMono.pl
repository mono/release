#!/usr/bin/perl -w

use strict;

# Parse command line options
use Getopt::Std;

my $hdiutil = "/usr/bin/hdiutil";
my $infoString = "0.97";
my $versionString = "RC1";
my $cp = "/bin/cp -R";
my $packageMaker="/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker";
my $workDir = "/usr/local/mono.build";

if (! -d $workDir) {
    mkdir($workDir);
}

my $monoBuild = "./buildMono.sh";
my $packageResources="$workDir/MonoFramework";

#set the default size for the image.  Get a better one later.
my $dmgSize = "30000k";

my $createImage = "$hdiutil create -ov -size $dmgSize -type SPARSE -fs HFS+ -quiet -volname";
my $mountImage = "$hdiutil mount -quiet";
my $unmountImage = "$hdiutil unmount -quiet";
my $convertImage = "$hdiutil convert -ov MonoFramework-$infoString.sparseimage -quiet -format UDRO -o";

my $packageName = "$workDir/MonoFramework-$infoString.pkg";
my $dmgName = "$workDir/MonoFramework-$infoString.dmg";
my %commandLineSwitches;
my $getoptsSucceeded = getopts( 'v', \%commandLineSwitches );
my $verbose = exists( $commandLineSwitches{v} );

if(! -d $workDir) {
	mkdir($workDir)
}

getMono();
createInfoPlist();
createPackage();
createDmg();

sub createDmg
{
    print("Creating dmg for package\n") if ( $verbose );
    print("$createImage MonoFramework-$infoString MonoFramework-$infoString.sparseimage\n") if ( $verbose );
    system("$createImage MonoFramework-$infoString MonoFramework-$infoString.sparseimage");
    print("$mountImage MonoFramework-$infoString.sparseimage\n") if ( $verbose );
    system("$mountImage MonoFramework-$infoString.sparseimage");
    print("$cp $packageName /Volumes/MonoFramework-$infoString/\n") if ( $verbose );
    system("$cp $packageName /Volumes/MonoFramework-$infoString/");
    print("$unmountImage /Volumes/MonoFramework-$infoString\n") if ( $verbose );
    system("$unmountImage /Volumes/MonoFramework-$infoString\n");
    print("$convertImage $workDir/MonoFramework-$infoString.dmg\n") if ( $verbose );
    system("$convertImage $workDir/MonoFramework-$infoString\n");
    unlink("$workDir/MonoFramework-$infoString.sparseimage");
}

sub getMono
{
    print("Building Mono and Deps\n") if ( $verbose );
    print ("$monoBuild $workDir $infoString\n")  if ( $verbose );
    system("$monoBuild $workDir $infoString");
}

sub createPackage
{
    print("Creating Package\n") if ( $verbose );
    print("$packageMaker -build -p $packageName -f $workDir/PKGROOT -r $workDir/Resources -i $workDir/Info.plist\n") if ( $verbose );
    system("$packageMaker -build -p $packageName -f $workDir/PKGROOT -r $workDir/Resources -i $workDir/Info.plist -d ./Description.plist\n");
    my @dmgOutput = split(/\t/, `du -sk $workDir/MonoFramework-$infoString.pkg`);
    #give dmg size a bump so that everything fits with formatting.
    $dmgOutput[0] += 1000;
    $dmgSize = $dmgOutput[0]."k";
    print("dmg will be $dmgSize\n") if ( $verbose );
}

sub createInfoPlist 
{
    print("Creating Info.plist\n") if ( $verbose );
    open (INFO, ">$workDir/Info.plist");
    print INFO <<EOF;
	<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	<plist version="1.0">
		<dict>
		<key>CFBundleGetInfoString</key>
		<string>$infoString</string>
		<key>CFBundleIdentifier</key>
		<string>com.xiaman.mono</string>
		<key>CFBundleName</key>
		<string>Mono.framework</string>
		<key>CFBundleShortVersionString</key>
		<string>$versionString</string>
		<key>IFMajorVersion</key>
		<integer>0</integer>
		<key>IFMinorVersion</key>
		<integer>0</integer>
		<key>IFPkgFlagAllowBackRev</key>
		<false/>
		<key>IFPkgFlagAuthorizationAction</key>
		<string>AdminAuthorization</string>
		<key>IFPkgFlagDefaultLocation</key>
		<string>/</string>
		<key>IFPkgFlagInstallFat</key>
		<false/>
		<key>IFPkgFlagIsRequired</key>
		<false/>
		<key>IFPkgFlagRelocatable</key>
		<false/>
		<key>IFPkgFlagRestartAction</key>
		<string>NoRestart</string>
		<key>IFPkgFlagRootVolumeOnly</key>
		<true/>
		<key>IFPkgFlagUpdateInstalledLanguages</key>
		<false/>
		<key>IFPkgFormatVersion</key>
		<real>0.10000000149011612</real>
		</dict>
	</plist>
EOF
#close(INFO);
}
