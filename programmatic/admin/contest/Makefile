#!/usr/bin/env make

include ../../Makefile.defs

all: contest usage

usage:
	@if [ ${DocumentRoot} = "" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot> target"; exit 1; fi

contest: gallery-edit.cgi

gallery-edit.cgi: gallery-edit.py

clean mrproper:
	/bin/rm -f gallery-edit.cgi

install: install-first

install-first: all
	install --mode=755 -d `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/contest
	install --mode=755 gallery-edit.cgi   `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/contest
