CC=gcc
SWIG=swig

all: rpmvercmp _rpmvercmp.so

rpmvercmp: rpmvercmp.c Makefile
	${CC} -Wall `pkg-config --libs --cflags glib-2.0` -I/opt/gnome/include -lpopt -lrpm -lrpmio -lrpmdb  -o rpmvercmp rpmvercmp.c

_rpmvercmp.so: rpmvercmp.c rpmvercmp.i Makefile
	${SWIG} -python rpmvercmp.i 
	gcc -fpic -c rpmvercmp.c rpmvercmp_wrap.c -I/usr/include/python/ `pkg-config --cflags glib-2.0` -I/opt/gnome/include
	gcc -shared rpmvercmp.o rpmvercmp_wrap.o -o _rpmvercmp.so `pkg-config --libs glib-2.0` -lrpm

clean:
	rm -f rpmvercmp
	rm -f *.o *.so
