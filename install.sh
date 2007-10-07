#!/bin/bash

if [ ! -f install.config ]; then
  echo ""
  echo "Install procedure requires install.config file."
  echo "See install.config.sample for an example."
  echo ""
  exit 1
fi

source install.config

if [ "x${HTDOCS_DIR}" = "x" ]; then
  echo ""
  echo "HTDOCS_DIR must be specified in install.config."
  echo "See install.config.sample for an example."
  echo ""
  exit 1
fi

if [ "x${PYTHON}" = "x" ]; then
  if [ "x`which python2.4`" != "x" ]; then
    PYTHON=python2.4
  else
    if [ "x`which python2.3`" != "x" ]; then
      PYTHON=python2.3
    else
      if [ "x`which python2.2`" != "x" ]; then
        PYTHON=python2.2
      else
        PYTHON=python
      fi
    fi
  fi
fi

if [ -z "$MAKE" ]; then
  MAKE=make
fi

${MAKE} PYTHON=${PYTHON} DocumentRoot=${HTDOCS_DIR} clean all programmatic install 2>&1 | tee make.out
echo done >> make.out

