
.configure:
	cd mono && ./autogen.sh --build=x86_64-apple-darwin10 --enable-nls=no --with-ikvm=yes

.make:
	cd mono && make -k

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
