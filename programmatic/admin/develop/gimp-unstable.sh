#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop
nlogs=10
date=`date +%y-%m-%d`
tmpdir=${DocumentRoot}/var/spool/gimp-unstable

mkdir ${tmpdir}
cd ${tmpdir}

title="Unstable ChangeLog - Last ${nlogs} Entries (snapshot ${date})"

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp/ChangeLog
${changelog} -f xhtml -n ${nlogs} -t "${title}" ${tmpdir}/gimp/ChangeLog > ${destdir}/unstable.html
${changelog} -f text  -n ${nlogs} -t "${title}" ${tmpdir}/gimp/ChangeLog > ${destdir}/unstable.txt

/bin/rm -rf ${tmpdir}
