.configure:
	cd dbus-sharp && ./autogen.sh && ./configure --enable-tests

.make:
	cd dbus-sharp && $(MAKE)

.test:
	if test -z "$$DBUS_SESSION_BUS_ADDRESS" ; then \
	    eval `dbus-launch --sh-syntax` ; \
	    echo "D-Bus per-session daemon address is: $$DBUS_SESSION_BUS_ADDRESS" ; \
	fi;
	$(MAKE) -C dbus-sharp/tests setup run

.dist:
	$(MAKE) -C dbus-sharp dist

.package:
	mv -f -v dbus-sharp/dbus-sharp*.tar.gz $(PACKAGES_PATH)

include wrench.make
