#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003 Helvetix Victorinox, a pseudonym,
# Mountain View, California
# $Id$
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


def format_attrs(attrs):
  if type(attrs) == dict:
    k = attrs.keys()
    k.sort()
    a = string.join(map(lambda key: '%s="%s"' % (key, attrs[key]), k))
    if len(a) > 0:
      a = " " + a
      pass
    pass
  else:
    raise TypeError, "attributes must be a dictionary, not a " + str(type(attrs))
  
  return (a)


class xml_init:
  def __init__(self, klasse, attrs):
    self.attrs = dict(klasse.defaults)
    self.attrs.update(attrs)
    self.tag = klasse.tag
    return None

  def __coerce__(self, other):
    return ("%s" % (self), ("%s" % (other)))

  def __repr__(self):
    if self.tag != None:
      return ("<" + self.tag + format_attrs(self.attrs) + ">")
    else:
      return ("")
    pass
  pass

    
class xml_fini:
  def __init__(self, klasse):
    self.tag = klasse.tag
    return None
  
  def __coerce__(self, other):
    return (str(self), str(other))
  
  def __repr__(self):
    if self.tag != None:
      return ("</" + self.tag + ">")
    else:
      return ("")
  
  pass


#
# This class handles attributes as variable argument dictionary
# The problem with this class is that I cannot say, for example
# 'class="header"' because 'class' is a keyword in Python.
#
# Don't depend on this class definition's future. XXX
#

class xml:
  def __init__(self, content="", **attrs):
    self.attrs = dict(self.defaults)
    self.attrs.update(attrs)

    if type(content) == types.FileType:
      self.content = string.join(content.readlines())
    else:
      self.content = content
      pass
    
    return None

  def __getitem__(self, name):
    return (self.attrs[name])

  def __setitem__(self, name, value):
    self.attrs[name] = value
    return (None)

  def __coerce__(self, other):
    return (str(self), str(other))
    
  def __repr__(self):
    return (str(self.init(self.attrs)) + self.content + str(self.fini()))

  pass

#
# This class handles attributes as a dictionary
#
class Xml:
  init = None
  fini = None
  
  def __init__(self, *args):

    content = None
    attrs = {}

    for a in args:
      if type(a) == dict:
        attrs = a
      else:
        content = str(a)
        pass
      pass

    if self.fini == None and content != None:
      raise ValueError, "element " + self.tag + " does not take content."

    self.attrs = dict(self.defaults)
    self.attrs.update(attrs)

    if type(content) == types.FileType:
      self.content = string.join(content.readlines())
    else:
      self.content = content
      pass

    if self.content == None:
      self.content = ""
      pass
    
    return None

  def __getitem__(self, name):
    return (self.attrs[name])

  def __setitem__(self, name, value):
    self.attrs[name] = value
    return (None)

  def __coerce__(self, other):
    return (str(self), str(other))
    
  def __str__(self):
    if self.fini == None:
      return ("<" + self.tag + format_attrs(self.attrs) + " />")
    
    return ("<" + self.tag + format_attrs(self.attrs) + ">" + str(self.content) + ("</" + self.tag + ">"))

  def __repr__(self):
    if self.fini == None:
      return ("<" + self.tag + format_attrs(self.attrs) + " />")

    return ("<" + self.tag + format_attrs(self.attrs) + ">" + str(self.content) + ("</" + self.tag + ">"))

  pass


def header():
  return ('<?xml version="1.0" encoding="iso-8859-1"?>')


def xml_(**attrs):
  defaults = {"version" : "1.0", "encoding" : "iso-8859-1"}
  a = dict(defaults)
  a.update(attrs)
  return '<?xml' + format_attrs(a) + '?>'


if __name__ == "__main__":
  print xml_()
