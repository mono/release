
API_UPLOAD := rsync -tz --delay-updates *.dll mono-api-upload@go-mono.com:~mono-web/go-mono/status/binary

#TARBALL_PATH=$BUILD_DATA_LANE/$(echo $BUILD_REVISION | head -c 8)/dependencies/mono-dist-master
#TARBALL=$(find $TARBALL_PATH -name 'mono-*.tar.*')
#NAME=$(basename $TARBALL)

.configure:
	cd mono && ./autogen.sh

.make:
	rpmbuild -ba mono/mono-core.spec

.package:
	@mkdir -p package
	find /usr/src/packages -type f -name "*.rpm" -exec mv {} package/ ';'

.upload:
	cd mono/mcs/class/lib/net_2_0 && $(API_UPLOAD)/2.0
	#cd mono/mcs/class/lib/net_4_0 && $(API_UPLOAD)/4.0
	cd mono/mcs/class/lib/net_4_5 && $(API_UPLOAD)/4.5

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
