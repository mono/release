
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

.deb:
	./external/debian-snapshot/prepare-packaging-metadata.sh
	SNAPSHOT=`echo mono-snapshot-*.tar.bz2 | cut -d' ' -f1` ; \
	mv $$SNAPSHOT /tmp/ && cd /tmp && tar -xvjf $$SNAPSHOT && cd `basename $$SNAPSHOT .tar.bz2` && dpkg-buildpackage ; \
	cp *.deb $(PACKAGES_PATH) ; \
	cd ../ && rm -Rf $$SNAPSHOT `basename $$SNAPSHOT .tar.bz2`

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
