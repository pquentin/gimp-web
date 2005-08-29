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

#
#  All of this is to make XHTML (1.0) conformant markup.
#
#  See accompanying Python scripts for examples of how I use this.
#

import types
import string
import sys
import os
import cgi
import base64
#from UserDict import *

import x_xml

# rfc2396_reserved = [";", "/", "?", ":", "@", "&", "=", "+", "$", ","]
#html_coreattrs = {"id", "class", "style", "title"}


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
  for c in ["%", ";", "/", ":", "?", "@", "&", "=", "+", "$", ",", " ", "(", ")", "<", ">"]:
    s = string.replace(s, c, _hexc(c))
  return s


def unescape(s):
  s = str(s)
  for c in [">", "<", ";", "/", "?", ":", "@", "&", "=", "+", "$", ",", " ", "(", ")", "%"]:
    s = string.replace(s, _hexc(c), c)
  return s


def quote(s):
  s = str(s)
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
  """Print the contents of a form as xhtml."""
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


##################################################################


class html_attrs:
  def __init__(self, attrs):
    self.data = attrs
    return None

  def __repr__(self):
    k = self.data.keys()
    k.sort()
    return (string.join(map(lambda key: ' %s="%s"' % (key, self.data[key]), k)))
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


def include(filename):
  fp = open(filename, "r")
  content =  fp.read()
  fp.close()
  return (content)
  

def xml(attrs={"version" : "1.0", "encoding" : "utf-8"}):
  return ("<?xml" + x_xml.format_attrs(attrs) + "?>")
    
    
def doctype():
  s = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
  s += xhtml.comment("This document was automatically generated by $Id$")
  return (s)
    

class body(x_xml.Xml):
  defaults = {}
  tag = "body"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, body, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, body))
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


class html(x_xml.Xml):
  defaults = { }
  tag = "html"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, html, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, html))
    pass
  pass

    
class link(x_xml.Xml):
  defaults = { "rel": "stylesheet", "href": "#", "type": "text/css" }
  tag = "link"
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, html, attrs))
    pass
  pass


class hyperlink(x_xml.Xml):
  tag = "a"
  defaults = {"href" : "#"}
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, hyperlink, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, hyperlink))
    pass
  pass


def mailto(address):
  return (hyperlink(character_reference(address), {"href" : character_reference("mailto:") + character_reference(address)}))


def comment(content):
  return ("<!--" + content + " -->")



class face_tt(x_xml.Xml):
  defaults = { }
  tag = "tt"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, face_tt, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, face_tt))
    pass
  pass


class list(x_xml.xml):
  defaults = { }
  tag = "ul"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, list, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, list))
    pass

  class item(x_xml.xml):
    defaults = { }
    tag = "li"

    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, list.item, attrs))
      pass
  
    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, list.item))
      pass
    pass
  pass


class div(x_xml.Xml):
  defaults = { }
  tag = "div"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, div, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, div))
    pass
  pass


class span(x_xml.Xml):
  defaults = { }
  tag = "span"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, span, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, span))
    pass
  pass


class h1(x_xml.Xml):
  defaults = { }
  tag = "h1"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h1, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h1))
    pass
  pass


class h2(x_xml.Xml):
  defaults = { }
  tag = "h2"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h2, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h2))
    pass
  pass


class h3(x_xml.Xml):
  defaults = { }
  tag = "h3"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h3, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h3))
    pass
  pass


class h4(x_xml.Xml):
  defaults = { }
  tag = "h4"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h4, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h4))
    pass
  pass


class h5(x_xml.Xml):
  defaults = { }
  tag = "h5"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h5, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h5))
    pass
  pass


class h6(x_xml.Xml):
  defaults = { }
  tag = "h6"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, h6, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, h6))
    pass
  pass

class para(x_xml.Xml):
  defaults = { }
  tag = "p"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, para, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, para))
    pass
  pass


class dd(x_xml.Xml):
  defaults = { }
  tag = "dd"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dd, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dd))
    pass
  pass


class dl(x_xml.Xml):
  defaults = { }
  tag = "dl"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dl, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dl))
    pass
  pass


class dt(x_xml.Xml):
  defaults = { }
  tag = "dt"

  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, dt, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, dt))
    pass
  pass


class head(x_xml.Xml):
  tag = "head"
  defaults = {}
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, head, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, head))
    pass
  pass


def text(content=""):
  return (content)


class table(__html__):
  defaults = {"summary": "table" }

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
  
  class row(x_xml.Xml):
    tag = "tr"
    defaults = {}
    
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, table.row, attrs))
      pass
  
    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, table.row))
      pass
    pass

  class cell(x_xml.Xml):
    tag = "td"
    defaults = {}
    
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, table.cell, attrs))
      pass
  
    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, table.cell))
      pass
    pass

  class header(x_xml.Xml):
    tag = "th"
    defaults = {}
    
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, table.header, attrs))
      pass
  
    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, table.header))
      pass
    pass
  pass


class object(x_xml.Xml):
  tag = "object"
  defaults = {}
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, object, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, object))
    pass
  pass


class image(x_xml.Xml):
  tag = "img"
  defaults = {"alt" : "image"}
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, image, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, image))
    pass
  pass


def linebreak():
  return ("<br />")


class script(x_xml.Xml):
  tag = "script"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, script, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, script))
    pass
  pass


class pre(x_xml.Xml):
  tag = "pre"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, pre, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, pre))
    pass
  pass


class label(x_xml.Xml):
  tag = "label"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, label, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, label))
    pass
  pass



class input(x_xml.Xml):
  tag = "label"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, label, attrs))
    pass
  
  class hidden(x_xml.Xml):
    tag = "input"
    defaults = {"type" : "hidden" }
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.hidden, attrs))
      pass
    pass
  
  class submit(x_xml.Xml):
    tag = "input"
    defaults = {"type" : "submit" }
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.submit, attrs))
      pass
    pass
  
  class checkbox(x_xml.Xml):
    tag = "input"
    defaults = {"type" : "checkbox" }
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.checkbox, attrs))
      pass
    pass
  

  class text(x_xml.Xml):
    tag = "input"
    defaults = {"type" : "text" }
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.text, attrs))
      pass
    pass
  

  class file(x_xml.Xml):
    tag = "input"
    defaults = {"type" : "file" }
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.file, attrs))
      pass
    pass
  
  class button(x_xml.Xml):
    tag = "button"
    defaults = {}
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.button, attrs))
      pass
    pass

  class textarea(x_xml.Xml):
    tag = "textarea"
    defaults = {}
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.textarea, attrs))
      pass

    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, input.textarea))
      pass
    pass

  class select(x_xml.Xml):
    tag = "select"
    defaults = {}
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.select, attrs))
      pass

    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, input.select))
      pass
    pass

  class option(x_xml.Xml):
    tag = "option"
    defaults = {}
  
    class init(x_xml.xml_init):
      def __init__(self, attrs={}):
        return (x_xml.xml_init.__init__(self, input.option, attrs))
      pass

    class fini(x_xml.xml_fini):
      def __init__(self):
        return (x_xml.xml_fini.__init__(self, input.option))
      pass
    pass
  pass

    
class form(x_xml.Xml):
  tag = "form"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, form, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, form))
    pass
  pass


class meta(x_xml.Xml):
  tag = "meta"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, meta, attrs))
    pass
  

class style(x_xml.Xml):
  tag = "style"
  defaults = { }
  
  class init(x_xml.xml_init):
    def __init__(self, attrs={}):
      return (x_xml.xml_init.__init__(self, style, attrs))
    pass
  
  class fini(x_xml.xml_fini):
    def __init__(self):
      return (x_xml.xml_fini.__init__(self, style))
    pass
  pass



def php(content=""):
  return ("<?php " + content + " ?>")



color = {}

def _load_rgb(file="/usr/lib/X11/rgb.txt"):
  _input = open(file)
  _input.readline()
  for _line in _input.readlines():
    _s = _line.split()
    color.update({ string.joinfields(_s[3:]): "#%02x%02x%02x" % (int(_s[0]), int(_s[1]), int(_s[2]))})
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
