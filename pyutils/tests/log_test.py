#!/usr/bin/env python


import sys
sys.path.append('..')

import logger

log = logger.Logger(print_screen=1, max_size=1)

while(1):
	try:
		log.log("Hey, are we here yet?\n")
	except logger.MaxLogOverflowException:
		print "Hit max logsize of...%d" % log.max_size
		break


while(1):
	log.log("Nope...\n")
