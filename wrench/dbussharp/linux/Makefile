.configure:
	cd dbus-sharp && ./autogen.sh && ./configure --enable-tests

.make:
	cd dbus-sharp && $(MAKE)

.test:
	$(MAKE) -C dbus-sharp/tests test

.dist:
	$(MAKE) -C dbus-sharp dist

.package:
	mv -f -v dbus-sharp/dbus-sharp*.tar.gz $(PACKAGES_PATH)

include wrench.make
