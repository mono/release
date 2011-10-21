
## Variable Defaults:

# this is where the sources will be checked out if individual scripts don't override SOURCES_PATH
DEFAULT_SOURCES_PATH := $(shell mkdir -p /tmp/source && echo /tmp/source)

# PACKAGES_PATH is where individual release scripts should drop their package(s)
DEFAULT_PACKAGES_PATH := $(shell mkdir -p `pwd`/package && echo `pwd`/package)

## These can be overridden by individual scripts:

SOURCES_PATH ?= $(DEFAULT_SOURCES_PATH)
PACKAGES_PATH ?= $(DEFAULT_PACKAGES_PATH)
BUILD_REPOSITORIES ?= $(BUILD_REPOSITORY_SPACE)


# BUILD_REPOSITORY_SPACE is automatically set by wrench to the git repository URLs
# strip those down to just the names of the checkout directories...
BUILD_REPOSITORY_NAMES := $(shell echo ${BUILD_REPOSITORIES} | perl -ne 'while (m/\/([^\/\.]+)\.git/g) { print "$$1 " }')
BUILD_REPOSITORY_PATHS := $(addprefix $(SOURCES_PATH)/,$(BUILD_REPOSITORY_NAMES))

MAIN_REPO = $(firstword $(BUILD_REPOSITORY_NAMES))
DEPENDENCIES = $(wordlist 2, $(words $(BUILD_REPOSITORY_NAMES)), $(BUILD_REPOSITORY_NAMES))

all: package

.checkout:: .clean
	cd $(MAIN_REPO) && git fetch && git checkout $(BUILD_REVISION)
	for repo in $(DEPENDENCIES); do ( cd $$repo && git fetch ); done

.clean:: $(BUILD_REPOSITORY_NAMES)
	cd $(MAIN_REPO) && git clean -xfd
	for repo in $(DEPENDENCIES); do ( cd $$repo && git clean -xfd ); done

$(BUILD_REPOSITORY_NAMES):
	mkdir -p $(SOURCES_PATH)
	-for repo in $(filter %$@.git, $(BUILD_REPOSITORIES)); do ( cd $(SOURCES_PATH) && git clone $$repo ); done
	ln -sv $(SOURCES_PATH)/$@ .

checkout: .checkout

configure: checkout .configure

make: configure .make

.PHONY: all checkout configure make
