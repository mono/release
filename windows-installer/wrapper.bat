@ECHO OFF
SETLOCAL
SET PATH=C:\mono\Mono-1.1.8.3\bin;%PATH%
SET MONO_PATH=C:\mono\Mono-1.1.8.3\lib
SET MONO_CFG_DIR=C:\mono\Mono-1.1.8.3\etc
"C:\mono\Mono-1.1.8.3\lib\mono.exe" "C:\mono\Mono-1.1.8.3\lib\mono\1.0\mcs.exe" %*
ENDLOCAL
