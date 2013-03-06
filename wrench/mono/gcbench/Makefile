BENCHMARK_REPOSITORY = git://github.com/xamarin/benchmarker.git
DESTINATION = $(BUILD_LANE)
STORAGE_SERVER = "builder@storage.bos.xamarin.com"
STORAGE_ROOT = "/srv/www/storage.bos.xamarin.com"
DOWNLOAD_URL = http://storage.bos.xamarin.com/$(DESTINATION)/
TARBALL_NAME = gcbench-results.tar.bz2

.setup-benchmarker:
	if test ! -d benchmarker; then \
		git clone $(BENCHMARK_REPOSITORY); \
	fi
	cd benchmarker && git pull

.configure:
	mkdir -p $(abspath ../benchmarker/installation)
	cd mono && ./autogen.sh --prefix=$(abspath benchmarker/installation)

.make:
	cd mono && make -j6 && make install

count = $(shell (cd mono && git rev-list HEAD) | wc -l | sed -e 's/ *//g' | xargs -n1 printf '%08d')
commit = $(shell (cd mono && git show --abbrev-commit HEAD) | grep '^commit' | sed -e 's/commit //')

.benchmark:
	for i in "1 2 3 4 5"; do \
		if curl -f -o $(TARBALL_NAME) $(DOWNLOAD_URL)/$(TARBALL_NAME); then \
			tar -C benchmarker -xvjf $(TARBALL_NAME); \
			break; \
		else \
			sleep 60; \
		fi \
	done
	cd benchmarker && ./runner.sh -c $(BUILD_REVISION) b$(count).$(commit) configs/default-sgen.conf configs/default-boehm.conf

.collect:
	cd benchmarker \
		&& ls -lR results/ \
		&& ./collect.pl --conf configs/default-boehm.conf --conf configs/default-sgen.conf results default-sgen default-boehm \
		&& tar -cvjf $(TARBALL_NAME) results/ \
		&& cp $(TARBALL_NAME) $(PACKAGES_PATH)
	rsync -ave ssh $(PACKAGES_PATH)/$(TARBALL_NAME) benchmarker/results/ $(STORAGE_SERVER):$(STORAGE_ROOT)/$(DESTINATION)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
