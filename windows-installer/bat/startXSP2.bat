@echo off
call C:\cygwin\tmp\install\bin\setmonopath.bat
cd /D C:\cygwin\tmp\install\share\doc\xsp\test
xsp2 --root . --port 8089 --applications /:.
