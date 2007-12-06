#!/bin/sh -x

#This script removes Mono from an OS X System.  It must be run as root

rm -r /Library/Frameworks/Mono.framework

rm -r /Library/Receipts/MonoFramework-1.1.4.pkg

cd /usr/bin
for i in `ls -al | grep Mono | awk '{print $9}'`; do
    rm ${i}
done
