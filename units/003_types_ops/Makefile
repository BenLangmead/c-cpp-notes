#!gmake

CPPMD=python ../cppmd_render.py

all: $(basename $(wildcard *.cppmd)).pdf

%.pdf: %.cppmd
	$(CPPMD) --prefix $(@:%.pdf=%) --beamer-theme=metropolis --force < $<

.PHONY: clean
clean:
	rm -f *.pdf *.md *.c *.cpp *.h *.hpp a.out *~
