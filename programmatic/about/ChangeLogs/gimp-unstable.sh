#!/bin/sh -x

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@anoncvs.gimp.org:/cvs/gnome checkout gimp/ChangeLog

/usr/bin/head -100 gimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-unstable.txt
/bin/rm -rf gimp/
