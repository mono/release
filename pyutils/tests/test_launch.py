#!/usr/bin/env python

import utils

print_output = 0

print utils.launch_process('ls /tmp', capture_stderr=1, print_output=print_output)

print utils.launch_process('ls /junk', capture_stderr=1, print_output=print_output)

print utils.launch_process('ls /tmp', capture_stderr=0, print_output=print_output)

print utils.launch_process('ls /junk', capture_stderr=0, print_output=print_output)

print utils.launch_process('./a.out', capture_stderr=1, print_output=print_output)
