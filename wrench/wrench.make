## Variable Defaults:

# source cache
SOURCES_PATH ?= $(shell mkdir -p /tmp/source && echo /tmp/source)

# build root (usually temp workspace created by wrench/jenkins)
BUILD_PATH ?= $(shell pwd)

# where individual release scripts will drop their package(s)
PACKAGES_PATH ?= $(shell mkdir -p `pwd`/package && echo `pwd`/package)

MSBUILD ?= /c/Windows/Microsoft.NET/Framework/v4.0.30319/msbuild.exe

# BUILD_REPOSITORY_SPACE is automatically set by wrench to the git repository URLs
BUILD_REPOSITORIES ?= $(BUILD_REPOSITORY_SPACE)
BUILD_REVISION ?= $(GIT_COMMIT)

# strip those down to just the names of the checkout directories...
# foo/bar.git => bar
BUILD_REPOSITORY_NAMES := $(shell echo ${BUILD_REPOSITORIES} | perl -ne 'while (m/\/([^\/]+)\.git/g) { print "$$1 " }')
# foo/bar.git => foo/bar
PREFIXED_BUILD_REPOSITORY_NAMES := $(shell echo ${BUILD_REPOSITORIES} | ruby -ne 'puts $$_.scan(/github\.com.(\S+)\.git/).join(" ")')

SOURCE_CACHE_CHECKOUTS := $(addprefix $(SOURCES_PATH)/,$(PREFIXED_BUILD_REPOSITORY_NAMES))
BUILD_ROOT_CHECKOUTS   := $(addprefix $(BUILD_PATH)/,$(BUILD_REPOSITORY_NAMES))

all: package

SUFFIX=&& (git checkout $(BUILD_REVISION) && git submodule update --init --recursive) 2>/dev/null) || (cd
CHECKOUT_COMMAND=(cd $(addsuffix $(SUFFIX) ,$(BUILD_ROOT_CHECKOUTS)) could-not-match-revision-to-repo)
COPY_TO_BUILD_DIR=(cd $(BUILD_PATH) && cp -r $(SOURCES_PATH)/$@ $(notdir $@))

.checkout:: .clean
	$(CHECKOUT_COMMAND)

.clean:: $(PREFIXED_BUILD_REPOSITORY_NAMES)
	@echo Repositories cleaned

# First assume the checkout is there and try to update it and copy to the build dir
# If that fails for any reason, delete it and try with a fresh clone
$(PREFIXED_BUILD_REPOSITORY_NAMES):
	@rm -rf $(BUILD_PATH)/$(notdir $@)

	repo=$(filter %$@.git, $(BUILD_REPOSITORIES)) && \
	( \
		(cd $(SOURCES_PATH)/$@ && git clean -xfd && git submodule foreach git clean -xfd && git pull --rebase && git submodule update --init --recursive && $(COPY_TO_BUILD_DIR)) || \
		(cd $(SOURCES_PATH) && rm -rf $@ && git clone --recursive $$repo $@ && $(COPY_TO_BUILD_DIR)) \
	)

checkout: .checkout

configure: checkout .configure

make: configure .make

package: make .package

.PHONY: all checkout configure make package
