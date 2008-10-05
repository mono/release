all: update-pages

push:
	rsync -a ../forums_page/* mono-web@www.go-mono.com:go-mono/forums
	rsync -a ../download_page/* mono-web@www.go-mono.com:go-mono/mono-downloads
	rsync -a ../irc_page/* mono-web@www.go-mono.com:go-mono/chat
	rsync -a --delete ../contact/* mono-web@www.go-mono.com:go-mono/archive/contact

update-template:
	curl -o TemplateExport.html http://www.mono-project.com/TemplateExport

update-pages: update-news-template
	./generate-static ../forums_page/index.html Forums ../forums_page/content.part.html
	./generate-static ../download_page/download.html Download ../download_page/download.part.html NONE ../download_page/download.head.html 
	./generate-static ../irc_page/index.html Chat ../irc_page/index.part.html NONE ../irc_page/index.head.html
	./generate-static ../contact/index.aspx Contact ../contact/index.part.html NONE ../contact/index.head.html ../contact/index.prologue.html

update-news-template:
	./generate-static /cvs/website/template News /cvs/website/body.part.html /cvs/website/toc.part.html 

