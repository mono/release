BENCHMARK_REPOSITORY = git://github.com/xamarin/benchmarker.git
BENCH_CONF = configs/default-sgen.conf

.setup-benchmarker:
	if test ! -d benchmarker; then \
		git clone $(BENCHMARK_REPOSITORY); \
	fi
	cd benchmarker && git pull

.configure:
	mkdir -p $(abspath ../benchmarker/installation)
	cd mono && ./autogen.sh --prefix=$(abspath ../benchmarker/installation)

.make:
	cd mono && make -j6 && make install

count = $(shell (cd mono && git rev-list HEAD) | wc -l | sed -e 's/ *//g' | xargs -n1 printf '%08d')
commit = $(shell (cd mono && git show --abbrev-commit HEAD) | grep '^commit' | sed -e 's/commit //')

.benchmark:
	cd benchmarker && ./runner.sh -c $(BUILD_REVISION) b$(count).$(commit) $(BENCH_CONF)

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
