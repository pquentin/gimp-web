#!/usr/bin/env make

include ../Makefile.defs

all: usage ChangeLog changelog-xhtml.css changelog-xhtml-mono.css

usage:

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
	/bin/rm -f *.cgi *~ changelog-xhtml.css changelog-xhtml-mono.css changelog-cron gimp-unstable gegl-unstable gimp-help gimp-print film-gimp

install: install-first

install-first: all
	sed -e 's|$${PYTHON}|${PYTHON}|g' -e 's|$${LIBDIR}|${LIBDIR}|g' ChangeLog.py        > ${LIBDIR}/ChangeLog.py && chmod 755 ${LIBDIR}/ChangeLog.py
	install -m 755 gimp-unstable   \
	                   gegl-unstable   \
	                   gimp-help       \
	                   gimp-print      \
	                   film-gimp       \
	                   changelog-cron           `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/develop
	install -m 644 changelog-xhtml.css      `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/develop
	install -m 644 changelog-xhtml-mono.css `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/develop
