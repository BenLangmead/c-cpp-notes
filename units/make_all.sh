#!/bin/sh

set -e

for i in */Makefile ; do
    make -C `dirname $i` $*
done
