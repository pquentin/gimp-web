#!/bin/sh

cd ${DocumentRoot}/var/spool


/usr/bin/cvs -d :pserver:anonymous@anoncvs.gnome.org:/cvs/gnome checkout gegl/ChangeLog
/usr/bin/head -100 gegl/ChangeLog > ${DocumentRoot}/about/ChangeLogs/ChangeLog-gegl-unstable.txt
/bin/rm -rf gegl/
