
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make -k

.dist:
	cd mono ; \
	make -k dist-bzip2 ; \
	EC=$$? ; \
	mv -f -v *.tar.* $(PACKAGES_PATH) ; \
	exit $$EC

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
