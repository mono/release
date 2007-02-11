DEVKIT	= mono
PACKAGE	= scratchbox-devkit-$(DEVKIT)
FILES	= /scratchbox/devkits/$(DEVKIT)/
VERSION	= $(MONO_VERSION)
ARCH	= $(shell dpkg-architecture -qDEB_BUILD_ARCH)

PACKAGE_TARGETS	= tarball deb rpm

.PHONY: build packages $(PACKAGE_TARGETS) clean

build:
	$(MAKE) -C meta/devkit install
	install -m 644 ChangeLog /scratchbox/devkits/mono/

packages: $(PACKAGE_TARGETS)

tarball:
	tar cfz ../$(PACKAGE)-$(VERSION)-$(ARCH).tar.gz --owner=root --group=root $(FILES)

deb:
	fakeroot debian/rules clean
	fakeroot debian/rules binary

rpm:
	sed "s/<VERSION>/$(VERSION)/" rpm/spec.in > rpm/spec
	echo $(FILES) >> rpm/spec
	rpmbuild --rcfile /usr/lib/rpm/rpmrc:rpm/rpmrc -bb rpm/spec
	mv rpm/$(ARCH)/* ..

clean:
	find . -type d -maxdepth 2 -mindepth 2 ! -name CVS -exec make -C {} clean \;
	fakeroot debian/rules clean
	rm -rf rpm/$(ARCH)
	rm -f rpm/spec
