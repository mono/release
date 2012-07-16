
.configure:
	cd mono && ./autogen.sh

.make:
	cd mono && make -k

.dist:
	cd mono && MAKEFLAGS='' make -k dist-bzip2

.deb:
	cd mono && ./external/debian-snapshot/prepare-packaging-metadata.sh
	cd mono ; SNAPSHOT=`echo mono-snapshot-*.tar.bz2 | cut -d' ' -f1` ; \
	mv $$SNAPSHOT /tmp/ && cd /tmp && tar -xvjf $$SNAPSHOT && cd `echo $$SNAPSHOT | cut -d'_' -f1` && dpkg-buildpackage ; \
	cd .. && mv *.deb *.dsc *.changes $(PACKAGES_PATH) ; \
	rm -Rf $$SNAPSHOT `echo $$SNAPSHOT | cut -d'_' -f1`

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
