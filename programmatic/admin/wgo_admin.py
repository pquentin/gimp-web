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

import cgi
import errno
import fcntl
import os
import stat
import string
import sys
import types

import wgo
import xhtml

def head_boilerplate(css=[], headers=[]):
  headers = headers + ["Content-type: text/html"]
  for h in headers: print h

  return (header("www.gimp.org - Administration", css))

def header(title, links):
  print
  print wgo.xhtml_init()
  
  print xhtml.title(title)
  print wgo.look_feel()

  print xhtml.link({"rel" : "stylesheet", "href" : "/style/extended.css", "type" : "text/css", "media" : "screen"})
  print xhtml.link({"rel" : "stylesheet", "href" : "/style/wgo-admin.css", "type" : "text/css", "media" : "screen"})
  for href in links:
    print xhtml.link({"rel" : "stylesheet", "href" : href, "type" : "text/css", "media" : "screen"})
    pass

  print wgo.page_init('admin')

  return (True)


def footer(prefix=None):
  if prefix != None:
    print prefix
    pass
  
  print wgo.page_fini('admin')
  print wgo.xhtml_fini()
  
  return (True)
