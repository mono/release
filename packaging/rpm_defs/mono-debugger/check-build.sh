#!/bin/bash
# Copyright (c) 2003, 2004 SuSE Linux AG, Germany.  All rights reserved.
#
# Authors: Thorsten Kukuk <kukuk@suse.de>
#
# this script use the following variable(s):
# 
# - $BUILD_BASENAME
#

# Mono needs a 2.6.13 kernel on x86-64 machines, it definitly fails with 2.6.5.

case $BUILD_BASENAME in
   *i386*|*i686*|*x86_64*)
        grep "Linux version 2.[0-5].[0-9][0-9]" /proc/version > /dev/null
        if [ $? -ne 1 ]; then
          echo "FATAL: kernel too old, need kernel >= 2.6.13 for this package"
          exit 1
        fi
        grep "Linux version 2.6.[0-9]-" /proc/version > /dev/null
        if [ $? -eq 0 ]; then
          echo "FATAL: kernel too old, need kernel >= 2.6.13 for this package"
          exit 1
        fi
        grep "Linux version 2.6.1[0-2]-" /proc/version > /dev/null
        if [ $? -eq 0 ]; then
          echo "FATAL: kernel too old, need kernel >= 2.6.13 for this package"
          exit 1
        fi
        grep "Linux version 2\.6\.1[0-2]\.[0-9]*-" /proc/version > /dev/null
        if [ $? -eq 0 ]; then
          echo "FATAL: kernel too old, need kernel >= 2.6.13 for this package"
          exit 1
        fi
   ;;
   *)
   ;;
esac

exit 0

