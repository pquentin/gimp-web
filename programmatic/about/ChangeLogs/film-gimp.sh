#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/filmgimp checkout filmgimp/ChangeLog filmgimp/data/ChangeLog

${changelog} -f xhtml -i filmgimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp.html
${changelog} -f text -i filmgimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp.txt
${changelog} -f xhtml -i filmgimp/data/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp-data.html
${changelog} -f text -i filmgimp/data/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp-data.txt

/bin/rm -rf ${DocumentRoot}/var/spool/filmgimp
