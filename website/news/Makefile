
all: 
	-mkdir out
	mono /cvs/lb/lb.exe -c config.xml -p out
	rsync -pr -v --rsh=ssh out/archive \
	out/*.rss2 out/index.html out/all.html		\
	mono@segfault.cam.novell.com:public_html/news
	curl -o /dev/null http://www.mono-project.com/Main_Page?action=purge
