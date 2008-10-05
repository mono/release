all: update-pages


update-template:
	curl -o TemplateExport.html http://www.mono-project.com/TemplateExport


update-pages:
	./generate-static ../forums_page/index.html Forums ../forums_page/content.part.html

update-news-template:
	./generate-static /cvs/website/template News /cvs/website/body.part.html /cvs/website/body.toc.html 

push:
