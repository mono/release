#!/bin/sh

########################
# zypper repositories
#disabled until bug 353489 is fixed
#zypper addrepo http://download.opensuse.org/update/10.3/ 10.3-update
zypper addrepo http://download.opensuse.org/distribution/10.3/repo/debug/ 10.3-debug
# This doesn't work like it should so we just drop the files in
#for repo in /tmp/*.repo; do
#	zypper addrepo --repo $repo
#done

# Turn ssh back on
chkconfig sshd on
# Turn on samba
chkconfig nmb on
chkconfig smb on

########################
# Kiwi hacks
# Kiwi doesn't let us have swap
#dd if=/dev/zero of=/swap bs=1024 count=512000
#mkswap /swap
# Kiwi only gives us 100MB free
#dd if=/dev/zero of=/extra bs=1024 count=512000

########################
# Default files for home
cd /home/linux

# Remove Live CD desktop files
rm /usr/share/dist/desktop-files/*.desktop

# Desktop Files
tar xjf /tmp/nautilus.tbz
mkdir Desktop
pushd Desktop

mkdir 'Gtk# Applications'
pushd 'Gtk# Applications'
for app in 'beagle-search' 'f-spot' 'gbrainy' 'tomboy' 'banshee'; do 
	ln -s /usr/share/applications/$app.desktop
done
popd
for app in 'monodevelop' 'monodoc'; do 
	ln -s /usr/share/applications/$app.desktop
done

mkdir 'Mono Winforms Applications'
pushd 'Mono Winforms Applications'
for app in $(rpm -ql wf-apps | grep .desktop); do
	ln -s $app
done
# These apps are broken
rm AlbumSurfer.desktop
rm UsingWebBrowser.desktop
popd

mkdir 'Mono Web Applications'
pushd 'Mono Web Applications'
tar xjf /tmp/web-apps.tbz
popd

mkdir 'Mono Web Sites'
pushd 'Mono Web Sites'
tar xjf /tmp/web-sites.tbz
popd

popd

# WinForms Applications Source
tar -xzf /tmp/WinFormsSource.tar.gz

# connect to #mono and #mono-live in xchat
#tar -xzvf /tmp/xchat2.tar.gz

# Music for Banshee
tar xzf /tmp/Music.tar.gz
# Configs for Banshee
tar xjf /tmp/banshee.tbz

# Photos for F-Spot
tar xjf /tmp/Photos.tbz
# Configs for F-Spot
tar xjf /tmp/f-spot.tbz

# Setup slab
tar xjf /tmp/slab.tbz

# Setup mime association for exe
tar xjf /tmp/mime-exe.tbz

chown -R linux:users /home/linux
chown -R linux /srv/www/htdocs
rm -Rf /tmp/*
