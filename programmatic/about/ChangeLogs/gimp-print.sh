#!/bin/sh -x

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/gimp-print checkout gdevstp700/ChangeLog
/usr/bin/head -100 gdevstp700/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gimp-print.txt
/bin/rm -rf gdevstp700
