
all: 
	mono /cvs/lb/lb.exe
	chmod 644 archive/*/*.html
	chmod 644 *html *rss2 
	rsync -pr -v --rsh=ssh texts archive \
	*.rss2 index.html all.html		\
	mono@segfault.cam.novell.com:public_html/newstouch

