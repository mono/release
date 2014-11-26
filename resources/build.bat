@echo off

set MONO_VERSION=3.12.1
set MONO_FILES_DIR=.\mono-files

"%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe" MonoForWindows.wixproj /p:Configuration=Release /p:DefaultCompressionLevel=high