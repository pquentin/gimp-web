#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop

cd ${DocumentRoot}/var/spool

nlogs=10
date=`date +%y-%m-%d`

title="FilmGIMP ChangeLog - Last ${nlogs} Entries" # Don't show the date (for some reason)

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/filmgimp checkout filmgimp/ChangeLog filmgimp/data/ChangeLog

${changelog} -f xhtml -n ${nlogs} -t "${title}" -i filmgimp/ChangeLog > ${destdir}/film.html
${changelog} -f text  -n ${nlogs} -t "${title}" -i filmgimp/ChangeLog > ${destdir}/file.txt

/bin/rm -rf ${DocumentRoot}/var/spool/filmgimp
