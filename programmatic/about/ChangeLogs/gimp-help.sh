#!/bin/sh -x

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp-help/ChangeLog

/usr/bin/head -100 gimp-help/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-help.txt
/bin/rm -rf gimp-help/
