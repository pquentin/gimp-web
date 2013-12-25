include ../Makefile.defs

.PHONY: all clean install

PYTHONPATH := ../

all: mirrors.xhtml

MIRRORS: MIRRORS.in
	grep -v '^#[^#]' MIRRORS.in | sed '/^$$/N;/^\n$$/D' > MIRRORS

mirrors.xhtml: MIRRORS
	${PYTHON} mirrorfmt.py MIRRORS > mirrors.xhtml

clean:
	/bin/rm -f mirrors.xhtml

install: mirrors.xhtml
	-mkdir -p `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/downloads
	install -m 644 mirrors.xhtml `${PYTHON} -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/downloads/mirrors.xhtml

#install-ftp: MIRRORS
#	-mkdir -p `${PYTHON} -c 'import wgo_config; print wgo_config.FtpRoot_path'`/gimp
#	install -m 644 MIRRORS `${PYTHON} -c 'import wgo_config; print wgo_config.FtpRoot_path'`/gimp/MIRRORS