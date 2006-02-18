#!/bin/sh

CWD=`pwd`
FRAMEWORKPREFIX=$CWD/Library/Frameworks/Mono.framework
MONOPREFIX=$FRAMEWORKPREFIX/Versions/@@MONO_VERSION@@

echo CWD=$CWD
echo FRAMEWORKPREFIX=$FRAMEWORKPREFIX
echo MONOPREFIX=$MONOPREFIX

###############################################
#Create the framework links, so that this is an OS X framework


mkdir -p ${FRAMEWORKPREFIX}/Versions
cd ${FRAMEWORKPREFIX}/Versions
if [ -e "${FRAMEWORKPREFIX}/Versions/Current" ]; then
	rm -f Current
fi

ln -sf @@MONO_VERSION@@ Current
echo "Creating framework links"

mkdir -p ${FRAMEWORKPREFIX}
cd ${FRAMEWORKPREFIX}

if [ ! -d ${FRAMEWORKPREFIX}/Versions/Current/Resoures ]; then
	mkdir -p ${FRAMEWORKPREFIX}/Versions/Current/Resources || echo "Problem creating dir..."
fi

ls $CWD/../*.plist
cp $CWD/../*.plist ${FRAMEWORKPREFIX}/Versions/Current/Resources
cd ${FRAMEWORKPREFIX}
ln -sf ${FRAMEWORKPREFIX}/Versions/Current/Resources Resources

#if [ ! -d Resources ] ; then
#       cd ${MONOPREFIX}
#       mkdir Resources
#       cp ${PLISTS}/version.plist Resources
#       cp ${PLISTS}/Info.plist Resources
#       cd ${FRAMEWORKPREFIX}
#
if [ ! -e Versions/Current/Resources ]; then
	ln -sf Versions/Current/Resources Resources
fi
ln -sf Versions/Current/lib Libraries
ln -sf Versions/Current/include Headers
ln -sf Versions/Current/bin Commands
ln -sf Versions/Current Home


if [ -e Versions/Current/lib/libmono.dylib ]; then
	ln -sf Libraries/libmono.dylib Mono
else
	echo "/Library/Frameworks/Mono.framework/Libraries/libmono.dylib does not exist"
fi

# What's this for?
#  Seems like this shouldn't be needed until post install time
for i in \
  `ls -al ${MONOPREFIX}/bin | grep -v total | grep -v .exe | grep -vw "\." |awk '{print $9}'`; do
  echo ${i}
  ln -sf ${MONOPREFIX}/bin/${i} /usr/bin/${i}
done



