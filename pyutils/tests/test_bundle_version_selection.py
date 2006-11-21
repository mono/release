#!/usr/bin/env python

import sys
import pdb

sys.path.append("../pyutils")

import packaging

bundle_conf = packaging.bundle(bundle_name='1.1.13')

for i in ['gtk-sharp', 'gtk-sharp-2.0', 'gtk-sharp-2.8']:
        env = packaging.buildenv('suse-101-i586')
        pack = packaging.package(env, i, bundle_obj=bundle_conf, source_basepath='/var/www/mono-website/go-mono/sources', package_basepath='/var/www/mono-website/go-mono/download')

        print "\n".join(pack.get_files())

        print pack.get_source_file()

