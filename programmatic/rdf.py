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
import pprint
import inspect

sys.path = ['${LIBDIR}'] + sys.path

import xml

class RDF(xml.xml):
  defaults = {
      "xmlns:rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "xmlns:" : "http://www.gimp.org/RDF/v0.1"
      }
  tag = "rdf:RDF"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, RDF, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, RDF))
    pass
  pass

class content(xml.xml):
  defaults = { }
  tag = "content"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, content, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, content))
    pass
  pass


class link(xml.xml):
  defaults = { }
  tag = "link"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, link, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, link))
    pass
  
  pass


class date(xml.xml):
  defaults = { }
  tag = "dc:date"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, date, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, date))
    pass
  
  pass

class channel(xml.xml):
  defaults = { }
  tag = "channel"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, channel, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, channel))
    pass
  
  pass

class title(xml.xml):
  defaults = { }
  tag = "title"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, title, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, title))
    pass
  
  pass

class description(xml.xml):
  defaults = { }
  tag = "description"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, description, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, description))
    pass
  
  pass

class item(xml.xml):
  defaults = { }
  tag = "item"

  class init(xml.xml_init):
    def __init__(self, attrs={}):
      return (xml.xml_init.__init__(self, item, attrs))
    pass

  class fini(xml.xml_fini):
    def __init__(self):
      return (xml.xml_fini.__init__(self, item))
    pass
  
  pass
