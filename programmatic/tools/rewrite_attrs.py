#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
#
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
#

# This simple script will rewrite any attribute: value pair in any
# xhtml element.  What is rewritten is configured by an external file.
# The name of the file to use is supplied as the first argument to
# this script.  The second argument is a well-formed xhtml document to
# use as input.  Output is standard out with the attributes and values
# in the input document substituted.
#
# The file format of the configure file is exactly like this:
#
# [ attribute_name ,  original_value,  {  attribute_name : new_value }]
#
# For example:

# ["href", "http:Gnome Main Site",       { "href": "http://www.gnome.org" } ]
# ["href", "http:Google",                { "href": "http://www.google.com" } ]
# ["href", "http:Sun Microsystems",      { "href": "http://www.sun.com" } ]
# ["href", "mailto:Sun Microsystems",    { "href": "mailto:webmaster@sun.com" }]
#
# replaces forms like href="httpGoogle" with href="http://www.google.com"
#
# Note that attribute names can be rewritten as well.
#

import types
import string
import sys
import os
import re
import HTMLParser
import x_xml

def doattrs(attrs):
  d = {}
  map(lambda (a, v): d.update(substitute(a, v)), attrs)
  return (d)
  
def substitute(a, v):
  if dictionary.has_key(a):
    d = dictionary[a]
    if d.has_key(v):
      return (d[v])
    pass

  return ({a: v})

class xlt(HTMLParser.HTMLParser):
  def handle_starttag(self, tag, attrs):
    sys.stdout.write("<" + tag + x_xml.format_attrs(doattrs(attrs)) + ">")
    return

  def handle_endtag(self, tag):
    sys.stdout.write("</" + tag + ">")
    return

  def handle_startendtag(self, tag, attrs):
    sys.stdout.write("<" + tag + x_xml.format_attrs(doattrs(attrs)) + ">")
    return

  def handle_data(self, data):
    sys.stdout.write(data)
    return
  
  def handle_charref(self, name):
    sys.stdout.write("&#" + name)
    return
  
  def handle_entityref(self, name):
    sys.stdout.write("&" + name + ";")
    return
  
  def handle_comment(self, data):
    sys.stdout.write("<!--" + data + " -->")
    return
  
  def handle_decl(self, decl):
    sys.stdout.write("<!" + decl + ">")
    return
  
  pass

def rewrite_dictionary(filename):
  dictionary = {}
  
  fp = open(filename, "r")
  lines = fp.readlines()
  fp.close()
  
  for line in lines:
    line = re.sub("#.*", "", line)
    line = re.sub("^[ \t]+", "", line)
    
    if len(line) > 1:
      (pre_attr, value, substitution) = eval(line)
      index = {value: substitution}
      if not dictionary.has_key(pre_attr):
        new_attr ={pre_attr : index}
        dictionary.update(new_attr)
      else:
        dictionary[pre_attr].update(index)
        pass
      pass
    pass

  del lines
  
  return (dictionary)

if __name__ == "__main__":

  dictionary = rewrite_dictionary(sys.argv[1])

  x = xlt()

  fp = open(sys.argv[2], "r")
  x.feed(fp.read())
  x.close()
  fp.close()
  sys.exit(0)

