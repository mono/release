CSC=g:/windows/microsoft.net/framework/v1.1.4322/csc.exe $(CSCOPTIONS)
CSC2=g:/windows/microsoft.net/framework/v2.0.40607/csc.exe $(CSCOPTIONS)
CSCOPTIONS=-nologo -nowarn:0618
RUNTIME=

all: mono-api-info mono-api-diff

mono-api-diff: mono-api-diff.exe mono-api-diff2.exe

mono-api-info: mono-api-info.exe mono-api-info2.exe

mono-api-info.exe: mono-api-info.cs
	$(CSC) -out:$@ $<

mono-api-diff.exe: mono-api-diff.cs
	$(CSC) -out:$@ $<

mono-api-info2.exe: mono-api-info.cs
	$(CSC2) -out:$@ $<

mono-api-diff2.exe: mono-api-diff.cs
	$(CSC2) -out:$@ $<

infos: infos1 infos2

infos1: mono-api-info.exe assemblies-list.txt createinfos.sh
	./createinfos.sh 1.1

infos2: mono-api-info2.exe assemblies-list.txt createinfos.sh
	./createinfos.sh 2.0

clean:
	rm -f *.pdb *.mdb mono-api-info*.exe mono-api-diff*.exe *~

