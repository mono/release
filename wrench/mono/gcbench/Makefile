BENCHMARK_REPOSITORY = git://github.com/xamarin/benchmarker.git
BENCH_CONF = configs/default-sgen.conf
DESTINATION="$BUILD_LANE/${BUILD_REVISION:0:2}/$BUILD_REVISION";
STORAGE_SERVER="builder@storage.bos.xamarin.com";
STORAGE_ROOT="/srv/www/storage.bos.xamarin.com";
UPLOAD = results

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
	cd benchmarker && ./runner.sh -c $(BUILD_REVISION) b$(count).$(commit) $(BENCH_CONF)

.collect:
	cd benchmarker && ./collect.pl results default-sgen
	ssh $(STORAGE_SERVER) mkdir -p $(STORAGE_ROOT)/$(DESTINATION)
	sleep 2
	scp -r $(UPLOAD) $(STORAGE_SERVER):$(STORAGE_ROOT)/$(DESTINATION) \
		&& ssh $STORAGE_SERVER ln -nsf ${BUILD_REVISION:0:2}/$(BUILD_REVISION) $(STORAGE_ROOT)/$(BUILD_LANE)/latest; 
	sleep 2
	echo "@MonkeyWrench: AddFileLink: <a href='http://storage.bos.xamarin.com/"$(DESTINATION)/$(UPLOAD)/"index.html'>""</a>";

.clean::
	-cd $(SOURCES_PATH)/mono && make distclean

include wrench.make
