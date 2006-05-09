#!/usr/bin/env python

import utils

print utils.get_destroot(utils.distro_info('sunos-8-sparc'), 'mono-1.1')
print utils.get_destroot(utils.distro_info('win-4-i386'), 'mono-1.1')
print utils.get_destroot(utils.distro_info('fedora-3-i386'), 'mono-1.1')
print utils.get_destroot(utils.distro_info('fedora-4-x86_64'), 'mono-1.1')
print utils.get_destroot(utils.distro_info('sles-9-x86_64'), 'mono-1.1')
print utils.get_destroot(utils.distro_info('sunos-8-sparc'), 'gtk-sharp')
print utils.get_destroot(utils.distro_info('fedora-4-x86_64'), 'ikvm')
print utils.get_destroot(utils.distro_info('fedora-3-i386'), 'libgdiplus-1.1')
print utils.get_destroot(utils.distro_info('win-4-i386'), 'libgdiplus-1.1')

print utils.get_destroot(utils.distro_info('win-4-i386'), 'mono-debugger')
print utils.get_destroot(utils.distro_info('nld-9-i586'), 'mono-debugger')
print utils.get_destroot(utils.distro_info('nld-9-i586'), 'monodevelop')


print utils.get_package_path(utils.distro_info('nld-9-i586'), 'monodevelop')
