#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gnome.org:/cvs/gnome checkout gegl/ChangeLog
${changelog} -f xhtml -i gegl/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gegl-unstable.html
${changelog} -f text -i gegl/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gegl-unstable.txt

/bin/rm -rf gegl/
