#!/bin/sh

mkdir -p full

FILES=$(ls */*.cppmd | sort)
cat $FILES > full/full.cppmd

cd full && ../build.sh && cd ..
