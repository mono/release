.configure:
	cd mono/external/debian-snapshot && rm -rf temp
	cd mono && GZIP_ENV=--fast ./autogen.sh

.make:
	cd mono && make -k

.dist:
	cd mono && rm -f mono-*.tar.* && MAKEFLAGS='' GZIP_ENV=--fast make -k dist-gzip

.deb:
	cd mono && ./external/debian-snapshot/prepare-packaging-metadata.sh
	cd mono && ./external/debian-snapshot/build-package.sh
	cd mono/external/debian-snapshot/ && mv *.deb mono-snapshot-*.tar.* *.dsc $(PACKAGES_PATH)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
