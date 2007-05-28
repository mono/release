all:
	-rm output/*
	gmcs -debug moma.cs && mono --debug moma.exe ~/Results/Fresh ~/Results/1.2.4 output

push:
	(cd output; rsync -a . primates.ximian.com:public_html/momareports)