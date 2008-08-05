use SaX;

open(FH, "/etc/langset.xkb");
my $XKBLayout=<FH>;
close(FH);
chomp $XKBLayout;

$exc = new SaX::SaXException;
$exc -> setDebug (1);

$init = new SaX::SaXInit;
if ( $init -> needInit() ) {
    print ("initialize cache...\n");
    $init -> doInit();
}
$status = $init -> errorString();

$config  = new SaX::SaXConfig;
$kbd     = new SaX::SaXImport ( $SaX::SAX_KEYBOARD );
$kbd -> setSource( $SaX::SAX_SYSTEM_CONFIG );
$kbd -> doImport();
$config->addImport($kbd);

$manip2 = new SaX::SaXManipulateKeyboard ($kbd);
$manip2 -> selectKeyboard( $SaX::SAX_CORE_KBD);
$manip2 -> setXKBLayout ("$XKBLayout");

$config->setMode ( $SaX::SAX_MERGE );
if ( ! $config->createConfiguration() ) {
    print "--- " . $config->errorString() . "\n";
    print "--- " . $config->getParseErrorValue() . "\n";
    exit(1);
}
$config->commitConfiguration();

exit (0);
