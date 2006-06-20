#!/usr/bin/env python

#
#  Wade Berrier <wberrier@novell.com>
#
#  ported rpmunpack.c by Gero Kuhlmann to python
#   and made the following changes:
#    1. adapt syntax to be a drop in for rpm2cpio
#    2. addd bz2 support (ha!: hack)
#  
#  http://www.ibiblio.org/pub/Linux/utils/package/rpmunpack.tar.gz
#

import sys
import gzip
import bz2

RPM_MAGIC = "\355\253\356\333"
GZ_MAGIC_1 = '\037'
GZ_MAGIC_2 = '\213'

BZ2_MAGIC_1 = 'B'
BZ2_MAGIC_2 = 'Z'
BZ2_MAGIC_3 = 'h'

# Check for command line parameters 
if len(sys.argv) != 2:
	sys.stderr.write("usage: ./rpm2cpio.py <RPM file>\n")
	sys.exit(1)

# Open up rpm
infile = open(sys.argv[1], 'r')

# Read magic ID  and make sure it's an rpm
buffer = infile.read(4)
if buffer != RPM_MAGIC:
	sys.stderr.write("input file is not in RPM format\n")
	sys.exit(1)

buffer = infile.read(6)		# Skip flags 

# Get and skip past rpm name
buffer = infile.read(64)

#
# Now search for the GZIP signature. This is rather awkward, but I don't
# know any other way how to find out the exact starting position of the
# archive within the input file. There are a couple of data structures
# and texts (obviously descriptions, installation shell scripts etc.)
# coming before the archive, but even they start at different offsets
# with different RPM files. However, it looks like the GZIP signature
# never appears before offset 0x200, so we skip these first couple of
# bytes to make the signature scan a little more reliable.
#

# Skip some more headers...
buffer = infile.read(0x200 - 74)

# Save this location
start = infile.tell()

# Try to proceed as if payload is gzip data
try:
	status = 0
	while status < 2:
		buffer = infile.read(1)
		if status == 0 and buffer[0] == GZ_MAGIC_1:
			status += 1
		elif status == 1 and buffer[0] == GZ_MAGIC_2:
			status += 1
		else:
			status = 0

	# Seek back 2 bytes to include the GZ magic
	infile.seek(infile.tell() - 2)

	# Set up decompress stream
	#  (This fails if the data is not in gzip format)
	outfile = gzip.GzipFile("", 'rb', 9, infile)
	# Copy stream to stdout
	for line in outfile:
		sys.stdout.write(line)

	outfile.close()
except:
	# not a gzip file, try bz2

	# Start over
	infile.seek(start)

	status = 0
	while status < 3:
		buffer = infile.read(1)
		if status == 0 and buffer[0] == BZ2_MAGIC_1:
			status += 1
		elif status == 1 and buffer[0] == BZ2_MAGIC_2:
			status += 1
		elif status == 2 and buffer[0] == BZ2_MAGIC_3:
			status += 1
		else:
			status = 0

	# Seek back 3 bytes to include the BZ2 magic
	infile.seek(infile.tell() - 3)

	data = infile.read()
	sys.stdout.write(bz2.decompress(data))


infile.close()


