#!/usr/bin/env make

include ../Makefile.defs
CSSFLAGS=-I../

all: usage admin news contest

usage:
	@if [ ${DocumentRoot} = "" ]; then echo "USAGE: make DocumentRoot=<DocumentRoot> target"; exit 1; fi

admin: dot-forward dot-htaccess dot-password wgo-admin.css

news:
	cd news && $(MAKE) all

contest:
	cd contest && $(MAKE) all

wgo-admin.css: wgo-admin.cpp

dot-forward: dot-forward.sh

dot-htaccess: dot-htaccess.sh

dot-password:
	touch dot-password

clean mrproper:
	cd news && $(MAKE) clean
	cd contest && $(MAKE) clean
	/bin/rm -f dot-forward dot-htaccess wgo-admin.css *~

install: install-first install-news install-contest

install-first: all
	install --mode=744 dot-forward   ${DocumentRoot}/.forward

	install wgo_admin.py            ${LIBDIR}

	install --mode=755 -d `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`
	#install --mode=744 dot-htaccess ${DocumentRoot}/admin/.htaccess
	install --mode=744 dot-password `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`/passwords

	install wgo-admin.css           `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`
	install howto.html              `${PYTHON} -c 'import wgo_config; print wgo_config.admin_path'`

install-news: news
	cd news && $(MAKE) install

install-contest: contest
	cd contest && $(MAKE) install
