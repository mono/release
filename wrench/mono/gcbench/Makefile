BENCHMARK_REPOSITORY = git://github.com/xamarin/benchmarker.git
BENCH_CONF = configs/default-sgen.conf
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
	if curl -f -o $(TARBALL_NAME) $(DOWNLOAD_URL)/$(TARBALL_NAME); then \
		tar -C benchmarker -xvjf $(TARBALL_NAME); \
	fi
	cd benchmarker && ./runner.sh -c $(BUILD_REVISION) b$(count).$(commit) $(BENCH_CONF)

.collect:
	cd benchmarker \
		&& ./collect.pl results default-sgen \
		&& tar -cvjf $(TARBALL_NAME) results/ \
		&& cp $(TARBALL_NAME) $(PACKAGES_PATH)
	rsync -ave ssh $(PACKAGES_PATH)/$(TARBALL_NAME) benchmarker/results/ $(STORAGE_SERVER):$(STORAGE_ROOT)/$(DESTINATION)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
