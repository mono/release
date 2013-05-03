BUILD_REPOSITORIES := \
	git@github.com:mono/monodevelop.git

.configure:
	cd monodevelop && ./configure --profile=dist --enable-tests

.make:
	make -C monodevelop all

.test:
	make -C monodevelop test assembly=$(assembly)

.dist:
	make -C monodevelop dist

.package:
	mv -f -v monodevelop/tarballs/*.tar.bz2 $(PACKAGES_PATH)
	mv -f -v monodevelop/specs/*.spec $(PACKAGES_PATH)

include wrench.make
