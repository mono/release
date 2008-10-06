#!/bin/bash -x

########################
# zypper repositories
zypper addrepo "http://download.opensuse.org/distribution/11.0/repo/debug" 11.0-debug
zypper addrepo "http://www.go-mono.com/download-stable/openSUSE_11.0" mono
zypper addrepo "http://download.opensuse.org/repositories/Mono:/Preview/openSUSE_11.0" mono-preview
zypper addrepo "http://download.opensuse.org/repositories/Mono:/Community/openSUSE_11.0" mono-community

zypper modifyrepo --disable mono-preview

for repo in "11.0-oss" "11.0-non-oss" "11.0-updates" "11.0-debug" "mono" "mono-preview" "mono-community"; do
	zypper modifyrepo --disable-autorefresh $repo
done

for repo in "11.0-oss" "11.0-updates" "11.0-debug" "mono" "mono-community"; do
	zypper modifyrepo --enable $repo
done

# Turn required services on
chkconfig dbus on
chkconfig haldaemon on
chkconfig network on

# Turn ssh on
chkconfig ssh on
# Turn samba on
chkconfig nmb on
chkconfig smb on
# Turn apache and dbs on
chkconfig apache2 on
chkconfig postgresql on
chkconfig mysql on

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
for app in 'beagle-search' 'f-spot' 'gbrainy' 'tomboy' 'banshee-1'; do 
	cp /usr/share/applications/$app.desktop .
done
popd
for app in 'monodevelop' 'monodoc' 'moma'; do 
	cp /usr/share/applications/$app.desktop .
done

mkdir 'Mono Winforms Applications'
pushd 'Mono Winforms Applications'
for app in $(rpm -ql wf-apps | grep .desktop); do
	cp $app .
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
curl http://mono.ximian.com/vm-data/Music.tar.gz | tar xz
# Configs for Banshee
tar xjf /tmp/banshee.tbz

# Photos for F-Spot
curl http://mono.ximian.com/vm-data/Photos.tbz | tar xj
# Configs for F-Spot
tar xjf /tmp/f-spot.tbz

# Setup slab
tar xjf /tmp/slab.tbz

# Setup gnome-do
#tar xjf /tmp/gnome-do.tbz

# Setup mime association for exe
tar xjf /tmp/mime-exe.tbz

chown -R linux:users /home/linux
chown -R linux /srv/www/htdocs
rm -Rf /tmp/*
