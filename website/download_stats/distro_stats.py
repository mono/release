#!/usr/bin/env python

import glob
import re

arch_count = {}
distro_count = {}
distro_ver_count = {}
distro_ver_arch_count = {}
distro_arch_count = {}

arch_size = {}
distro_size = {}
distro_ver_size = {}
distro_ver_arch_size = {}
distro_arch_size = {}

distros = """
	sles
	suse
	fedora
	rhel
""".split()

archs = """
	i.86
	x86_64
	ia64
	ppc
	s390
	s390x
""".split()

def accumulate(type, key, num):

	if not type.has_key(key):
		type[key] = 0
	type[key] += int(num)

def sort_and_output(title, type):

	print "--------------------------------------------"
	print title
	print ""

	# create reverse lookup to sort by value
	new ={}
	for k,v in type.iteritems():
		new[v] = k

	sorted = new.keys()
	sorted.sort()
	sorted.reverse()

	total = sum(sorted)
	for i in sorted:
		print "%-20s:%15d (%.2f%%)" % (new[i], i, float(i) / float(total))

	print ""
	print "Total: %d" % total
	print "--------------------------------------------"
	print ""

# collect stats

for i in glob.glob("www_http/url_*.tab") + glob.glob("www_ftp/url_*.tab"):
	
	fd = open(i)

	for line in fd.readlines():

		(hits, total_size, url) = line.split()

		# What distro and arch? (if any)
		m1 = re.search("\/(%s)-(\d+)-(%s)\/" % ("|".join(distros), "|".join(archs)), line)
		if m1:

			(distro, ver, arch) = m1.groups()

			accumulate(arch_count, arch, hits)
			accumulate(distro_count, distro, hits)
			accumulate(distro_ver_count, "-".join((distro,ver)), hits)
			accumulate(distro_arch_count, "-".join((distro,arch)), hits)
			accumulate(distro_ver_arch_count, "-".join((distro,ver,arch)), hits)

			accumulate(arch_size, arch, total_size)
			accumulate(distro_size, distro, total_size)
			accumulate(distro_ver_size, "-".join((distro,ver)), total_size)
			accumulate(distro_arch_size, "-".join((distro,arch)), total_size)
			accumulate(distro_ver_arch_size, "-".join((distro,ver,arch)), total_size)

	fd.close()

# display reports

sort_and_output("Architecture Hits Count", arch_count)
sort_and_output("Distribution Hits Count", distro_count)
sort_and_output("Distribution Version Hits Count", distro_ver_count)
sort_and_output("Distribution Architecture Hits Count", distro_arch_count)
sort_and_output("Distribution Arch Version Hits Count", distro_ver_arch_count)

sort_and_output("Architecture Download Size", arch_size)
sort_and_output("Distribution Download Size", distro_size)
sort_and_output("Distribution Version Download Size", distro_ver_size)
sort_and_output("Distribution Architecture Download Size", distro_arch_size)
sort_and_output("Distribution Arch Version Download Size", distro_ver_arch_size)

