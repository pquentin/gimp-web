#!/usr/bin/env make

include ../../Makefile.defs

all: usage ChangeLog changelog-xhtml.css changelog-xhtml-mono.css

usage:


ChangeLog: ChangeLog-xhtml.cgi gimp-unstable gegl-unstable gimp-help

gimp-unstable: gimp-unstable.sh

gegl-unstable: gegl-unstable.sh

gimp-help: gimp-help.sh

ChangeLog-xhtml.cgi: ChangeLog-xhtml.py

changelog-xhtml.css: changelog-xhtml.cPP

changelog-xhtml-mono.css: changelog-xhtml-mono.cPP

clean mrproper:
	/bin/rm -f *.cgi *~ changelog-xhtml.css changelog-xhtml-mono.css gegl-unstable gimp-unstable gimp-help

install: install-first

install-first: all
	#install --mode=755 -d                  `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=755 ChangeLog-xhtml.cgi `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=755 gimp-unstable       `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=755 gegl-unstable       `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=755 gimp-help           `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=644 changelog-xhtml.css `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
	install --mode=644 changelog-xhtml-mono.css `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/about/ChangeLogs
