#!/usr/bin/env make

include ../Makefile.defs
CSSFLAGS=-I../

# ChangeLogs should not be built because a different mechanism will be used
# in the future.
#all: usage ChangeLogs
all: usage

usage:
	@if [ ${DocumentRoot} = "" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot> target"; exit 1; fi

ChangeLogs:
	cd ChangeLogs && $(MAKE)

clean mrproper:
	(cd ChangeLogs ; $(MAKE) clean)
	/bin/rm -f *.pyc *~

# ChangeLogs should not be installed because a different mechanism will be used
# in the future.
# install: install-first install-ChangeLogs
install:

install-first: all

install-ChangeLogs: ChangeLogs
	cd ChangeLogs && $(MAKE) install

install-contest: contest
	cd contest && $(MAKE) install
