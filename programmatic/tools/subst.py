#!/usr/bin/env python2.2
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
# Note that attribute names can be rewritten as well.
#

import types
import string
import sys
import os
import re
import HTMLParser
import getopt

sys.path = ['${SRCDIR}'] + sys.path



def subst(dictionary, body):
  keys = dictionary.keys()
  keys.sort()

  for key in keys:
    body = string.replace(body, '@'+key+'@', dictionary[key])
    pass
  
  return (body)

def load_rewrite_dictionary(filename):
  dictionary = {}
  
  fp = open(filename, "r")
  lines = fp.readlines()
  fp.close()
  
  for line in lines:
    if len(line) > 1:
      dictionary.update(eval(line))
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
  print "  -v                        Print version and exit"
  return
  
if __name__ == "__main__":

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:vq", ["help", "version", "dictionary=", "quiet"])
  except getopt.GetoptError:
    usage(sys.argv[0])
    sys.exit(2)
    pass
  
  quiet_flag = False

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

    if o in ("-v", "--version"):
      print Version
      sys.exit()
      pass
    pass


  fp = open(args[0], "r")
  sys.stdout.write(subst(dictionary, fp.read()))
  fp.close()
  
  sys.exit(0)
