#!/bin/sh -x

#This script removes Mono from an OS X System.  It must be run as root

rm -r /Library/Frameworks/Mono.framework

rm -r /Library/Receipts/MonoFramework-1.0.1.pkg

cd /usr/bin
for i in `ls -al | grep Mono`; do
    echo ${i}
done
