#!/usr/bin/env python

import sys

sys.path += ['..']

import utils

utils.launch_process('./timeout_script.sh', output_timeout=3)

