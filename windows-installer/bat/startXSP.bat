@echo off
call @@DOS_MONO_INST_DIR@@\bin\setmonopath.bat
cd /D @@DOS_MONO_INST_DIR@@\lib\xsp\test
xsp --root . --port 8089 --applications /:.
