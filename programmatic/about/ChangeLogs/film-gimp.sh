#!/bin/sh -x

cd ${DocumentRoot}/var/spool

/usr/bin/cvs -d :pserver:anonymous@cvs.sourceforge.net:/cvsroot/filmgimp checkout filmgimp/ChangeLog filmgimp/data/ChangeLog
/usr/bin/head -100 filmgimp/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp.txt
/usr/bin/head -100 filmgimp/data/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-film-gimp-data.txt
/bin/rm -rf ${DocumentRoot}/var/spool/filmgimp
