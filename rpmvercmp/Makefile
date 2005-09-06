

CC=gcc

all: rpmvercmp

rpmvercmp: rpmvercmp.c Makefile
	${CC} -o rpmvercmp -lpopt -lrpm -lrpmio -lrpmdb rpmvercmp.c

clean:
	rm -f rpmvercmp
