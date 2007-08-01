all:
	echo "Use make cycle (best), make regen, make push or make update-source"

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