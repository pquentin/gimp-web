#!/bin/sh -x

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

log=${INSTALLDIR}/install.out

/bin/rm -f  ${log}
echo "contents of unix/"  >> ${log}

/bin/ls -l ${INSTALLDIR}/unix/  >> ${log}

make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} clean all 2>&1 >> ${log}

rsync -rlt --delete --exclude-from=$CVSDIR/install.exclude $CVSDIR/ $INSTALLDIR/

(cd programmatic ; make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} all install ) 2>&1 >> ${log}

(cd crontab ; make all install) 2>&1 >> ${log}

ls -l ${INSTALLDIR}/var/spool/wgo-contest-current  >> ${log}

