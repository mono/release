#!/usr/bin/perl

$Lang=""; $Terr="";
open(CMDL, "</proc/cmdline" );
while (<CMDL>) {
    if (m,lang=([a-z][a-z])([_@][\w@]+)?,) {
	$Lang=$1;
	$Terr=$2;
	last;
    }
}
close CMDL;
$RcLang="";
$Keyt="";
$XKBLayout="";
if (open(CONF, "</etc/langset/$Lang$Terr" ) ||
    open(CONF, "</etc/langset/$Lang" )) {
    while (<CONF>) {
	m,RC_LANG=(.*), && ($RcLang = $1) ;
	m,KEYTABLE=(.*), && ($Keyt = $1) ;
	m,XKBLAYOUT=(.*), && ($XKBLayout = $1) ;
    }
    close CONF;
}

system("sed -i -e 's,RC_LANG=\".*,RC_LANG=\"$RcLang\",' /etc/sysconfig/language") if $RcLang ne "";
system("sed -i -e 's,KEYTABLE=\".*,KEYTABLE=\"$Keyt\",' /etc/sysconfig/keyboard") if $Keyt ne "";
open(FH, ">/etc/langset.xkb");
print FH "$XKBLAYOUT\n";
close(FH);
