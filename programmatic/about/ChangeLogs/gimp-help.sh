#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp-help/ChangeLog

${changelog} -f xhtml -i gimp-help/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-help.html
${changelog} -f text -i gimp-help/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-help.txt

/bin/rm -rf gimp-help/
