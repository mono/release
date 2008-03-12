#!/bin/bash -x
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

if [ "$type" = "vmx" ]; then
# Kiwi doesn't give us swap
	mount -o bind /lib/udev/devices /dev
	dd if=/dev/zero of=/swap bs=1024 count=512000
	/sbin/mkswap /swap
	echo "/swap swap swap defaults 0 0" >> /etc/fstab
	umount /dev
fi

if [ "$type" = "iso" ]; then
	sed -i '/^\/swap/d' /etc/fstab
	rm -f /swap
	if rpm -q kernel-source; then
		rpm -ev kernel-source
	fi
fi

for package in $delete; do
	if rpm -q $package; then
		rpm -ev $package
	fi
done
