API_UPLOAD := rsync -tz --delay-updates *.dll mono-api-upload@go-mono.com:~mono-web/go-mono/status/binary
MONO_BUILD := /usr/src/packages/BUILD/mono-*

#TARBALL_PATH=$BUILD_DATA_LANE/$(echo $BUILD_REVISION | head -c 8)/dependencies/mono-dist-master
#TARBALL=$(find $TARBALL_PATH -name 'mono-*.tar.*')
#NAME=$(basename $TARBALL)

.configure:
	cd mono && ./autogen.sh

.make:
	@rm -rf $(MONO_BUILD)
	@cd mono && rm -f *.tar.bz2
	cd mono && make -j`grep processor /proc/cpuinfo | wc -l` && make dist-bzip2 && rpmbuild -ta mono-*.tar.bz2
	rm -f mono && ln -s $(MONO_BUILD) ./mono

.package:
	@mkdir -p package
	find /usr/src/packages -type f -name "*.rpm" -exec mv {} package/ ';'

.upload:
	cd $(MONO_BUILD)/mcs/class/lib/net_2_0 && $(API_UPLOAD)/2.0
	cd $(MONO_BUILD)/mcs/class/lib/net_4_0 && $(API_UPLOAD)/4.0
	cd $(MONO_BUILD)/mcs/class/lib/net_4_5 && $(API_UPLOAD)/4.5

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
