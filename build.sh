#!/bin/bash
#set -xv

if [ $# -eq 0 ] then
    echo "Version number is needed!"
    echo "Usage: ./build.sh version"
    exit 0
fi

if [ ! -d build ]; then
    mkdir build
    mkdir build/pipic
fi

rm -rfv build/pipic/*
cp -r src/* build/pipic/
cd build
rm pipic/*.pyc
rm pipic/pics/pic_*
#tar -czvf ../bkp/pipic.$1.$(date -d "today" +"%Y%m%d_%H%M").tar.gz pipic
rm pipic/parameters.ini
cp pipic/parameters.dpl pipic/parameters.ini
tar -czvf pipic.$1.$(date -d "today" +"%Y%m%d_%H%M").tar.gz pipic
#cp  pipic.$1.$(date -d "today" +"%Y%m%d_%H%M").tar.gz  ~/www/pipic/build/
cd ..



