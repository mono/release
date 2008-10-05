all: update-pages

push:
	rsync -a ../forums_page/* mono-web@www.go-mono.com:go-mono/forums

update-template:
	curl -o TemplateExport.html http://www.mono-project.com/TemplateExport

update-pages:
	./generate-static ../forums_page/index.html Forums ../forums_page/content.part.html
	./generate-static ../download_page/download.html Download ../download_page/download.part.html NONE ../download_page/download.head.html 

update-news-template:
	./generate-static /cvs/website/template News /cvs/website/body.part.html /cvs/website/toc.part.html 

push:
