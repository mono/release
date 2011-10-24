
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make -k

.check:
	cd mono ; \
	make -k distcheck ; \
	mv -f -v *.tar.gz $(PACKAGES_PATH)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
