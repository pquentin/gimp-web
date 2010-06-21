include ../Makefile.defs

.PHONY: all clean install

all: mirrors.xhtml

mirrors.xhtml: MIRRORS
	${PYTHON} mirrorfmt.py MIRRORS > mirrors.xhtml

clean:
	/bin/rm -f mirrors.xhtml

install: mirrors.xhtml
	-mkdir `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/downloads
	install -m 644 mirrors.xhtml `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/downloads/mirrors.xhtml
