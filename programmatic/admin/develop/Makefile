#!/usr/bin/env make

include ../../Makefile.defs

all: develop usage ChangeLog

usage:
	@if [ ${DocumentRoot} = "" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot> target"; exit 1; fi

develop: changelogs.cgi

changelogs.cgi: changelogs.py

ChangeLog: changelog-cron gimp-unstable gegl-unstable gimp-help gimp-print film-gimp

gimp-unstable: gimp-unstable.sh
gegl-unstable: gegl-unstable.sh
gimp-help: gimp-help.sh
gimp-print: gimp-print.sh
film-gimp: film-gimp.sh
changelog-cron: changelog-cron.sh

changelog-xhtml.css: changelog-xhtml.cPP

changelog-xhtml-mono.css: changelog-xhtml-mono.cPP

clean mrproper:
	/bin/rm -f *.cgi *~

install: install-first

install-first: all
	install --mode=755 -d `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/develop
	install --mode=755 changelogs.cgi `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/develop

	install --mode=755 gimp-unstable   \
	                   gegl-unstable   \
	                   gimp-help       \
	                   gimp-print      \
	                   film-gimp       \
	                   changelog-cron `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/develop
