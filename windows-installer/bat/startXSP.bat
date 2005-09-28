@echo off
call C:\cygwin\tmp\install\bin\setmonopath.bat
cd /D C:\cygwin\tmp\install\share\doc\xsp\test
xsp --root . --port 8089 --applications /:.
