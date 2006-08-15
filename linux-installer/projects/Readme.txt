Visit http://go-mono.com/archive/@@VERSION@@ for release details.

Please file any bugs or issues at http://bugzilla.ximian.com

Installer changes:

1.1.17:
- Remove gtk# and related apps, since running them from the
  installer was not reliable across distros because of missing
  libraries.
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

