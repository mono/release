
.configure:
	cd mono && ./autogen.sh --host=i386-apple-darwin10

.make:
	cd mono && make -k

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
