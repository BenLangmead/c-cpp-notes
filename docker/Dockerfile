# Author: Ben Langmead
#   Date: 1/21/2018

FROM fedora:27

RUN yum install -y valgrind
RUN yum install -y gdb
RUN yum install -y gcc
RUN yum install -y gcc-c++
RUN yum install -y emacs-nox
RUN yum install -y git

RUN dnf -y debuginfo-install glibc-2.26-15.fc27.x86_64