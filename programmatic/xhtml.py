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

import xml

color = {}

# rfc2396_reserved = [";", "/", "?", ":", "@", "&", "=", "+", "$", ","]

#html_coreattrs = {"id", "class", "style", "title"}

def rawfile(filename):
  fp = open(filename, "r")
  data = fp.read()
  fp.close()
  return (data)
  
def encodefile(filename):
  fp = open(filename, "r")
  data = fp.read()
  fp.close()
  return (base64.encodestring(data))

def _hexc(c):
  return ("%%%02X" % (ord(c)))


def _charref(c):
  return ("&#%d;" % (ord(c)))


def escape(s):
  s = str(s)
  for c in ["%", ";", "/", "?", ":", "@", "&", "=", "+", "$", ",", " ", "(", ")"]:
    s = string.replace(s, c, _hexc(c))
  return s


def unescape(s):
  s = str(s)
  for c in [";", "/", "?", ":", "@", "&", "=", "+", "$", ",", " ", "(", ")", "%"]:
    s = string.replace(s, _hexc(c), c)
  return s


def quote(s):
  s = string.replace(s, "&", "&amp;")
  s = string.replace(s, "<", "&lt;")
  s = string.replace(s, ">", "&gt;")
  return (s)


def character_reference(s):
  s = str(s)
  a_z = map(lambda c: chr(c), range(ord("a"), ord("z")))
  A_Z = map(lambda c: chr(c), range(ord("A"), ord("Z")))
  for c in ["/", "?", ":", "@", "=", ".", "!", "<", ">"] + a_z + A_Z:
    s = string.replace(s, c, _charref(c))
  return s

  
def environ():
  l = os.environ.keys()
  l.sort()
  print div.init({"style" : "border: thin solid red; font-size: small; padding: 2px;"})
  map(lambda k: sys.stdout.write("%s=%s<br />\n" % (k, escape(os.environ[k]))), l)
  print div.fini()
  return (None)

def validate(text="validate", attrs={}):
  attrs.update({"href" : "http://validator.w3.org/check/referer"})
  return hyperlink(text, attrs)

def print_form(form, label="Form Contents"):
  """PrintdDump the contents of a form as xhtml."""
  keys = form.keys()
  keys.sort()

  print "Content-Type: text/html"
  print
  print '<div style="border: thin solid red; font-size: small; padding: 2px;">'
  print '<div style="font-weight: bold; margin-bottom: 1ex;">' + label + "</div>"
  if not keys:
    print para("No form fields.")
    pass

  for key in keys:
    value = form[key]
    print '<div><span style="font-family: monospace; text-decoration: underline;">'
    print quote(key)
    print "</span>&nbsp;<b>&equiv;</b>&nbsp;<i>"
    print quote(`type(value)`) + "</i></div>" + '<div style="text-indent: 3em;">' + quote(`value`) + "</div>"
    pass
  
  print "</div>"

  return

class html_attrs(UserDict):
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

class xyz_init:
  def __init__(self, attrs, begin="<??%s>"):
    self.begin = begin
    self.a = html_attrs(attrs)
    return None

  def __coerce__(self, other):
    return ("%s" % (self), ("%s" % (other)))

  def __repr__(self):
    return self.begin % (self.a)

  pass
    
class xyz_fini:
  def __init__(self, tag="</??>"):
    self.tag = tag
    return None
  
  def __coerce__(self, other):
    return (str(self), str(other))
  
  def __repr__(self):
    return self.tag
  pass

class __html__:
  def __init__(self, content, attrs, begin="<??%s>", end="</??>"):
    self.begin = begin
    self.end = end
    self.a = html_attrs(attrs)

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
    return __html__("%s%s" % (self, other), {})

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

class debug(__html__):
  def __init__(self, content=None, attrs={}):
    print >>sys.stderr, content
    return None
  pass

class include(__html__):
  def __init__(self, filename):
    fp = open(filename, "r")
    content =  fp.read()
    fp.close()
    __html__.__init__(self, content, {}, "", "")
    return
  pass

class xml(__html__):
  def __init__(self, attrs={"version" : "1.0", "encoding" : "iso-8859-1"}):
    __html__.__init__(self, None, attrs, '<?xml%s?>', "")
    return
  pass
    
    
class doctype(__html__):
  def __init__(self):
    __html__.__init__(self, None, {}, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">', "")
    return
  pass
    
class body(__html__):
  defaults = {}

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<body%s>", "</body>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(body.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<body%s>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</body>"))
    pass
  pass

class title(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<title%s>", "</title>")
    return None
  pass

class html(__html__):
  def __init__(self, content=None, attrs={}):
    return (__html__.__init__(self, content, attrs, "<html%s>", "</html>"))

  class init(xyz_init):
    def __init__(self, attrs={}):
      return (xyz_init.__init__(self, attrs, "<html%s>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</html>"))
    pass
  pass
    
class link(__html__):
  defaults = { "rel": "stylesheet", "href": "#", "type": "text/css" }
  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<link%s />", "")
    return None
  pass

class hyperlink(__html__):
  def __init__(self, content=None, attrs={"href": "#"}):
    __html__.__init__(self, content, attrs, "<a%s>", "</a>")
    return None
  pass

class mailto(__html__):
  def __init__(self, content=None, attrs={}):
    attrs = {"href" : character_reference("mailto:") + character_reference(content)}
    __html__.__init__(self, character_reference(content), attrs, "<a%s>", "</a>")
    return None
  pass

class comment(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<!--", " -->")
    return None
  pass

class list(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<ul%s>", "</ul>")
    return None

  class item(__html__):
    def __init__(self, content=None, attrs={}):
      __html__.__init__(self, content, attrs, "<li%s>", "</li>")
      return None
    pass
  pass

class div(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<div%s>", "</div>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(div.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<div%s>"))
    pass
  
  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</div>"))
    pass
  pass

class span(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<span%s>", "</span>")
    return None
  pass

class h1(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class h2(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class h3(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class h4(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class h5(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class h6(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<h1%s>", "</h1>")
    return None
  pass

class para(__html__):
  defaults = { }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<p%s>", "</p>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(para.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<p%s>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</p>"))
    pass
  pass

class dd(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<dd%s>", "</dd>")
    return None
  pass

class dl(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<dl%s>", "</dl>")
    return None
  pass

class dt(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<dt%s>", "</dt>")
    return None
  pass

class head(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<head%s>", "</head>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      return (xyz_init.__init__(self, attrs, "<head%s>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</head>"))
    pass
  pass

class text(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "", "")
    return None

  def __repr__(self):
    return self.content
  pass

class table(__html__):
  defaults = {"summary": "table", "cellpadding" : 0, "cellspacing" : 0}

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)

    __html__.__init__(self, content, a, "<table%s><tbody>", "</tbody></table>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(table.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<table%s><tbody>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</tbody></table>"))
    pass
  
  class row(__html__):
    def __init__(self, content=None, attrs={}):
      __html__.__init__(self, content, attrs, "<tr%s>", "</tr>")
      return None

    class init(xyz_init):
      def __init__(self, attrs={}):
        return (xyz_init.__init__(self, attrs, "<tr%s>"))
      pass

    class fini(xyz_fini):
      def __init__(self, attrs={}):
        return (xyz_fini.__init__(self, "</tr>"))
      pass
    pass
    
  class cell(__html__):
    def __init__(self, content=None, attrs={}):
      self.attributes = attrs
      __html__.__init__(self, content, self.attributes, "<td%s>", "</td>")
      return None

    class init(xyz_init):
      def __init__(self, attrs={}):
        return (xyz_init.__init__(self, attrs, "<td%s>"))
      pass
    
    class fini(xyz_fini):
      def __init__(self, attrs={}):
        return (xyz_fini.__init__(self, "</td>"))
      pass
    pass

  class header(__html__):
    def __init__(self, content=None, attrs={}):
      __html__.__init__(self, content, attrs, "<th%s>", "</th>")
      return None
    pass
  pass

class object(__html__):
  defaults = {  }

  def __init__(self, content=None, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<object%s>", "</object>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(div.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<object%s>"))
    pass
  
  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</object>"))
    pass
  pass

class _object(__html__):
  defaults = {  }

  def __init__(self, *args):
    a = {}
    __html__.__init__(self, content, a, "<object%s>", "</object>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      return (xyz_init.__init__(self, attrs, "<object%s>"))
    pass
  
  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</object>"))
    pass
  pass

class image(__html__):
  defaults = {"alt" : "image"}

  def __init__(self, attrs={}):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, "", a, "<img%s />", "")
    return None
  pass

class linebreak(__html__):
    def __init__(self, content=None, attrs={}):
        __html__.__init__(self, content, attrs, "", "<br />")
        return None

class script(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<script%s>", "</script>")
    return None
  pass

class pre(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, escape(content), attrs, "<pre%s>", "</pre>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      return (xyz_init.__init__(self, attrs, "<pre%s>"))
    pass
  
  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</pre>"))
    pass
  pass

class label(__html__):
  def __init__(self, content=None, attrs={}):
    __html__.__init__(self, content, attrs, "<label%s>", "</label>")
    return None
  pass

class input(__html__):
  defaults = {"type": "submit", "name": "submit"}
  allowed = {"type":
             ("text", "password", "checkbox", "radio", "submit",
              "reset", "file", "hidden", "image", "button")}
  def __init__(self, attrs=defaults):
    __html__.__init__(self, "", attrs, "<input%s />", "")
    return None

  class hidden(__html__):
    def __init__(self, attrs={}):
      __html__.__init__(self, "", attrs, '<input type="hidden"%s />', "")
      return None
    pass
    
  class submit(__html__):
    def __init__(self, attrs={}):
      __html__.__init__(self, "", attrs, '<input type="submit"%s />', "")
      return None
    pass

  class checkbox(__html__):
    def __init__(self, attrs={}):
      __html__.__init__(self, "", attrs, '<input type="checkbox"%s />', "")
      return None
    pass

  class text(__html__):
    defaults = { }
    def __init__(self, attrs=defaults):
      __html__.__init__(self, "", attrs, '<input type="text"%s />', "")
      return None
    pass

  class file(__html__):
    defaults = { }
    def __init__(self, attrs=defaults):
      __html__.__init__(self, "", attrs, '<input type="file"%s />', "")
      return None
    pass

  class button(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
      __html__.__init__(self, content, attrs, "<button%s>", "</button>")
      return None
    pass

  class textarea(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
      __html__.__init__(self, content, attrs, "<textarea%s>", "</textarea>")
      return None
    pass

  class select(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
      __html__.__init__(self, content, attrs, "<select%s>", "</select>")
      return None
    pass
    
  class option(__html__):
    defaults = { }
    def __init__(self, content=None, attrs=defaults):
      __html__.__init__(self, content, attrs, "<option%s>", "</option>")
      return None
    pass
  pass
    
class form(__html__):
  defaults = { }
  def __init__(self, content=None, attrs=defaults):
    a = dict(self.defaults)
    a.update(attrs)
    __html__.__init__(self, content, a, "<form%s>", "</form>")
    return None

  class init(xyz_init):
    def __init__(self, attrs={}):
      a = dict(form.defaults)
      a.update(attrs)
      return (xyz_init.__init__(self, a, "<form%s>"))
    pass

  class fini(xyz_fini):
    def __init__(self, attrs={}):
      return (xyz_fini.__init__(self, "</form>"))
    pass
  pass

class meta(__html__):
  defaults = { }
  def __init__(self, content=None, attrs=defaults):
    __html__.__init__(self, content, attrs, "<meta%s />", "")
    return None
  pass

class style(__html__):
  defaults = {"type": "text/css" }
  def __init__(self, content=None, attrs=defaults):
    __html__.__init__(self, content, attrs, "<style%s>", "</style>")
    return None

  class css(__html__):
    def __init__(self, selector, style={}):
      self.selector = selector
      self.style = style
      return None
    pass

  def __repr__(self):
    out = self.selector + " { "
    for s in self.style.keys():
      out += '%s: %s; ' % (s, self.style[s])
      pass
    out += "}"
    return out
  pass

class php(__html__):
  defaults = { }
  def __init__(self, content=None, attrs=defaults):
    __html__.__init__(self, content, attrs, "<?php", "?>")
    return None
  pass

class extn(__html__):
  def __init__(self):
    return None
  pass

def _load_rgb(file="/usr/lib/X11/rgb.txt"):
  _input = open(file)
  _input.readline()
  for _line in _input.readlines():
    _s = _line.split()
    color.update({ string.joinfields(_s[3:]):
                   "#%02x%02x%02x" % (int(_s[0]), int(_s[1]), int(_s[2]))})
    pass
  
  _input.close()
  return

def _dump_colors():
  keys = color.keys()
  keys.sort()

  rows = ""
  for k in keys:
    row = table.row(table.cell("%s %s" % (color[k], k), {"style" : "background: %s none;" % (color[k])})
                    + table.cell("%s %s" % (color[k], k), {"style" : "background: white none;"}))
    rows += row.__repr__()
    pass

  print table(rows)
  return
