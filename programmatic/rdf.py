#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003 Helvetix Victorinox, a pseudonym,
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

import types
import string
import sys
import os
import cgi
import base64
from UserDict import *

class rdf_attrs(UserDict):
  def __init__(self, attrs):
    UserDict.__init__(self, attrs)
    return None

  def __repr__(self):
    str = ""
    k = self.data.keys()
    k.sort()
    
    for a in k:
      if self.data[a] == "" or self.data[a] == None:
        str += ' %s' % (a)
      else:
        str += ' %s="%s"' % (a, self.data[a])
        pass
      pass
                    
    return str
  pass

class rdf_init:
  def __init__(self, attrs, begin="<??%s>"):
    self.begin = begin
    self.a = rdf_attrs(attrs)
    return None

  def __coerce__(self, other):
    return ("%s" % (self), ("%s" % (other)))

  def __repr__(self):
    return self.begin % (self.a)

  pass
    
class rdf_fini:
  def __init__(self, tag="</??>"):
    self.tag = tag
    return None
  
  def __coerce__(self, other):
    return (str(self), str(other))
  
  def __repr__(self):
    return self.tag
  pass

class __rdf__:
  def __init__(self, content, attrs, begin="<??%s>", end="</??>"):
    self.begin = begin
    self.end = end
    self.a = rdf_attrs(attrs)

    if type(content) == types.NoneType:
      self.content = ""
    elif type(content) == types.StringType:
      self.content = content
    elif type(content) == types.FileType:
      self.content = ""
      self.readfile(content)
    else:
      self.content = content
      pass
    return None

  def __coerce__(self, other):
    return (str(self), str(other))
    
  def __repr__(self):
    return self.begin % (self.a) + str(self.content) + self.end

  def __add__(self, other):
    print >>sys.stderr, "add self, other", type(self), type(other)
    return __rdf__("%s%s" % (self, other), {})

  def attribute(self, name, value):
    self.a[name] = value
    return self

  def readfile(self, input):
    if type(input) == types.StringType:
      input = open(input)
      pass
            
    for l in input.read():
      self.content += l
      pass

    return self
  pass

class rdf(__rdf__):
  defaults = {
      "xmlns:rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "xmlns" : "http://my.netscape.com/rdf/simple/0.9/"
      }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __rdf__.__init__(self, content, a, "<rdf:RDF%s>", "</rdfRDF>")
    return None

  class init(rdf_init):
    def __init__(self, attrs={}):
      a = dict(rdf.defaults)
      a.update(attrs)
      return (rdf_init.__init__(self, a, "<rdf:RDF%s>"))
    pass

  class fini(rdf_fini):
    def __init__(self, attrs={}):
      return (rdf_fini.__init__(self, "</rdf:RDF>"))
    pass
  pass

