#!/bin/sh

CVSDIR=`pwd`

if test "x$1" != x ; then
  INSTALLDIR=$1
else
  echo 2>&1 "Usage: install.sh DESTDIR"
  exit 1
fi

rsync -rlt --delete --delete-excluded --exclude-from=$CVSDIR/install.exclude $CVSDIR/ $INSTALLDIR/
(cd programmatic ; make DocumentRoot=${INSTALLDIR} all install )
