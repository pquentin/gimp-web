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

import xhtml
import wgo_config as config
import os

def spool_file(name, suffix=""):
  return (config.spool_dir + os.path.basename(name) + suffix)

def spool_path(name, suffix=""):
  return (config.spool_path + os.path.basename(name) + suffix)

def error(text):
  return (xhtml.div("Eeek! An error!", {"class" : "subtitle"}) + xhtml.para(text))

def header(title, css_list, left_menu):
  extended_css = "/style/extended.css"
  
  print
  print xhtml.include('%s/includes/header_pretitle.inc' % (config.DocumentRoot_path))
  print xhtml.title(title)
  print xhtml.link(None, {"rel" : "stylesheet", "href" : extended_css, "type" : "text/css", "media" : "screen", "title" : title})
  for href in css_list:
    print xhtml.link(None, {"rel" : "stylesheet", "href" : href, "type" : "text/css", "media" : "screen", "title" : title})
    pass
  print xhtml.include('%s/includes/header_posttitle.inc' % (config.DocumentRoot_path))
  print xhtml.include(left_menu)
  return (True)

def footer():
  print xhtml.include('%s/includes/linkbar.inc' % (config.DocumentRoot_path))
  
  #print xhtml.object("doesn't work", {"standby": "loading", "type" : "image/png",
  #"data" : 'data:base64, ' + xhtml.encodefile('/home/asdf/public_html/helvetix/anybrowser.png')})
  #                                      "data" : 'data:binary, ' + xhtml.rawfile('/home/asdf/public_html/helvetix/anybrowser.png')})
  if config.validate: print xhtml.validate()
  else: print config.validate
  print xhtml.div("version 1.0", {"class" : "watermark"})
  print xhtml.include('%s/includes/footer.inc' % (config.DocumentRoot_path))
  return (True)

