#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
# "every tool is a weapon, if you hold it right."
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
import fcntl
import email
import errno
import getopt
import mimetypes
import os
import re
import rfc822
import stat
import sys
import time
import types
import Cookie
import cgi
import mailbox
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo
import wgo_contest

def os_path_root(fname):
  p = str(fname).rfind(".")
  return (fname[0:p])


def get_gallery_names():
  d = dict()
  map(lambda f: d.update({os_path_root(f).replace("-t", ""): False}), os.listdir(wgo_contest.config.gallery_path))
  names = d.keys()
  names.sort()
  return (names)
  

def format(name):
  view_button = {"name" : "action", "value" : "view"}
  view = "gallery.cgi?display=image&amp;name=" + name

  entry = wgo_contest.gallery_image(name)
  if not entry.exists():
    link = "Eeek!  This entry is not available in the gallery. ", name
  else:
    link = entry.ashtml("thumb") + xhtml.hyperlink("view", {"href" : view, "class" : "faux-button"})
    pass

  return (xhtml.div(link, {"class" : "splash-thumb"}))


def display_gallery(form):
  wgo_contest.folio_init("GIMP Splash Image Gallery")

  names = get_gallery_names()

  index = int(form.getfirst("index", "0"))
  tableless = int(form.getfirst("tableless", "0"))
  images_per_page = 8

  next = ""
  next_page_images = index + images_per_page + 1
  if index < len(names) and len(names) >= next_page_images:
    next = xhtml.hyperlink("NEXT", {"class" : "faux-button", "href" : "gallery.cgi?display=GALLERY&amp;index=%d" % (next_page_images)})
    pass

  prev = ""
  prev_page_images = index - images_per_page - 1
  if index >= images_per_page:
    prev = xhtml.hyperlink("PREV", {"class" : "faux-button", "href" : "gallery.cgi?display=GALLERY&amp;index=%d" % (prev_page_images)})
    pass

  #print xhtml.div(xhtml.span(prev, {"style" : "float: left;"}) + xhtml.span(next, {"style" : "float: right;"}) + "&nbsp;", {"style" : "height 10ex;"})

  if tableless == 0:
    if len(names) > 0:
      print xhtml.table.init({"cellspacing" : 6, "cellpadding" : 0, "border" : 0, "class" : "gallery"})
      print xhtml.table.row.init()
      map(lambda k: sys.stdout.write(str(xhtml.table.cell(format(k), {"style" : "text-align: left;"}))), names[index:index+(images_per_page/2)])
      print xhtml.table.row.fini()

      if len(names[index+(images_per_page/2):index+images_per_page + 1]) > 0:
        print xhtml.table.row.init()
        map(lambda k: sys.stdout.write(str(xhtml.table.cell(format(k), {"style" : "text-align: left;"}))), names[index+(images_per_page/2):index+images_per_page + 1])
        print xhtml.table.row.fini()
        pass
      
      print xhtml.table.fini()
      pass
    pass
  else:                                 # table-less layout
    print xhtml.div.init({"style" : "vertical-align: bottom;"})
    print xhtml.div("&nbsp;", {"style" : "clear: both;"})
    for k in names[index:next_page_images]:
      print xhtml.div(format(k), {"style" : "float: left; margin: 1em;"})
      pass
    print xhtml.div("&nbsp;", {"style" : "clear: both;"})
    print xhtml.div.fini()
    pass

  print xhtml.div(xhtml.hyperlink("Submit an image", {"href" : "/contest/contest.cgi"}))

  wgo_contest.folio_fini()
  return


def display_image(form):
  wgo_contest.folio_init("GIMP Splash Image Contender")

  name = os.path.basename(form.getvalue("name", "")) # XXX
  entry = wgo_contest.gallery_image(name)

  if entry.exists():
    print xhtml.div(entry.ashtml("image"), {"class": "splash-image"})
  else:
    print wgo.error("That image is not available in the gallery.")
    pass

  wgo_contest.folio_fini()

  return
  

def main(argv):
  form = cgi.FieldStorage()

  display = form.getvalue("display", "gallery")
  
  if display in ["gallery", "GALLERY"]: display_gallery(form)
  elif display in ["image", "IMAGE"]: display_image(form)
  else:
    pass

  return (0)

sys.exit(main(sys.argv))
