#!/usr/bin/env ${PYTHON}
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
import sre as re
import string
import getopt

class processor:
  Version = """SSI Preprocessor, version $Version:$
Copyright (C) 2003 Helvetix Victorinox, a pseudonym.
This is free software; see the source code for copying conditions.
There is ABSOLUTELY NO WARRANTY; not even for MERCHANTIBILITY or
FITNESS FOR A PARTICULAR PURPOSE.

Report bugs to: <HELVETIX@Mysterious.ORG>"""
  
  def __init__(self, variables=None):
    if variables == None:
      variables = os.environ
      pass
    
    self.variables = dict(variables)
    self.document_root = "./"
    return None


  def __interpolate_variables(self, name):
    s = ""

    _last = 0
    for l in re.finditer("\${(\w+)}|\$(\w+)", name):
      s += name[_last:l.start()]
      v = filter(lambda x: x != None, l.groups())
      v = v[0]
      s += self.variables[v]
      _last = l.end()
      pass

    s += name[_last:]
    return (s)


  def __parse_attribute(self, s):
    avlist = { }
    map(lambda x: avlist.update({x[0]: x[1]}), re.findall("(\w+)=\"([^\"]*)\"\s*", s))
    return (avlist)


  def parse(self, filename):
    if filename != '-':
      fp = open(filename, "r")
      body = fp.read()
      fp.close()
    else:
      body = sys.stdin.read()
      pass

    _last = 0
    output = ""

    #matches = re.findall("<!--#(\w+)\s+(.*)\s*-->", body)
    
    #for ssi in matches:
    for ssi in re.finditer("<!--#(\w+)\s+(.*)\s*-->", body):
      
      output += body[_last:ssi.start()]

      element = ssi.expand("\\1")
      attrs = self.__parse_attribute(ssi.expand("\\2"))

      if element == "include":
        output += self.parse(os.path.normpath(self.document_root + attrs["virtual"]))
      elif element == "set":
        value = self.__interpolate_variable(attrs["value"])
        self.variables.update({attrs["var"]: value})
      elif element == "echo":
        output += self.__interpolate_variable(attrs["var"])
      else:
        print >>sys.stderr, "Unsupported SSI element", element, "in", body[ssi.start():ssi.end()]
        raise AttributeError

      _last = ssi.end()
      pass
  
    output += body[_last:]
    return (output)


  def depend(self, filename):
    if filename != '-':
      fp = open(filename, "r")
      body = fp.read()
      fp.close()
    else:
      body = sys.stdin.read()
      pass

    files = [filename]
  
    for ssi in re.finditer("<!--#(\w+)\s+(.*)\s*-->", body):
      element = ssi.expand("\\1")
      attrs = self.__parse_attribute(ssi.expand("\\2"))

      if element == "include":
        l = self.depend(os.path.normpath(self.document_root + attrs["virtual"]))
        files.append(l)
      elif element == "set":
        value = self.__interpolate_variable(attrs["value"])
        self.variables.update({attrs["var"]: value})
      elif element == "echo":
        pass
      else:
        print >>sys.stderr, "Unsupported SSI element", element, "in", body[ssi.start():ssi.end()]
        raise AttributeButton
      pass
  
    return (files)
  pass
