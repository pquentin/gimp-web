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

make PYTHON=${PYTHON} DocumentRoot=${INSTALLDIR} clean all programmatic install 2>&1 | tee make.out
ls -l ${INSTALLDIR}/var/spool/wgo-contest-current | tee -a make.out
echo done >> make.out


