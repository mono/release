@ECHO OFF
SETLOCAL
SET SIGNBASE=C:\CodeSigning\SignTools
SET PATH=%SIGNBASE%\nss\bin;%PATH%

ECHO Signing Mozilla Plugin
SET CERT="Novell"
SET DB=%SIGNBASE%\nss\privkey
SET NAME="novell-moonlight"

FOR %%V IN ("1.0" "2.0") DO (
	FOR %%A IN ("i586" "x86_64") DO (
		signtool -d %DB% -k %CERT% -p %1 -X -Z %NAME%-%%V-%%A.xpi -c 9 %NAME%-%%V-%%A
	)
)

ENDLOCAL
PAUSE
