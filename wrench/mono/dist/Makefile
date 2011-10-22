
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make

.check:
	cd mono && make distcheck
	mv -f -v mono/*.tar.gz $(PACKAGES_PATH)

.clean::
	-cd mono && make distclean

include wrench.make
