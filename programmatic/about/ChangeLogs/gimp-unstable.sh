#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp/ChangeLog
${changelog} -f xhtml -i gimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-unstable.html
${changelog} -f text -i gimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-unstable.txt

/bin/rm -rf gimp/
