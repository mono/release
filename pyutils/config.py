# Config vars
import os
import stat

# Default distro to make tarballs on (can be overridden in def file)
mktarball_host = "suse-103-x86_64"

# Set release base dir
#  Must do at startup, opposed to doing this in a function
module_dir = os.path.dirname(__file__)
if module_dir != "": module_dir += os.sep
release_repo_root = os.path.abspath(module_dir + '..')
# This gets set to /home/wberrier/wa/msvn/release


# Packaging paths
packaging_dir = release_repo_root + '/packaging'
platform_conf_dir = packaging_dir + "/conf"
def_dir = packaging_dir + "/defs"

# Full path to where the builds are output
packages_dir = packaging_dir + "/packages"
snapshot_packages_dir = packaging_dir + "/snapshot_packages"

# Source dirs
sources_dir = packaging_dir + "/sources"
snapshot_sources_dir = packaging_dir + "/snapshot_sources"

# smbclient password file
smb_passfile = packaging_dir + "/.smbpass"

# Mono repo svn location
#MONO_ROOT = "svn://anonsvn.mono-project.com/source"
#src_key_file = ""
MONO_ROOT = "svn+ssh://distro@mono-cvs.ximian.com/source"
src_key_file = packaging_dir + os.sep + "distro_source_key"

#buildenv_key_file = ""
buildenv_key_file = packaging_dir + os.sep + "distro_source_key"

# Url path from view of webserver
web_root_url = ""
web_root_dir = release_repo_root + "/monobuild/www"

# 
#build_info_dir = web_root_dir + "/builds/testing"
#build_info_url = web_root_url + "/builds/testing"
build_info_dir = web_root_dir + "/builds"
build_info_url = web_root_url + "/builds"

mktarball_logs = web_root_dir + "/tarball_logs"
mktarball_logs_release_relpath = 'monobuild/www/tarball_logs'

# Can set this to a full path if needed
tar_path="tar"

# Tarball daemon config info
##############################################
td_active = True
# Seconds
td_network_error_interval = 60
td_max_poll_interval = 60
#td_max_poll_interval = 10

# How many revisions to go back when starting to build sequential tarballs
td_num_sequential = 10

# static list of packages to create tarballs for
td_packages = """
	gecko-sharp2
	gluezilla
	gtk-sharp
	libgdiplus
	mod_mono
	mono
	mono-basic
	mono-debugger
	mono-tools
	monodevelop
	monodoc
	moon
	olive
	xsp
""".split()

# builds each and every checkin if true, otherwise, only build the latest checkin
td_sequential = False

##############################################


# Scheduler daemon config info
##############################################
sd_active = True
#  (auto reloading only works for the wakeup_interval and latest_build_packages on the scheduler daemon)
# seconds
sd_wakeup_interval = 60
#sd_wakeup_interval = 300

# Currently not used...
sd_sequential_build_distros = [ 'redhat-9-i386' ]
sd_sequential_build_packages = [ 'mono', 'mono-1.1.13' ]

# List of platforms/packages
	#sunos-8-sparc
sd_latest_build_distros = """
	debian-4-arm
	debian-4-sparc
	macos-10-ppc
	macos-10-x86
	sles-9-i586
	sles-9-ia64
	sles-9-ppc
	sles-9-s390
	sles-9-s390x
	sles-9-x86_64
	sunos-10-x86
	suse-101-i586
	suse-101-x86_64
	suse-103-i586
	win-4-i386
""".split()
sd_latest_build_packages = td_packages
##############################################

# Sync thread options
##############################################
sync_active = True
sync_host = 'mono-web@mono.ximian.com'
sync_target_dir = '~/release'

# Testing
#sync_host = 'wberrier@wblinux.provo.novell.com'
#sync_target_dir = 'wa/msvn/release/monobuild/www/builds'

#sync_num_builds = 50 # 880 MB in one test...
#sync_num_builds = 20 # 434 MB in one test...
sync_num_builds = 10 # 268 MB in one test...

sync_sleep_time = 10

# That's what autoconf gives us... try it out
sync_max_arg_len = 32768
##############################################

##############################################
# Default environment (used by sshutils and packaging.buildenv)
# TODO: there needs to be a better correlation between these env vars and the _path vars in packaging/conf
env_vars = {
	'chroot_path':		'/usr/sbin/chroot',
	'strip_path':		'strip',
	'tar_path':		'tar',
	'make_path':		'make',
	'build_location':	'/tmp/monobuild',
	#'shell_path':		'/bin/sh',
	# We depend on bash (ie: env string in execute_command)
	'shell_path':		'/bin/bash',
	'python_path':		'python', # full path can be set in conf file for individual jails
}

######################################
# Common place for source extensions, which can be compiled to reg later
# Ennumerate to make it simpler...
#  (Src.zip for IronPython)
# (note: these need to be in the order of increasingly less specific, for 'packaging/build')
source_extensions = """
        -src.tar.bz2
        -src.tar.gz
        .tar.bz2
        .tar.gz
        -Src.zip
        -src.zip
        .zip
""".split()

# Results in something like:
# = "(\.tar\.gz|\.zip)"
sources_ext_re_string = "(" + "|".join(source_extensions).replace(".", "\.") + ")"

######################################

######################################
# Commonly used permission settings

all_rwx = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO # 777
shell_perms = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH # 755
data_perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH # 644

######################################

# Common place to put all ssh options
ssh_options = '-o BatchMode=yes -o StrictHostKeyChecking=no -o Cipher=blowfish -o ConnectTimeout=10'

# Add key file to options for all ssh stuff, so all you need is the distro key
if os.path.exists(buildenv_key_file) and buildenv_key_file != "":
	ssh_options += ' -i ' + buildenv_key_file
