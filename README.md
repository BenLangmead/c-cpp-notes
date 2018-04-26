# C & C++ programming notes

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

* Author: Ben Langmead

These are lecture notes and example code for teaching C &amp; C++.  The slides themselves are written in a custom "runnable Markdown" dialect for C/C++.  These files have extension `.cppmd`.  The script that "compiles" `.cppmd` files is `units/cppmd_render.py`.  This script:

* Generates C/C++ source files based on specially-formatted comments in the Markdown (`<!---cppmd-file ... -->`)
* Runs shell commands based on specially-formatted comments in the Markdown (`<!---cppmd-shell ... -->`), often in order to compile and run the source code
    * Possibly integrates the output from the shell back into the slides, so that output can be included in final rendered doc
* Uses `pandoc` & `beamer` to render a PDF

Outputs consist of (a) a PDF of the slides, (b) source files for all the examples.

All the shel commands are run within a Docker image.  We use this image from Docker Hub: 

* [`benlangmead/fedora-cpp-slides`](https://hub.docker.com/r/benlangmead/fedora-cpp-slides/)

