
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

.monolite:
	cd mono/mcs/class/lib/basic ; \
	MONO_CORLIB_VERSION=$(sed -n "s/\#define MONO_CORLIB_VERSION //p" ../../../../mono/metadata/appdomain.c) ; \
	MONOLITE=monolite-$$MONO_CORLIB_VERSION-$DATE ; \
	mkdir -p $$MONOLITE ; \
	cp *.dll *.exe $$MONOLITE ; \
	tar zcvpf $$MONOLITE.tar.gz $$MONOLITE/ ; \
	mv -f -v $$MONOLITE.tar.gz $(PACKAGES_PATH)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
