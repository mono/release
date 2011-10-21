
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make all dist

.check:
	cd mono && make distcheck

.clean::
	-cd mono && make distclean

include wrench.make
