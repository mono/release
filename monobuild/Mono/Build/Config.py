

releaseRepo = "/home/wberrier/wa/msvn/release"

platformDir = releaseRepo + "/packaging/conf"
packageDir = releaseRepo + "/packaging/defs"

rootUrl = ""

# Full path to where the builds are output
#buildsDir = releaseRepo + "/monobuild/www/builds"
# Url path from view of webserver
#buildsUrl = rootUrl + "/builds"

# Testing
buildsDir = releaseRepo + "/monobuild/www/builds/testing"
buildsUrl = "builds/testing"

mktarballPlatform = "suse-93-i586"


# Mono repo svn location
#MONO_ROOT = " svn+ssh://distro@mono-cvs.ximian.com/source"
MONO_ROOT = " svn+ssh://wade@mono-cvs.ximian.com/source"

