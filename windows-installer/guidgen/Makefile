all: guidgen

guidgen: guidgen.c Makefile
	gcc -g ./guidgen.c -lrpcrt4 -o guidgen -mno-cygwin -I/usr/include
	strip --strip-unneeded guidgen.exe

clean:
	rm -f guidgen.exe guidgen.exe.stackdump

