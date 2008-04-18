Visit http://mono-project.com/Downloads for release details.

Please file any bugs or issues at http://bugzilla.ximian.com

Warning: gtk-sharp apps (Monodoc, MonoDevelop, etc...)
  may not work on all distros.  This is due to differing
  gtk+ versions.  Also, if you want to run MonoDevelop,
  you must have the Gnome libraries installed.  During the
  installation, bin/.installer_post_libscan was run to try
  to find any libraries with unresolved symbols.  This should
  help locate missing libraries.

Note: If you selected to have your environment modified by
  the installer, you will need to restart your shell for
  these changes to take effect.
  If you decided against the installer modifying your
  environment, you can load the necessary settings by 
  sourcing 'bin/setup.sh'.  This is done by running:

source <install dir>/bin/setup.sh

  You need to replace <install dir> with the directory you
  chose for installation.  These settings are not permanent 
  and will only affect the current environment.

Installer changes:

1.9.1-3:
- Resctrict installation target to user's home dir and
  /opt/mono for root.  This way it won't override the
  system Mono in /usr.
- Move environment setup to post install script.
- Adding .desktop launch with a terminal that has the
  environment set up.

1.2.3-2:
- Add postinstall script to find unresolved symbols for 
  native libraries
- Add setup.sh for command line usage.  Also use it for
  monodoc and monodevelop so that launching these does not 
  require a restart after installation.

1.1.17:
- Add some libgdiplus deps, as well as some other base deps.  
  These deps may be on most installations, but include them to 
  make sure.

1.1.14:
- Added graphics libs for libgdiplus; fixed libtiff symlinks.

1.1.11:
- Added heap-buddy

1.1.10.1:
- Fix Monodevelop help browsing

1.1.10:
- Install Software has been updated to Bitrock 3.0.1
- Since Mono is relocatable, the wrapper scripts
  are not needed anymore

