#!/bin/bash

set -e

for i in */*.cppmd ; do
    pushd `dirname $i`
    make -f ../Makefile.slides clean
    popd
done
