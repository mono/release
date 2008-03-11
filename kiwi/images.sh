#!/bin/bash -x
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

echo "Type: $type" > /type

if [ "$type" = "vmx" ]; then
# Kiwi doesn't give us swap
	dd if=/dev/zero of=/swap bs=1024 count=512000
	mkswap /swap
	echo "/swap swap swap defaults 0 0" >> /etc/fstab
fi

if [ "$type" = "iso" ]; then
	rm -f /swap
	rpm -ev kernel-source
fi

rpm -ev $delete
