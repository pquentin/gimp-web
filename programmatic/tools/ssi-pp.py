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

Version = """SSI Preprocessor, version $Revision$
Copyright (C) 2003 Helvetix Victorinox, a pseudonym.
This is free software; see the source code for copying conditions.
There is ABSOLUTELY NO WARRANTY; not even for MERCHANTIBILITY or
FITNESS FOR A PARTICULAR PURPOSE.

Report bugs to: <HELVETIX@Mysterious.ORG>"""

DocumentRoot="./"

Variables = { }

def var_rvalue(name):
  s = ""

  _last = 0
  for l in re.finditer("\${(\w+)}|\$(\w+)", name):
    s += name[_last:l.start()]
    v = filter(lambda x: x != None, l.groups())
    v = v[0]
    s += Variables[v]
    _last = l.end()
    pass

  s += name[_last:]
  return (s)


def attr_parse(s):
  avlist = { }
  map(lambda x: avlist.update({x[0]: x[1]}), re.findall("(\w+)=\"([^\"]*)\"\s*", s))
  return (avlist)


def process(filename, fpout):
  _last = 0

  if filename != '-':
    fp = open(filename, "r")
    body = fp.read()
    fp.close()
  else:
    body = sys.stdin.read()
    pass


  for ssi in re.finditer("<!--#(\w+)\s+(.*)\s*-->", body):
    fpout.write(body[_last:ssi.start()])

    element = ssi.expand("\\1")
    attrs = attr_parse(ssi.expand("\\2"))

    if element == "include":
      process(DocumentRoot + attrs["virtual"], fpout)
    elif element == "set":
      value = var_rvalue(attrs["value"])
      Variables.update({attrs["var"]: value})
    elif element == "echo":
      fpout.write(var_rvalue(attrs["var"]))
      pass
    else:
      print >>sys.stderr, "Unsupported SSI element", element, "in", body[ssi.start():ssi.end()]
      sys.exit(1)
      return

    _last = ssi.end()
    pass
  
  fpout.write(body[_last:])
  return


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
  
  Variables.update(os.environ)

  fpout = sys.stdout
  
  try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:D:vr:", ["help", "output=", "version", "DocumentRoot="])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(2)
    pass
  
  output = None
  for o, a in opts:
    if o in ("-h", "--help"):
      usage(sys.argv[0])
      sys.exit()
      pass
    
    if o in ("-o", "--output"):
      fpout = open(a, "w")
      pass

    if o in ("-r", "--DocumentRoot"):
      DocumentRoot = a + "/"
      pass

    if o in ("-v", "--version"):
      print Version
      sys.exit()
      pass

    if o in ("-D", "--define"):
      Variables.update(dict(map(lambda b: filter(lambda a: a != '', b),
                                re.findall("(\w+)=\"([^\"]*)\"\s*|(\w+)=([^\s]*)\s*", a))))
      pass
    pass

  for a in args:
    process(a, fpout)
    pass
  
