
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make all dist
	mv -f -v mono/*.tar.gz $(PACKAGES_PATH)

.check:
	cd mono && make distcheck

.clean::
	-cd mono && make distclean

include wrench.make
