#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/gimp-print checkout gdevstp700/ChangeLog

${changelog} -f xhtml -i gdevstp700/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-print.html
${changelog} -f text -i gdevstp700/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-print.txt

/bin/rm -rf gdevstp700
