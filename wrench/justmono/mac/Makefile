
.configure:
	cd mono && ./autogen.sh --host=i386-apple-darwin10 --enable-nls=no --with-ikvm=yes
	killall -9 mono
	killall -9 mono-sgen

.make:
	cd mono && make -k

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
