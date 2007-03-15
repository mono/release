#!/bin/sh

: ${prefix=/usr/local}
: ${exec_prefix=${prefix}}
: ${libdir=${exec_prefix}/lib}

mkdir -p $libdir/mono/1.0
mkdir -p $libdir/mono/2.0

for i in 1.0/*.dll
do
  echo MONO_PATH=./1.0 mono ./1.0/gacutil.exe /i $i /f /package 1.0 /root ${libdir}
  MONO_PATH=./1.0 mono ./1.0/gacutil.exe /i $i /f /package 1.0 /root ${libdir}
done

for i in 1.0/*.exe
do
  echo install $i $libdir/mono/1.0
  install $i $libdir/mono/1.0
done


for i in 2.0/*.dll
do
  echo MONO_PATH=./2.0 mono ./1.0/gacutil.exe /i $i /f /package 2.0 /root ${libdir}
  MONO_PATH=./2.0 mono ./1.0/gacutil.exe /i $i /f /package 2.0 /root ${libdir}
done

for i in 2.0/*.exe
do
  echo install $i $libdir/mono/2.0
  install $i $libdir/mono/2.0
done
