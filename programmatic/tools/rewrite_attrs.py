#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
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
# Note that other attribute values can be rewritten as well.
#

import types
import string
import sys
import os
import re
import HTMLParser
import getopt

sys.path = ['${SRCDIR}'] + sys.path

import x_xml

def rewrite_attrs(attrs):
  d = dict()
  map(lambda (a, v): d.update(substitute(a, v)), attrs)
  
  return (d)
  
def substitute(a, v):
  if dictionary.has_key(a):
    d = dictionary[a]
    if d.has_key(v):
      return (d[v])
    pass

  return ({a: v})

    
def check_attribute_sanity(filename, attrs):
  for (a, v) in attrs:
    if type(v) == type(None):
      sys.stderr.write("Warning: " + filename + ": attribute '" + a + "' has no value.  See http://www.w3.org/TR/xhtml1/#h-4.5 and http://www.w3.org/TR/xhtml1/#C_10\n")
      pass
    pass
  return

# Return True if the supplied <string> looks like it is the content of
# an Apache SSI directive.
#
def is_apache_ssi_p(string):
  data = string.lstrip()
  if len(data) > 0 and data[0] == "#":
    return True
  return False
  
class xhtml_parser(HTMLParser.HTMLParser):
  def __init__(self, filename, quiet_flag=False, strip_comments_flag=False, output=sys.stdout):
    self.filename = filename
    self.quiet = quiet_flag
    self.strip_comments = strip_comments_flag
    self.serial = 0
    self.output = output
    self.declaration_done = False
    self.banner_comment_already_printed = False
    return HTMLParser.HTMLParser.__init__(self)

  def handle_pi(self, tag):
    self.output.write("<?" + tag + ">")
    return

  def handle_starttag(self, tag, attrs):
    self.serial += 1

    check_attribute_sanity(self.filename, attrs)
    
    self.print_banner_comment()
    self.output.write("<" + tag + x_xml.format_attrs(rewrite_attrs(attrs)) + ">")
    return

  def handle_endtag(self, tag):
    self.output.write("</" + tag + ">")
    return

  def handle_startendtag(self, tag, attrs):
    self.output.write("<" + tag + x_xml.format_attrs(rewrite_attrs(attrs)) + " />")
    self.serial += 1
    return

  def handle_data(self, data):
    self.output.write(data)
    return
  
  def handle_charref(self, name):
    self.output.write("&#" + name)
    return
  
  def handle_entityref(self, name):
    self.output.write("&" + name + ";")
    return
  
  def handle_comment(self, data):
    if is_apache_ssi_p(data):
      # Be sure any ssi directives appear before our special comment.
      self.output.write("<!--" + data + "-->")
      self.print_banner_comment()
    elif not self.strip_comments:
      # Be sure any ssi directives appear before our special comment.
      self.print_banner_comment()
      self.output.write("<!--" + data + "-->")
      pass
    return
  
  def handle_decl(self, decl):
    self.output.write("<!" + decl + ">")
    self.declaration_done = true
    self.print_banner_comment()
    return
  
  def print_banner_comment(self):
    if not self.banner_comment_already_printed:
      if not self.quiet:
        self.output.write("\n<!-- This file was automatically generated from " + self.filename + " by rewrite-attrs.py $Revision$.  Do not edit. -->")
        pass
      self.banner_comment_already_printed = True
    return

  pass

  
def load_rewrite_dictionary(filename):
  dictionary = {}
  
  fp = open(filename, "r")
  lines = fp.readlines()
  fp.close()
  
  for line in lines:
    #line = re.sub("#.*", "", line)
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

Version = """XML Attribute Rewriter, version $Revision$
Copyright (C) 2003 Helvetix Victorinox, a pseudonym.
This is free software; see the source code for copying conditions.
There is ABSOLUTELY NO WARRANTY; not even for MERCHANTIBILITY or FITNESS
FOR A PARTICULAR PURPOSE.

Report bugs to: <HELVETIX@Mysterious.ORG>"""

def usage(name):
  print Version
  print "Usage:", name, "[OPTION] [FILE]"
  print "Rewrite XML attributes from one value to another."
  print
  print "  -h, --help                This message"
  print "  -d file, -dictionary file Use file as the substitution dictionary."
  print "  -q, --quiet               No 'automatically generated' comment."
  print "  -s, --strip               Strip all HTML comments from the output."
  print "  -v, --version             Print version and exit"
  return
  
if __name__ == "__main__":

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:vqs", ["help", "version", "dictionary=", "quiet"])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(2)
    pass
  
  quiet_flag = False
  strip_comments_flag = False
  dictionary = False

  for o, a in opts:
    if o in ("-h", "--help"):
      usage(sys.argv[0])
      sys.exit()
      pass
    
    if o in ("-d", "--dictionary"):
      dictionary = load_rewrite_dictionary(a)
      pass

    if o in ("-q", "--quiet"):
      quiet_flag = True
      pass

    if o in ("-s", "--strip"):
      strip_comments_flag = True
      pass

    if o in ("-v", "--version"):
      print Version
      sys.exit()
      pass
    pass

  if dictionary == False:
    usage(sys.argv[0])
    sys.exit()
    pass

  if len(args) > 1:
    output = open(args[1], "w")
  else:
    output = sys.stdout
    pass
  
  xhtml = xhtml_parser(args[0], quiet_flag, strip_comments_flag, output)

  fp = open(args[0], "r")
  #sys.stdout.write('<?xml version="1.0" encodings="utf-8" standalone="yes"?>\n')
  xhtml.feed(fp.read())

  # If there is an output file named on the command line, then
  # preserve the permissions bits.
  if len(args) > 1:
    os.chmod(args[1], os.fstat(fp.fileno())[0])
    pass

  fp.close()
  xhtml.close()
  
  sys.exit(0)
