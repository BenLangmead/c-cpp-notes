#!/bin/sh

for i in */Makefile ; do
    make -C `dirname $i` $*
done
