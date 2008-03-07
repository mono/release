#!/bin/sh

########################
# zypper repositories
zypper addrepo http://download.opensuse.org/update/10.3 10.3-update
zypper addrepo http://download.opensuse.org/distribution/10.3/repo/debug 10.3-debug
zypper addrepo http://www.go-mono.com/download-stable/suse-103-i586 mono
zypper addrepo http://mono.ximian.com/monobuild/preview/download-preview/suse-103-i586 mono-preview

#disabled until bug 353489 is fixed
zypper modifyrepo --disable 10.3-update

zypper modifyrepo --disable mono-preview

for repo in "10.3-oss" "10.3-non-oss" "10.3-update" "10.3-debug" "mono" "mono-preview"; do
	zypper modifyrepo --disable-autorefresh $repo
done

rpm -ev $delete

# Turn ssh back on
chkconfig sshd on
# Turn on samba
chkconfig nmb on
chkconfig smb on

########################
# Kiwi hacks

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

mv /tmp/web-apps 'Mono Web Applications'
mv /tmp/web-sites 'Mono Web Sites'

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
