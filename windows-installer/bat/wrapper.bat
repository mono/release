@ECHO OFF
SETLOCAL
SET PATH=C:\cygwin\tmp\install\bin;%PATH%
SET MONO_PATH=C:\cygwin\tmp\install\lib
SET MONO_CFG_DIR=C:\cygwin\tmp\install\etc
"C:\cygwin\tmp\install\lib\mono.exe" "C:\cygwin\tmp\install\lib\mono\1.0\@@MONO_WRAPPER@@.exe" %*
ENDLOCAL
