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

import x_xml

def quote(s):
  s = string.replace(s, "&", "&amp;")
  s = string.replace(s, "<", "&lt;")
  s = string.replace(s, ">", "&gt;")
  return (s)
  
# Namespaces should appear to be imported into Python as well.
# Otherwise, I have to write all these silly wrappers. XXX

class RDF(x_xml.Xml):
  defaults = {
    "xmlns"       : "http://purl.org/rss/1.0/",
    "xmlns:dc"    : "http://purl.org/dc/elements/1.1/",
    "xmlns:rdf"   : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    
    "xmlns:admin" : "http://webns.net/mvcb/",
    "xmlns:syn"   : "http://purl.org/rss/1.0/modules/syndication/",
    "xmlns:taxo"  : "http://purl.org/rss/1.0/modules/taxonomy/",
    "xmlns:gimp"  : "http://www.gimp.org/RDF/v0.1"
    }
  tag = "rdf:RDF"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, RDF, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, RDF))
    pass
  pass

class rss(x_xml.Xml):
  defaults = { }
  tag = "rss"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, rss, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, rss))
    pass
  pass

class content(x_xml.Xml):
  defaults = { }
  tag = "content"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, content, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, content))
    pass
  pass


class link(x_xml.Xml):
  defaults = { }
  tag = "link"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, link, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, link))
    pass
  
  pass


class pubDate(x_xml.Xml):
  defaults = { }
  tag = "pubDate"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, pubDate, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, pubDate))
    pass
  
  pass


class channel(x_xml.Xml):
  tag = "channel"
  defaults = { }

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, channel, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, channel))
    pass
  
  pass

class title(x_xml.Xml):
  defaults = { }
  tag = "title"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, title, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, title))
    pass
  
  pass

class description(x_xml.Xml):
  defaults = { }
  tag = "description"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, description, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, description))
    pass
  
  pass

class item(x_xml.Xml):
  defaults = { }
  tag = "item"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, item, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, item))
    pass
  
  pass

class items(x_xml.Xml):
  defaults = { }
  tag = "items"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, item, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, item))
    pass
  
  pass

class li(x_xml.Xml):
  defaults = { }
  tag = "rdf:li"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, item, attrs))
    pass

  pass

class seq(x_xml.Xml):
  defaults = { }
  tag = "rdf:Seq"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, item, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, item))
    pass
  
  pass

# Dublin Core Metadata Element Set
# http://web.resource.org/rss/1.0/modules/dc/
#
# Again, namespaces should be imported (somehow) so they appear
# without all writting all the wrappers by hand.

class dc_title(x_xml.Xml):
  defaults = { }
  tag = "dc:title"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_title, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_title))
    pass
  
  pass

class dc_creator(x_xml.Xml):
  defaults = { }
  tag = "dc:creator"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_creator, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_creator))
    pass
  
  pass

class dc_subject(x_xml.Xml):
  defaults = { }
  tag = "dc:subject"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_subject, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_subject))
    pass
  
  pass

class dc_description(x_xml.Xml):
  defaults = { }
  tag = "dc:description"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_description, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_description))
    pass
  
  pass


class dc_publisher(x_xml.Xml):
  defaults = { }
  tag = "dc:publisher"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_publisher, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_publisher))
    pass
  
  pass

class dc_contributor(x_xml.Xml):
  defaults = { }
  tag = "dc:contributor"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_contributor, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_contributor))
    pass
  
  pass

class dc_date(x_xml.Xml):
  defaults = { }
  tag = "dc:date"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_date, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_date))
    pass
  
  pass

class dc_type(x_xml.Xml):
  defaults = { }
  tag = "dc:type"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_type, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_type))
    pass
  
  pass

class dc_format(x_xml.Xml):
  defaults = { }
  tag = "dc:format"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_format, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_format))
    pass
  
  pass

class dc_identifier(x_xml.Xml):
  defaults = { }
  tag = "dc:identifier"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_identifier, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_identifier))
    pass
  
  pass

class dc_source(x_xml.Xml):
  defaults = { }
  tag = "dc:source"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_source, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_source))
    pass
  
  pass

class dc_language(x_xml.Xml):
  defaults = { }
  tag = "dc:language"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_language, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_language))
    pass
  
  pass

class dc_relation(x_xml.Xml):
  defaults = { }
  tag = "dc:relation"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_relation, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_relation))
    pass
  
  pass

class dc_coverage(x_xml.Xml):
  defaults = { }
  tag = "dc:coverage"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_coverage, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_coverage))
    pass
  
  pass

class dc_rights(x_xml.Xml):
  defaults = { }
  tag = "dc:rights"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dc_rights, attrs))
    pass

  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dc_rights))
    pass
  
  pass
