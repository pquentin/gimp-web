#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
# Copyright (C) 2002, 2003  Helvetix Victorinox, a pseudonym
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import errno
import fcntl
import getopt
import os
import re
import sha
import stat
import string
import sys
import time
import types

sys.path = ['${SRCDIR}'] + sys.path

import wgo

def usage():
  return

if __name__ == "__main__":

  try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:", ["help", "attribute="])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(1)
    pass

  for o, a in opts:
    if o in ("-h", "--help"):
      usage(sys.argv[0])
      sys.exit(0)
      pass

    if o in ("-a", "--attribute"):
      print eval(a)
      pass
    pass
  

  sys.exit(0)
    

