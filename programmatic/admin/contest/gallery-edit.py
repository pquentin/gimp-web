#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
# "every tool is a weapon, if you hold it right."
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003  Helvetix Victorinox, a pseudonym
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

import errno
import getopt
import os
import re
import stat
import sys
import time
import types
import Cookie
import cgi
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

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
    link =  xhtml.div(entry.ashtml("thumb")
                      + (xhtml.span(xhtml.hyperlink("edit", {"href" : edit, "class" : "faux-button"})
                                    + xhtml.hyperlink("delete", {"href" : delete, "class" : "faux-button"}), {"style" : "text-align: left;"})),
                           {"style" : "text-align: left;"})
    pass

  return (xhtml.div(link, {"class" : "splash-thumb"}))

def edit_image(form):
  wgo.http_preamble(["Content-type: text/html"])

  wgo_admin.header('www.gimp.org - Administration - Splash Image',
                   [ {"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "/wgo-contest.css", "type" : "text/css", "media" : "screen"} ])

  print xhtml.h1("www.gimp.org - Administrate Contest - Edit Entry", {"class" : "heading"})

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
  wgo.http_preamble(["Content-type: text/html"])

  wgo_admin.header('www.gimp.org - Administration - Splash Image',
                   [ {"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "/wgo-contest.css", "type" : "text/css", "media" : "screen"} ])

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
  wgo.http_preamble(["Content-type: text/html"])

  wgo_admin.header('www.gimp.org - Administration - Splash Image',
                   [ {"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "/wgo-contest.css", "type" : "text/css", "media" : "screen"} ])

  name = form["name"].value
  entry = wgo_contest.gallery_image(name)

  entry.delete()

  wgo_admin.footer()
  return (0)

def display_gallery(form):
  wgo.http_preamble(["Content-type: text/html"])

  wgo_admin.header('www.gimp.org - Administration - Splash Image',
                   [ {"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "/wgo-contest.css", "type" : "text/css", "media" : "screen"} ])

  names = get_gallery_names()

  if len(names) == 0:                   # If there's nothing to do, return
    wgo_admin.footer()
    return
    
  this_page_index = int(form.getfirst("index", "0"))

  images_per_page = 12

  next_page_index = this_page_index + images_per_page
  prev_page_index = this_page_index - images_per_page

  next = "&gt;"
  if this_page_index < len(names) and len(names) >= next_page_index:
    next = xhtml.hyperlink({"href" : "gallery-edit.cgi?mode=GALLERY&amp;index=%d" % (next_page_index)}, next)
    pass

  prev = "&lt;"
  if this_page_index >= images_per_page:
    prev = xhtml.hyperlink({"href" : "gallery-edit.cgi?mode=GALLERY&amp;index=%d" % (prev_page_index)}, prev)
    pass

  print xhtml.table.init({"class" : "contest-progress-bar"})
  print xhtml.table.row.init()
  print xhtml.table.cell({"id" : "prev"}, prev)

  position = this_page_index * 100 / len(names)

  for i in range(0, 100):
    index = len(names) * i / 100
    link = "&nbsp;"
    if i == position:
      print xhtml.table.cell({"id" : "current-position", "title" : "image %d (%d%%)" % (this_page_index, i)}, link)
    else:
      print xhtml.table.cell(link)
      pass
    pass
  print xhtml.table.cell({"id" : "next" }, next)

  print xhtml.table.row.fini()
  print xhtml.table.fini()
  
  print xhtml.table.init({"class" : "contest-image-gallery"})

  row_start = this_page_index
  row = names[row_start : row_start + 4]
  print xhtml.table.row("".join(map(lambda k: str(xhtml.table.cell(format(k))), row)))

  row_start = this_page_index + 4
  row = names[row_start : row_start + 4]
  print xhtml.table.row("".join(map(lambda k: str(xhtml.table.cell(format(k))), row)))

  row_start = this_page_index + 8
  row = names[row_start : row_start + 4]
  print xhtml.table.row("".join(map(lambda k: str(xhtml.table.cell(format(k))), row)))

  print xhtml.table.fini()

  wgo_admin.footer()
  return

def display_image(form):
  wgo.http_preamble(["Content-type: text/html"])

  wgo_admin.header('www.gimp.org - Administration - Splash Image',
                   [ {"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "/wgo-contest.css", "type" : "text/css", "media" : "screen"} ])

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

  if mode in ["gallery", "GALLERY"]: display_gallery(form)
  elif mode in ["edit", "EDIT"]:     edit_image(form)
  elif mode in ["save", "SAVE"]:     save_image(form)
  elif mode in ["delete", "DELETE"]: delete_image(form)
  else:
    display_gallery(form)
    pass

  return (0)

sys.exit(main(sys.argv))
