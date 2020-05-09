# C & C++ programming notes

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

* Author: Ben Langmead

These are lecture notes and example code for teaching C &amp; C++.  The slides themselves are written in a custom "runnable Markdown" dialect for C/C++.  These files have extension `.cppmd`.  The script that "compiles" `.cppmd` files is `units/cppmd_render.py`.  This script:

* Generates C/C++ source files based on specially-formatted comments in the Markdown (`<!---cppmd-file ... -->`)
* Runs shell commands based on specially-formatted comments in the Markdown (`<!---cppmd-shell ... -->`), often in order to compile and run the source code
    * Possibly integrates the output from the shell back into the slides, so that output can be included in final rendered doc
* Uses `pandoc` & `beamer` to render a PDF

Outputs consist of (a) a PDF of the slides, (b) source files for all the examples.

All the shell commands are run within a Docker image.  We use this image from Docker Hub:

* [`benlangmead/fedora-cpp-slides`](https://hub.docker.com/r/benlangmead/fedora-cpp-slides/)

And the corresponding `Dockerfile` and scripts used to build/pull/push are available in the `docker` subdirectory.  The base image is Fedora 27.  The most relevant software versions are:

```
gcc-7.2.1
g++-7.2.1
gdb: Fedora 8.0.1-33.fc27
valgrind-3.13.0
git v2.14.3
```

### Philosophy

The reality of programming in C and C++ can seem divorced from the conceptual discussions in texts.  In these notes, explaining concepts is always intertwined with showing examples.  When examples are shown, I give exact code and exact command lines, executed in a predictable environment, so that students can recreate the conditions exactly.  I show examples that do work and others that don't.  The idea is never to stray too far from a code example.
