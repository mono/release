#!/usr/bin/perl


use FindBin;
use lib "$FindBin::RealBin/..";

use Mono::Build;

my $platform = 'suse-93-i586';
my $package = 'gecko-sharp-2.0';
my $rev = 'r4543';

my $state = Mono::Build::getState($platform, $package, $rev);

print "State: $state\n";

