#!/bin/sh

CVSDIR=`pwd`

if test "x$1" != x ; then
  INSTALLDIR=$1
else
  echo 2>&1 "Usage: install.sh DESTDIR"
  exit 1
fi

rsync -rlt --delete --exclude-from=$CVSDIR/install.exclude $CVSDIR/ $INSTALLDIR/
