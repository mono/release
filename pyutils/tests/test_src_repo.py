#!/usr/bin/env python

import time
import unittest
import sys
sys.path.append('..')

import config
import src_repo_utils

# Can't do this in setUp because it gets run on every case, which won't test the cache
src_repo = src_repo_utils.svn(config.MONO_ROOT, min_wait=2, debug=1)

src_repo.cache_max_size = 1

start_rev = 90000

# Really this tests to see if svn is givint the correct values back... :)
#  we'd need to time to see if the cache was faster or not with the same output
class TestSvn(unittest.TestCase):
    
	def setUp(self):
		# Repeat a function to hit
		start = time.time()
		res = src_repo.latest_path_revision("trunk/release/packaging", 50001)
		end = time.time()
		self.miss = end - start

		# load up cache for cache testing
		for i in range(0,15):
			res = src_repo.latest_path_revision("trunk/release/packaging", 50001 + i)

	def testmiss(self):
		res = src_repo.latest_path_revision("trunk/release/packaging", 49800)
		self.assertEqual(49773, res, "These revisions should match")

	def testhit(self):
		start = time.time()
		res = src_repo.latest_path_revision("trunk/release/packaging", 50001)
		end = time.time()

		self.assertEqual(49810, res, "These revisions should match")
		self.failUnless(end - start < self.miss, "A cache hit should be shorter than a non-cache hit")


if __name__ == '__main__':
	for i in range(0,100):
		unittest.main()
