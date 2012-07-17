.configure:
	cd mono/external/debian-snapshot && git clean -xfd
	cd mono && ./autogen.sh

.make:
	cd mono && make -k

.dist:
	cd mono && rm -f mono-*.tar.* && MAKEFLAGS='' GZIP_ENV=--fast make -k dist-gzip

.deb:
	cd mono && ./external/debian-snapshot/prepare-packaging-metadata.sh
	cd mono ; SNAPSHOT=`echo mono-snapshot-*.tar.gz | cut -d' ' -f1` ; \
	mv $$SNAPSHOT /tmp/ && cd /tmp && tar -xzf $$SNAPSHOT && cd `echo $$SNAPSHOT | cut -d'_' -f1` && dpkg-buildpackage ; \
	cd .. && mv *.deb *.dsc *.changes $(PACKAGES_PATH) ; \
	rm -Rf $$SNAPSHOT `echo $$SNAPSHOT | cut -d'_' -f1`

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
