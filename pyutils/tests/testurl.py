#!/usr/bin/env python

import sys

sys.path.append("..")

import utils

# Ftp missing, valid
utils.get_url("ftp://ftp.gnome.org/pub/GNOME/platform/2.12/2.12.2/win32/glib-2.8.6.zip", '.')
utils.get_url("ftp://ftp.gnome.org/pub/GNOME/platform/2.16/2.16.0/win32/glib-2.12.3.zip", '.')

# Valid dir, invalid file
utils.get_url("ftp://ftp.gnome.org/pub/GNOME/platform/2.16/2.16.0/glib-2.12.3_invalid.zip", '.')

# Http missing, valid
utils.get_url("http://www.google.com/1234", '.')
utils.get_url("http://www.google.com/index.html", '.')

