#!/bin/sh -x

changelog=${LIBDIR}/ChangeLog.py
destdir=${DocumentRoot}/develop

cd ${DocumentRoot}/var/spool

nlogs=10
date=`date +%y-%m-%d`

title="Help ChangeLog - Last ${nlogs} Entries" # Don't show the date (for some reason)

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp-help/ChangeLog

${changelog} -f xhtml -n ${nlogs} -t "${title}" -i gimp-help/ChangeLog > ${destdir}/help.html
${changelog} -f text  -n ${nlogs} -t "${title}" -i gimp-help/ChangeLog > ${destdir}/help.txt

/bin/rm -rf gimp-help/
