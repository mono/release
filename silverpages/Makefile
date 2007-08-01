all: config mscorlib.dll.source 
	echo "Use make cycle (best), make regen, make push or make update-source"

config:
	@if test -f config; then echo OK; else echo Please run configure; exit 1; fi

mscorlib.dll.source:
	wget http://mono.ximian.com/masterinfos/sl11rjuly-full.tar.gz
	tar xzvf sl11rjuly-full.tar.gz

cycle:
	make regen
	make push

regen:
	sh make-ours
	sh make-list

update-source:
	sh make-source

push:
	rsync -a output/* primates.ximian.com:public_html/silverpages