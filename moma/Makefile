all:
	-rm -rf output
	gmcs -debug moma.cs && mono --debug moma.exe ~/Results/Fresh ~/Results/1.9 output > stats

push:
	(cd output; rsync -a . primates.ximian.com:public_html/momareports)
