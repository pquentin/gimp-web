#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop
tmpdir=${DocumentRoot}/var/spool/gegl-unstable

mkdir ${tmpdir}
cd ${tmpdir}

nlogs=10
date=`date +%y-%m-%d`

title="Help ChangeLog - Last ${nlogs} Entries" # Don't show the date (for some reason)

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gnome.org:/cvs/gnome checkout gegl/ChangeLog
${changelog} -f xhtml -n ${nlogs} -t "${title}" ${tmpdir}/gegl/ChangeLog > ${destdir}/gegl.html
${changelog} -f text  -n ${nlogs} -t "${title}" ${tmpdir}/gegl/ChangeLog > ${destdir}/gegl.txt

/bin/rm -rf ${tmpdir}
