#!/usr/bin/perl

use FindBin;
use lib "$FindBin::RealBin";

use Mono::Build;

my $platform = "rhel-3-i386";
my $package = "gtk-sharp";

#my $latest_rev = 44840;
my $latest_rev = Mono::Build::getLatestTreeRevision();

Mono::Build::scheduleBuild($platform, $package, $latest_rev);


