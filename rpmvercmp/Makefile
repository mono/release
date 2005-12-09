CC=gcc

all: rpmvercmp

rpmvercmp: rpmvercmp.c Makefile
	${CC} `pkg-config --libs --cflags glib-2.0` -I/opt/gnome/include -lpopt -lrpm -lrpmio -lrpmdb  -o rpmvercmp rpmvercmp.c

clean:
	rm -f rpmvercmp
