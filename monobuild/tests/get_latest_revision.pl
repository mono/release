#!/usr/bin/perl


use FindBin;
use lib "$FindBin::RealBin/..";

use Mono::Build;

my $platform = 'suse-93-i586';
my $package = 'gecko-sharp-2.0';

my $revision = Mono::Build::getLatestRevision($platform, $package);

print "Revision: $revision\n";

