#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop
tmpdir=${DocumentRoot}/var/spool/gimp-print

mkdir ${tmpdir}
cd ${tmpdir}

nlogs=10
date=`date +%y-%m-%d`

title="Print ChangeLog - Last ${nlogs} Entries" # Don't show the date (for some reason)

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/gimp-print checkout gdevstp700/ChangeLog # ??

${changelog} -f xhtml -n ${nlogs} -t "${title}" -i gdevstp700/ChangeLog > ${destdir}/print.html
${changelog} -f text  -n ${nlogs} -t "${title}" -i gdevstp700/ChangeLog > ${destdir}/print.txt

/bin/rm -rf ${tmpdir}
