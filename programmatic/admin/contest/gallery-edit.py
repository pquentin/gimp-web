#!/usr/bin/env python
# -*- mode: python py-indent-offset: 2; -*-
# "every tool is a weapon, if you hold it right."
#
# www.gimp.org website administration and tools
# Copyright (C) 2002, 2003  Helvetix Victorinox, pseudonym
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

sys.path.append('__LIBDIR__')

import xhtml
import wgo
import wgo_admin
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
  edit_button = {"name" : "action", "value" : "edit"}
  delete_button = {"name" : "action", "value" : "delete"}
  edit = "gallery-edit.cgi?mode=EDIT&amp;name=" + name
  delete = "gallery-edit.cgi?mode=DELETE&amp;name=" + name
  
  entry = wgo_contest.gallery_image(name)
  if not entry.exists():
    link = "Eeek!  This entry is not available in the gallery. ", name
  else:
    link = (xhtml.div(xhtml.span(xhtml.hyperlink(xhtml.input.submit(edit_button), {"href" : edit})
                                 + xhtml.hyperlink(xhtml.input.submit(delete_button), {"href" : delete}), {"style" : "text-align: left;"}),
            {"style" : "border-bottom: 1px dotted black; text-align: left;"})
            + entry.ashtml("thumb"))
    link =  xhtml.div(entry.ashtml("thumb")
             + (xhtml.span(xhtml.hyperlink(xhtml.input.submit(edit_button), {"href" : edit})
                                    + xhtml.hyperlink(xhtml.input.submit(delete_button), {"href" : delete}), {"style" : "text-align: left;"})),
                      {"style" : "text-align: left;"})
    pass

  return (xhtml.div(link, {"class" : "splash-thumb"}))

def edit_image(form):
  wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"])
  
  print xhtml.div("www.gimp.org - Administrate Contest - Edit Entry", {"class" : "heading"})

  name = form["name"].value

  image = wgo_contest.gallery_image(name)
  
  cell = xhtml.table.cell
  row = xhtml.table.row

  fields = (xhtml.table.init({"cellspacing" : 6})
            + row(cell("Name:",          {"style" : "font-weight: bold"}) + cell(name))
            + row(cell("Title:",         {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "title", "value" : image["title"]})))
            + row(cell("Artist's Name:", {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "author", "value" : image["author"]})))
            + row(cell("Artists Email:", {"style" : "font-weight: bold"}) + cell(xhtml.input.text({"name" : "email", "value" : image["email"]})))
            + row(cell(xhtml.input.hidden({"name" : "name", "value" : name}))
                  + cell(xhtml.input.submit({"name" : "mode", "value" : "SAVE"})
                         + xhtml.input.submit({"name" : "mode", "value" : "DELETE"})))
            + xhtml.table.fini())
  
  print xhtml.para(xhtml.form(xhtml.div(fields), {"enctype" : "multipart/form-data", "method" : "post", "action" : "gallery-edit.cgi"}))

  if image.exists():
    print xhtml.div(image.ashtml("image"), {"class": "splash-image"})
  else:
    print xhtml.div(xhtml.para("That image is not available in the gallery."))
    pass

  wgo_admin.footer()
  return (0)

def save_image(form):
  wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"], ["Location: gallery-edit.cgi"])

  name = form["name"].value

  entry = wgo_contest.gallery_image(name)
  
  entry["title"] = form.getvalue("title", "")
  entry["author"] = form.getvalue("author", "")
  entry["email"] = form.getvalue("email", "")

  print entry["author"], "<br/>"
  entry.save()

  wgo_admin.footer()
  return (0)

def delete_image(form):
  wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"], ["Location: gallery-edit.cgi"])

  name = form["name"].value
  entry = wgo_contest.gallery_image(name)
  entry.delete()

  wgo_admin.footer()
  return (0)

def display_gallery(form):
  wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"])

  names = get_gallery_names()

  index = int(form.getfirst("index", "0"))

  next_button = xhtml.input.submit({"value" : "NEXT"})
  prev_button = xhtml.input.submit({"value" : "PREV"})

  images_per_page = 8

  next = ""
  next_page_images = index + images_per_page + 1
  
  if index < len(names) and len(names) >= next_page_images:
    next = xhtml.hyperlink(next_button, {"href" : "gallery-edit.cgi?mode=GALLERY&amp;index=%d" % (next_page_images)})
    pass

  prev = ""
  prev_page_images = index - images_per_page - 1
  if index >= images_per_page:
    prev = xhtml.hyperlink(prev_button, { "href" : "gallery-edit.cgi?mode=GALLERY&amp;index=%d" % (prev_page_images)})
    pass

  print xhtml.para(xhtml.span(prev, {"style" : "float: left;"})
                   + xhtml.span(next, {"style" : "float: right;"}) + "&nbsp;", {"style" : "height 10ex;"})

  if True:
    if len(names) > 0:
      print xhtml.table.init({"cellspacing" : 6, "cellpadding" : 0, "border" : 0, "class" : "gallery"})
      print xhtml.table.row.init()
      map(lambda k: sys.stdout.write(str(xhtml.table.cell(format(k)))), names[index:index+(images_per_page/2)])
      print xhtml.table.row.fini()
      print xhtml.table.row.init()
      map(lambda k: sys.stdout.write(str(xhtml.table.cell(format(k)))), names[index+(images_per_page/2 + 1):index+images_per_page + 1])
      print xhtml.table.row.fini()
      print xhtml.table.fini()
      pass
  else:
    print xhtml.div.init({"style" : "vertical-align: bottom;"})
    print xhtml.div("&nbsp;", {"style" : "clear: both;"})
    for k in names[index:next_page_images]:
      print xhtml.div(format(k), {"style" : "float: left; margin: 1em;"})
      pass
    print xhtml.div("&nbsp;", {"style" : "clear: both;"})
    print xhtml.div.fini()
    pass

  wgo_admin.footer()
  return

def display_image(form):
  wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"])

  name = os.path.basename(form.getvalue("name", ""))

  entry = wgo_contest.gallery_image(name)

  if entry.exists():
    print xhtml.div(entry.ashtml("image"), {"class": "splash-image"})
  else:
    print wgo.error("That image is not available in the gallery.")
    pass

  wgo_admin.footer()
  return
  
def main(argv):
  form = cgi.FieldStorage()

  mode = form.getvalue("mode", "GALLERY")

  if mode in ["gallery", "GALLERY"]:  display_gallery(form)
  elif mode in ["edit", "EDIT"]:   edit_image(form)
  elif mode in ["save", "SAVE"]:   save_image(form)
  elif mode in ["delete", "DELETE"]: delete_image(form)
  else:
    wgo_admin.head_boilerplate([wgo_contest.config.contest_dir + "wgo-contest.css"])
    print xhtml.para(mode)
    wgo_admin.footer()
    pass

  return (0)

sys.exit(main(sys.argv))