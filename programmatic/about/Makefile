#!/usr/bin/env make

include ../Makefile.defs
CSSFLAGS=-I../

all: usage ChangeLogs

usage:
	@if [ ${DocumentRoot} = "" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot> target"; exit 1; fi

ChangeLogs:
	cd ChangeLogs && $(MAKE)

clean mrproper:
	(cd ChangeLogs ; $(MAKE) clean)
	/bin/rm -f *.pyc *~

install: install-first install-ChangeLogs

install-first: all

install-ChangeLogs: ChangeLogs
	cd ChangeLogs && $(MAKE) install

install-contest: contest
	cd contest && $(MAKE) install
