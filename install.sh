#!/bin/sh -x

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
date >> ${log}
make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} clean webtools all programmatic install >> ${log}
make -C crontab all install 2>&1 >> ${log}
ls -l ${INSTALLDIR}/var/spool/wgo-contest-current  >> ${log}

