all: update-pages


update-template:
	curl -o TemplateExport.html http://www.mono-project.com/TemplateExport


update-pages:
	./generate-static ../forums_page/content.part.html ../forums_page/index.html Forums

push:
