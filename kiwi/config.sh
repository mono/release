#!/bin/bash
#================
# FILE          : config.sh
#----------------
# PROJECT       : OpenSuSE KIWI Image System
# COPYRIGHT     : (c) 2006,2007,2008 SUSE LINUX Products GmbH. All rights reserved
#               :
# AUTHOR        : Marcus Schaefer <ms@suse.de>, Stephan Kulow <coolo@suse.de>
#               :
# LICENSE       : BSD
#======================================
# Functions...
#--------------------------------------
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

exec > /var/log/config.log
exec 2>&1

#======================================
# Greeting...
#--------------------------------------
echo "Configure image: [$name]..."

#======================================
# Load sound drivers by default
#--------------------------------------
perl -ni -e 'm,^blacklist snd-, || print;' \
	/etc/modprobe.d/blacklist

# and unmute their mixers.
perl -pi -e 's,/sbin/alsactl -F restore,/bin/set_default_volume -f,;' \
	/etc/udev/rules.d/40-alsa.rules

#--------------------------------------
# these two we want to disable for policy reasons
#chkconfig sshd off
chkconfig cron off

# enable create_xconf
chkconfig create_xconf on
chkconfig boot.langset on

cd /
patch -p0 < /tmp/config.patch
rm /tmp/config.patch

# disabled for now - if you reenable, don't forget correct_live_install
# bnc#382158
# patch -p0 < /etc/YaST2/policy.patch

for i in /rpmkeys/gpg*.asc; do 
   rpm --import $i && rm $i
done
rmdir /rpmkeys

insserv 

rm -rf /var/cache/zypp/raw/*

# TODO: take them directly out of control.xml
zypper addrepo -d http://download.opensuse.org/distribution/11.0/repo/oss/ "11.0-oss"
zypper addrepo -d http://download.opensuse.org/distribution/11.0/repo/non-oss/ "11.0-non-oss"
zypper addrepo -d http://download.opensuse.org/update/11.0/ "11.0-updates"
zypper mr -p 120 "11.0-oss"
zypper mr -p 120 "11.0-non-oss"
zypper mr -p 20 "11.0-updates"

rm -rf /var/cache/zypp/raw/*

#======================================
# /etc/sudoers hack to fix #297695 
# (Installation Live CD: no need to ask for password of root)
#--------------------------------------
sed -i -e "s/ALL ALL=(ALL) ALL/ALL ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers 
chmod 0440 /etc/sudoers

/usr/sbin/useradd -m -u 999 linux -c "Rupert Monkey" -p '$2a$05$DlJal4RD7tKd3trZ6Qjb5ufS7cJ4R7O56g8yNn8SYcLPvpelTl7lq'

# delete passwords
#passwd -d root
#passwd -d linux
# empty password is ok
#pam-config -a --nullok

: > /var/log/zypper.log

mv /tmp/*.pdf /home/linux

#======================================
# SuSEconfig
#--------------------------------------
mount -o bind /lib/udev/devices /dev
rm -rf /usr/share/icons/*/icon-theme.cache
suseConfig
umount /dev

test -x /usr/bin/kbuildsycoca4 && su - linux -c /usr/bin/kbuildsycoca4

#======================================
# Mono System configuration
#--------------------------------------
/tmp/config-mono.sh
rm /tmp/config-mono.sh

#======================================
# Umount kernel filesystems
#--------------------------------------
baseCleanMount

rm -rf /var/lib/smart

exit 0
