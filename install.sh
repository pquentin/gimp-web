#!/bin/sh

CVSDIR=`pwd`

if test "x$1" != x ; then
  INSTALLDIR=$1
else
  echo 2>&1 "Usage: install.sh DESTDIR"
  exit 1
fi

if test -z "$PYTHON" ; then
  PYTHON=python
fi

rm -f  ${INSTALLDIR}/install.out
ls -l unix/  >> ${INSTALLDIR}/install.out

make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} clean all install 2>&1 >> ${INSTALLDIR}/install.out

rsync -rlt --delete --exclude-from=$CVSDIR/install.exclude $CVSDIR/ $INSTALLDIR/

(cd programmatic ; make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} all install ) 2>&1 >> ${INSTALLDIR}/install.out

(cd crontab ; make all install) 2>&1 >> ${INSTALLDIR}/install.out

ls -l ${INSTALLDIR}/var/spool/wgo-contest-current  >> ${INSTALLDIR}/install.out

