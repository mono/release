# Config vars

import os

# Set release base dir
#  Must do at startup, opposed to doing this in a function
#  Maybe there's a better way to do this
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
release_repo_root = packaging_root = os.path.abspath(module_dir + '..')


# Packaging paths
packaging_dir = release_repo_root + '/packaging'
platform_conf_dir = packaging_dir + "/conf"
def_dir = packaging_dir + "/defs"

root_url = ""

# Full path to where the builds are output
packages_dir = packaging_dir + "/packages"
snapshot_packages_dir = packaging_dir + "/snapshot_packages"

# Source dirs
sources_dir = packaging_dir + "/sources"
snapshot_sources_dir = packaging_dir + "/snapshot_sources"

# Build info dirs

# Url path from view of webserver

# Testing
build_info_dir = release_repo_root + "/monobuild/www/builds/testing"
build_info_url = "/builds/testing"

mktarball_platform = "suse-93-i586"


# Mono repo svn location
#MONO_ROOT = " svn+ssh://distro@mono-cvs.ximian.com/source"
MONO_ROOT = " svn+ssh://wade@mono-cvs.ximian.com/source"

