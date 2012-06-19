BUILD_REPOSITORIES := \
	git@github.com:mono/monodevelop.git

.configure:
	cd monodevelop; \
	./configure --profile=dist --enable-tests

.make:
	cd monodevelop; \
	make; \
	make dist
.test:
	cd monodevelop && make test assembly=$(assembly)

.package:
	mv -f -v monodevelop/tarballs/*.tar.bz2 $(PACKAGES_PATH)
	mv -f -v monodevelop/specs/*.spec $(PACKAGES_PATH)


.clean::
	-cd monodevelop && make clean

include wrench.make
