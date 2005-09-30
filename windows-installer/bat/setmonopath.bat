@echo off
echo Mono version @@MONO_VERSION@@ Build @@MONO_REVISION@@
echo Prepending '@@DOS_MONO_INST_DIR@@\bin' to PATH
PATH=@@DOS_MONO_INST_DIR@@\bin;%PATH%

