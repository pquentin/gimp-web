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

class xml_attrs:
  def __init__(self, attrs):
    self.data = attrs
    return None

  def __repr__(self):
    str = ""
    k = self.data.keys()
    k.sort()

    for a in k:
      if self.data[a] == "":
        str += ' %s' % (a)
      elif self.data[a] == None:
        pass
      else:
        str += ' %s="%s"' % (a, self.data[a])
        pass
      pass

    return (str)
  pass

def format_attrs(attrs):
  str = ""
  k = attrs.keys()
  k.sort()

  for a in k:
    if attrs[a] == "":
      str += ' %s' % (a)
    elif attrs[a] == None:
      pass
    elif type(attrs[a]) == type({}):
      str += format_attrs(attrs[a])
    else:
      str += ' %s="%s"' % (a, attrs[a])
      pass
    pass
  
  return (str)


class xml_init:
  def __init__(self, klasse, attrs):
    self.attrs = dict(klasse.defaults)
    self.attrs.update(attrs)
    self.tag = klasse.tag
    return None

  def __coerce__(self, other):
    return ("%s" % (self), ("%s" % (other)))

  def __repr__(self):
    return "<" + self.tag + format_attrs(self.attrs) + ">"

  pass

    
class xml_fini:
  def __init__(self, klasse):
    self.tag = klasse.tag
    return None
  
  def __coerce__(self, other):
    return (str(self), str(other))
  
  def __repr__(self):
    return "</" + self.tag + ">"
  
  pass


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

def header():
  return ('<?xml version="1.0" encoding="iso-8859-1"?>')


