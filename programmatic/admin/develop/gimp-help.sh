#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop

tmpdir=${DocumentRoot}/var/spool/gimp-unstable

mkdir ${tmpdir}
cd ${tmpdir}

nlogs=10
date=`date +%y-%m-%d`

title="Help ChangeLog - Last ${nlogs} Entries" # Don't show the date

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp-help/ChangeLog

${changelog} -f xhtml -n ${nlogs} -t "${title}" ${tmpdir}/gimp-help/ChangeLog > ${destdir}/help.html
${changelog} -f text  -n ${nlogs} -t "${title}" ${tmpdir}/gimp-help/ChangeLog > ${destdir}/help.txt

/bin/rm -rf ${tmpdir}
