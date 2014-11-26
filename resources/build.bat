@echo off

set MONO_VERSION=3.12.1
set MONO_FILES_DIR=..\tmp\mono

"%windir%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe" %~dp0\MonoForWindows.wixproj /p:Configuration=Release /p:DefaultCompressionLevel=high
