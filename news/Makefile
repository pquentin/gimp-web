#!/usr/bin/env make

OWNER=apache
INSTALLDIR=""

NEWSDIR=${INSTALLDIR}/news
LIBDIR=${NEWSDIR}/lib

%.cgi: %.py
	sed -e 's|__LIBDIR__|${LIBDIR}|g' -e 's|__NEWSDIR__|${NEWSDIR}|g' -e 's|__INSTALLDIR__|${INSTALLDIR}|g' $< > $@
	chmod a+rx $@

%: %.sh
	sed -e 's|__LIBDIR__|${LIBDIR}|g' -e 's|__NEWSDIR__|${NEWSDIR}|g' -e 's|__INSTALLDIR__|${INSTALLDIR}|g' $< > $@
	chmod a+rx $@

%: %.py
	sed -e 's|__LIBDIR__|${LIBDIR}|g' -e 's|__NEWSDIR__|${NEWSDIR}|g' -e 's|__INSTALLDIR__|${INSTALLDIR}|g' $< > $@
	chmod a+rx $@

all: usage config.py news-receiver news-batch.cgi news-edit-action.cgi news-edit.cgi news-index.cgi dot-forward dot-htaccess dot-password

usage:
	@if [ ${INSTALLDIR} = "" ]; then echo "USAGE: make INSTALLDIR=<DocumentRoot> install"; exit 1; fi

config.py: Makefile
	(echo "#!/usr/bin/env python"            ; \
	 echo "installdir='${INSTALLDIR}'"       ; \
	 echo "news_user_name='${OWNER}'"        ; \
	 echo "news_user_id=`id -u ${OWNER}`"    ; \
	 echo "news_directory='news/'"           ; \
	 echo "news_icon_path='icons/'"          ; \
	 echo "pending_queue='pending'"          ; \
	 echo "current_queue='current'"          ; \
	 echo "archive_queue='archive'"          ; \
	 echo "news_blotter='news-blotter'"      ; \
	 echo "news_permission=0644"             ; \
	 echo "debug = 0"                        ; \
	 echo "validator=0"                      ; \
	 echo "datetime_format = '%Y-%m-%d'"     ; \
	 echo "news_root=installdir + '/' + news_directory" \
	) > config.py

news-receiver: news-receiver.py

news-batch.cgi: news-batch.py

news-edit-action.cgi: news-edit-action.py

news-edit.cgi: news-edit.py

news-index.cgi: news-index.py

dot-forward: dot-forward.sh

dot-htaccess: dot-htaccess.sh

dot-password:
	touch dot-password

clean mrproper:
	/bin/rm -f *.pyc *.cgi news-receiver config.py dot-forward dot-htaccess

install: all

	install --owner=${OWNER} --mode=755 -d ${LIBDIR}
	install --owner=${OWNER} --mode=755 -d ${NEWSDIR}/include
	install --owner=${OWNER} --mode=755 -d ${NEWSDIR}/icons
	install --owner=${OWNER} --mode=755 -d ${NEWSDIR}/`python  -c 'import config; print config.pending_queue'`
	install --owner=${OWNER} --mode=755 -d ${NEWSDIR}/`python  -c 'import config; print config.current_queue'`
	install --owner=${OWNER} --mode=755 -d ${NEWSDIR}/`python  -c 'import config; print config.archive_queue'`

	install --owner=${OWNER} include/archive_footer.inc  ${NEWSDIR}/include/archive_footer.inc
		install --owner=${OWNER} include/archive_header.inc  ${NEWSDIR}/include/archive_header.inc
	install --owner=${OWNER} include/current_footer.inc  ${NEWSDIR}/include/current_footer.inc
	install --owner=${OWNER} include/current_header.inc  ${NEWSDIR}/include/current_header.inc
	install --owner=${OWNER} include/news_menu.inc       ${NEWSDIR}/include/news_menu.inc
	install --owner=${OWNER} include/pending_footer.inc  ${NEWSDIR}/include/pending_footer.inc
	install --owner=${OWNER} include/pending_header.inc  ${NEWSDIR}/include/pending_header.inc

	install --owner=${OWNER} icons/options.txt ${NEWSDIR}/icons/options.txt
	install --owner=${OWNER} icons/gimp_code.png ${NEWSDIR}/icons/gimp_code.png
	install --owner=${OWNER} icons/gimp_construction.png ${NEWSDIR}/icons/gimp_construction.png

	install --owner=${OWNER} --mode=744 dot-forward ${INSTALLDIR}/.forward
	install --owner=${OWNER} --mode=744 dot-htaccess ${NEWSDIR}/.htaccess
	install --owner=${OWNER} --mode=744 dot-password ${NEWSDIR}/.password
	install --owner=${OWNER} config.py ${LIBDIR}
	install --owner=${OWNER} xhtml.py ${LIBDIR}
	install --owner=${OWNER} wgo_news.py ${LIBDIR}
	install --owner=${OWNER} news-receiver ${NEWSDIR}

	install --owner=${OWNER} news.css ${NEWSDIR}
	install --owner=${OWNER} index.html ${NEWSDIR}
	install --owner=${OWNER} news-batch.cgi ${NEWSDIR}
	install --owner=${OWNER} news-edit-action.cgi ${NEWSDIR}
	install --owner=${OWNER} news-edit.cgi ${NEWSDIR}
	install --owner=${OWNER} news-index.cgi ${NEWSDIR}

