@ECHO OFF
SETLOCAL

IF "%1" == "" GOTO PROMPTPASS
SET PWD=%1
GOTO RUN

:PROMPTPASS
ECHO Enter code signing password:
SET /p PWD=

:RUN

SET SIGNBASE=C:\CodeSigning\SignTools
SET PATH=%SIGNBASE%\nss\bin;%PATH%

ECHO Signing Mozilla Plugin
SET CERT="Novell"
SET DB=%SIGNBASE%\nss\privkey
SET NAME="novell-moonlight"

FOR %%V IN ("1.0" "2.0") DO (
	FOR %%A IN ("i586" "x86_64") DO (
		%SIGNBASE%\nss\bin\signtool.exe -d %DB% -k %CERT% -p %PWD% -X -Z %NAME%-%%V-%%A.xpi -c 9 %NAME%-%%V-%%A
	)
)

ENDLOCAL
PAUSE
