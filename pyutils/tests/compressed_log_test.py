#!/usr/bin/env python

import time
import sys

sys.path.append("..")

import logger

my_logger = logger.Logger('test.log', compressed=1)

count = 0
while 1:
	my_logger.log(str(count) + "\n")
	time.sleep(1)
	count += 1

