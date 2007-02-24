#!/bin/sh
#
# USAGE: update-status VERSION NAME
#
VERSION=$1
NAME=$2
SECTIONS=(
#	Microsoft.VisualBasic
	System
	System.Configuration.Install
	System.Data
	System.Data.OracleClient
	System.Design
	System.DirectoryServices
	System.Drawing
	System.Drawing.Design
	System.EnterpriseServices
	System.Management
	System.Messaging
	System.Runtime.Remoting
	System.Runtime.Serialization.Formatters.Soap
	System.Security
	System.ServiceProcess
	System.Web
	System.Web.Services
	System.Windows.Forms
	System.Xml
	cscompmgd
	mscorlib
)

DEST="mono-web@mono.ximian.com:go-mono/class-status/$NAME"

CLASS_STATUS_DIR=$(dirname $(which $0))
SCRIPTS_DIR=$(dirname $(which $0))/..
cd ./mono/web/web

#
# Download the masterinfo files and unpack them
#
#wget -nv -O masterinfos-$VERSION.tar.gz http://mono.ximian.com/masterinfos/masterinfos-$VERSION.tar.gz
wget -m http://mono.ximian.com/masterinfos/masterinfos-$VERSION.tar.gz
test $? -eq 0 || exit 1
cp mono.ximian.com/masterinfos/masterinfos-$VERSION.tar.gz .
tar zxpf masterinfos-$VERSION.tar.gz

PROFILE=nonesuch
case $VERSION in
1.1) PROFILE=default ;;
2.0) PROFILE=net_2_0 ; SECTIONS=(
		${SECTIONS[@]}
		Microsoft.Build.Engine
		Microsoft.Build.Framework
		Microsoft.Build.Tasks
		Microsoft.Build.Utilities
		Microsoft.VisualBasic
		System.Configuration
		System.ServiceProcess
		System.Transactions
	) ;;
esac

#
# Build the necessary tools
#
echo "Build tools"
mcs -nowarn:0618 transform.cs XhtmlWriter.cs
(cd ../../../mcs/tools/corcompare; make PROFILE=default || exit 1)
(cd ../../../mcs/tools/corcompare; make PROFILE=$PROFILE || exit 1)

#
# Generate the data
#
echo "Generate the data"
for i in ${SECTIONS[@]} ; do
    echo $i
    mono ../../../mcs/class/lib/$PROFILE/mono-api-info.exe $i > infos/$i.xml || (rm -f infos/$i.xml && exit 1)
    mono ../../../mcs/tools/corcompare/mono-api-diff.exe masterinfos/$i.xml infos/$i.xml > src/$i.xml || (rm -f src/$i.xml && exit 1)
    mono ./transform.exe src/$i.xml ../../../mcs/tools/corcompare/mono-api.xsl > src/$i.html.in || (rm -f src/$i.html.in && exit 1)
    perl htmlify src/$i.html.in > src/class-status-$i.src
done

#
# Apply the template to the src files to form the final HTML file
#
echo "Apply the template"
$CLASS_STATUS_DIR/apply-template.py $CLASS_STATUS_DIR/template.html $CLASS_STATUS_DIR/index-$VERSION.src index.html
for file in src/*.src; do
    f=src/`basename $file .src`
    $CLASS_STATUS_DIR/apply-template.py $CLASS_STATUS_DIR/template.html $f.src $f.html
done

#
# Upload the templates and files
#
echo "Upload template"
chmod 644 src/*.html index.html
scp -i $SCRIPTS_DIR/key/cron_key -o "StrictHostKeyChecking no" -C -q src/*.html index.html $DEST/
chmod 644 deploy/cm/*
scp -i $SCRIPTS_DIR/key/cron_key -o "StrictHostKeyChecking no" -q deploy/cm/* $DEST/cm/


