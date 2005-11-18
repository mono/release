DATE=`date +'%Y%m%d'`
#DATE=20051017
PATH_TMP=/var/www/html

if [ $1 -eq 4 ]
then
echo "generate the static page for windows"
php generate-html.php --profile=net_2_0 --distro=windowsXP > $PATH_TMP/windowsXP-net_2_0.html
php generate-html.php --profile=default --distro=windowsXP > $PATH_TMP/windowsXP-default.html

echo "cp /var/www/html/testresults/windowsXP/net_2_0/xml&png To mono.ximian.com"
scp /var/www/html/testresults/windowsXP/net_2_0/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/windowsXP/net_2_0/charts/.
scp /var/www/html/testresults/windowsXP/net_2_0/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/windowsXP/net_2_0/xml/.
echo "cp /var/www/html/testresults/suse-90-i586/default/xml&png To mono.ximian.com"
scp /var/www/html/testresults/windowsXP/default/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/windowsXP/default/charts/.
scp /var/www/html/testresults/windowsXP/default/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/windowsXP/default/xml/.

echo "cp /var/www/html/suse-90-i586-net_2_0.html To mono.ximian.com "
scp /var/www/html/windowsXP-net_2_0.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
echo "cp /var/www/html/suse-90-i586-default.html To sachin"
scp /var/www/html/windowsXP-default.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
fi

if [ $1 -eq 3 ] 
then

echo "generate the static page for redhat"
php generate-html.php --profile=net_2_0 --distro=redhat-9-i386 > $PATH_TMP/redhat-9-i386-net_2_0.html
php generate-html.php --profile=default --distro=redhat-9-i386 > $PATH_TMP/redhat-9-i386-default.html

echo "cp /var/www/html/testresults/redhat-9-i386/net_2_0/xml&png To mono.ximian.com"
scp /var/www/html/testresults/redhat-9-i386/net_2_0/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/redhat-9-i386/net_2_0/charts/.
scp /var/www/html/testresults/redhat-9-i386/net_2_0/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/redhat-9-i386/net_2_0/xml/.
echo "cp /var/www/html/testresults/redhat-9-i386/default/xml&Png To mono.ximian.com"
scp /var/www/html/testresults/redhat-9-i386/default/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/redhat-9-i386/default/charts/.
scp /var/www/html/testresults/redhat-9-i386/default/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/redhat-9-i386/default/xml/.

echo "cp /var/www/html/redhat-9-i386-net_2_0.html To mono.ximian.com"
scp /var/www/html/redhat-9-i386-net_2_0.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
echo "cp /var/www/html/redhat-9-i386-default.html To mono.ximian.com"
scp /var/www/html/redhat-9-i386-default.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.


fi

if [ $1 -eq 2 ] 
then

echo "generate the static page for fedora"
#php generate-html.php --profile=net_2_0 --distro=fedora-1-i386 > $PATH_TMP/fedora-1-i386-net_2_0.html
#php generate-html.php --profile=default --distro=fedora-1-i386 > $PATH_TMP/fedora-1-i386-default.html

echo "cp /var/www/html/testresults/fedora-1-i386/net_2_0/xml&png To mono.ximian.com"
scp /var/www/html/testresults/fedora-1-i386/net_2_0/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/fedora-1-i386/net_2_0/charts/.
scp /var/www/html/testresults/fedora-1-i386/net_2_0/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/fedora-1-i386/net_2_0/xml/.
echo "cp /var/www/html/testresults/fedora-1-i386/default/*.dat To mono.ximian.com"
scp /var/www/html/testresults/fedora-1-i386/default/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/fedora-1-i386/default/charts/.
scp /var/www/html/testresults/fedora-1-i386/default/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/fedora-1-i386/default/xml/.

echo "cp /var/www/html/testresults/fedora-1-i386-net_2_0.html To mono.ximian.com"
scp /var/www/html/fedora-1-i386-net_2_0.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
echo "cp /var/www/html/testresults/fedora-1-i386-default.html To mono.ximian.com"
scp /var/www/html/fedora-1-i386-default.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.


fi

if [ $1 -eq 1 ]
then
echo "generate the static page for suse"
#php generate-html.php --profile=net_2_0 --distro=suse-90-i586 > $PATH_TMP/suse-90-i586-net_2_0.html
#php generate-html.php --profile=default --distro=suse-90-i586 > $PATH_TMP/suse-90-i586-default.html

echo "cp /var/www/html/testresults/suse-90-i586/net_2_0/xml&png To mono.ximian.com"
scp /var/www/html/testresults/suse-90-i586/net_2_0/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/suse-90-i586/net_2_0/charts/.
scp /var/www/html/testresults/suse-90-i586/net_2_0/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/suse-90-i586/net_2_0/xml/.
echo "cp /var/www/html/testresults/suse-90-i586/default/xml&png To mono.ximian.com"
scp /var/www/html/testresults/suse-90-i586/default/charts/*.png sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/suse-90-i586/default/charts/.
scp /var/www/html/testresults/suse-90-i586/default/xml/*$DATE.xml sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/testresults/suse-90-i586/default/xml/.

echo "cp /var/www/html/suse-90-i586-net_2_0.html To mono.ximian.com"
scp /var/www/html/suse-90-i586-net_2_0.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
echo "cp /var/www/html/suse-90-i586-default.html To mono.ximian.com"
scp /var/www/html/suse-90-i586-default.html sachin@mono.ximian.com:/var/www/mono-website/go-mono/tests/.
fi


if [ $1 -gt 4 ] 
	then
	echo "Please enter the distro Id correctly"
fi	
