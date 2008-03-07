#!/bin/bash
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

if [ "X$type" == "Xvmx" ]; then
# Kiwi doesn't give us swap
	dd if=/dev/zero of=/swap bs=1024 count=512000
	mkswap /swap
	echo "/swap swap swap defaults 0 0" >> /etc/fstab
fi

if [ "X$type" == "Xiso" ]; then
	rm -f /swap
fi
