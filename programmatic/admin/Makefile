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
	/bin/rm -f dot-forward dot-htaccess wgo-admin.css

install: install-first install-news install-contest

install-first: all
	install --owner=${OWNER} --mode=755 -d `python -c 'import wgo_config; print wgo_config.admin_path'`
	#install --owner=${OWNER} --mode=744 dot-htaccess ${DocumentRoot}/admin/.htaccess
	install --owner=${OWNER} --mode=744 dot-password `python -c 'import wgo_config; print wgo_config.admin_path'`/passwords
	install --owner=${OWNER} --mode=744 dot-forward   ${DocumentRoot}/.forward
	install --owner=${OWNER} admin-menu.inc          `python -c 'import wgo_config; print wgo_config.DocumentRoot_path'`/includes
	install --owner=${OWNER} wgo-admin.css           `python -c 'import wgo_config; print wgo_config.admin_path'`
	install --owner=${OWNER} wgo_admin.py            ${LIBDIR}
	install --owner=${OWNER} index.html              `python -c 'import wgo_config; print wgo_config.admin_path'`
	install --owner=${OWNER} howto.html              `python -c 'import wgo_config; print wgo_config.admin_path'`

install-news: news
	cd news && $(MAKE) install

install-contest: contest
	cd contest && $(MAKE) install
