#!/bin/bash

set -e

for i in */Makefile.slides ; do
    pushd `dirname $i`
    ../build.sh
    popd
done
