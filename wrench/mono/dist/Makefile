include wrench.make

.configure:
	cd mono; \
	./autogen.sh

.make:
	cd mono; \
	make dist

.check:
	cd mono; \
	make distcheck
