#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
#
# Copyright (C) 2003 Helvetix Victorinox, a pseudonym,
# Mountain View, California
# 
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
#
import sys
import os
import re
import string
import getopt

import apache_ssi

def usage(name):
  print "Usage:", name, "[OPTION] [FILE]..."
  print "Preprocess FILE(s), performing limited file include and variable substitution."
  print "Akin to the Apache SSI facility."
  print
  print "  -h, --help                This message"
  print "  -o, --output=<file>       Output to file <file>"
  print "  -D <attr>=<value>         Define variable <attr> to value <value>"
  print "  -r <directory>            Directory pathname for include files"
  print "  -DocumentRoot=<directory> Directory pathname for include files"
  print "  -v                        Print version and exit"
  return
  
    
if __name__ == "__main__":

  ssi = apache_ssi.processor()

  fpout = sys.stdout
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:D:vr:M", ["help", "output=", "version", "DocumentRoot=", "M"])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(2)
    pass
  
  dependency_list = False
  
  for o, a in opts:
    if o in ("-h", "--help"):
      usage(sys.argv[0])
      sys.exit()
      pass
    
    if o in ("-o", "--output"):
      fpout = open(a, "w")
      pass

    if o in ("-r", "--DocumentRoot"):
      ssi.document_root = a + "/"
      pass

    if o in ("-M", "--M"):
      dependency_list = True
      pass
    
    if o in ("-v", "--version"):
      print ssi.Version
      sys.exit()
      pass

    if o in ("-D", "--define"):
      ssi.variables.update(dict(map(lambda b: filter(lambda a: a != '', b),
                                    re.findall("(\w+)=\"([^\"]*)\"\s*|(\w+)=([^\s]*)\s*", a))))
      pass
    pass

  if dependency_list:
    print >>fpout, map(lambda a: ssi.depend(a), args)
  else:
    print >>fpout, string.join(map(lambda a: ssi.parse(a), args))
    pass

  pass
