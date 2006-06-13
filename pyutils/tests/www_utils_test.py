#!/usr/bin/env python

import sys

sys.path += [ '..' ]

import www_utils

args = {'test': "super/unsafe/../../path", 'test2': 'normal arg' }

print www_utils.sanitize_args(args)

