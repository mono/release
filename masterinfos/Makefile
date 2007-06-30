CSC=$(WINDIR)/microsoft.net/framework/v1.1.4322/csc.exe $(CSCOPTIONS)
CSC2=$(WINDIR)/microsoft.net/framework/v2.0.50727/csc.exe $(CSCOPTIONS) \
	-define:NET_2_0
CSCOPTIONS=-nologo -nowarn:0618
RUNTIME=

all: mono-api-info

mono-api-info: mono-api-info.exe mono-api-info2.exe

mono-api-info.exe: mono-api-info.cs
	$(CSC) -out:$@ $<

mono-api-info2.exe: mono-api-info.cs
	$(CSC2) -out:$@ $<

infos: infos1 infos2

infos1: mono-api-info.exe assemblies-list.txt createinfos.sh
	./createinfos.sh 1.1 assemblies-list.txt

infos2: mono-api-info2.exe assemblies-list-2.txt createinfos.sh
	./createinfos.sh 2.0 assemblies-list-2.txt

clean:
	rm -f *.pdb *.mdb mono-api-info*.exe *~

