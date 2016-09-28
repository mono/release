
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
	MONO_CORLIB_VERSION=$(shell sed -n "s/\#define MONO_CORLIB_VERSION //p" mono/mono/metadata/appdomain.c) ; \
	cd mono/mcs/class/lib/basic ; \
	MONOLITE=monolite-$$MONO_CORLIB_VERSION-latest ; \
	mkdir -p $$MONOLITE ; \
	cp *.dll *.exe $$MONOLITE ; \
	tar zcvpf $$MONOLITE.tar.gz $$MONOLITE/ ; \
	mv -f -v $$MONOLITE.tar.gz $(PACKAGES_PATH)

.jenkins-monolite:
	MONO_CORLIB_VERSION=$(shell sed -n "s/\#define MONO_CORLIB_VERSION //p" mono/metadata/appdomain.c) ; \
	MONOLITE=monolite-$$MONO_CORLIB_VERSION-latest ; \
	make -C mcs/class dist-monolite monolite_dir=$$MONOLITE; \
	tar zcvpf $$MONOLITE.tar.gz mcs/class/lib/$$MONOLITE/ ; \
	mv -f -v $$MONOLITE.tar.gz $(PACKAGES_PATH)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
