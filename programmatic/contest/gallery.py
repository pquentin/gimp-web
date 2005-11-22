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

  if len(names) == 0:
    wgo_contest.folio_fini();
    return

  this_page_index = int(form.getfirst("index", "0"))

  images_per_page = 12

  next_page_index = this_page_index + images_per_page
  prev_page_index = this_page_index - images_per_page

  next = "&gt;"
  if this_page_index < len(names) and len(names) >= next_page_index:
    next = xhtml.hyperlink({"href" : "gallery.cgi?mode=GALLERY&amp;index=%d" % (next_page_index)}, next)
    pass

  prev = "&lt;"
  if this_page_index >= images_per_page:
    prev = xhtml.hyperlink({"href" : "gallery.cgi?mode=GALLERY&amp;index=%d" % (prev_page_index)}, prev)
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

  # Comment out submission when contest is closed.
  #print xhtml.div(xhtml.hyperlink("Submit an image", {"href" : "/contest/contest.cgi"}))

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

def display_slideshow(form):
  names = get_gallery_names()

  if len(names) == 0:
    wgo_contest.folio_init()
    wgo_contest.folio_fini()
    return
  
  name = os.path.basename(form.getvalue("image", names[0]))
  refresh = int(form.getvalue("refresh", "5"))
  fullscreen = form.getvalue("fullscreen", "")
  style = form.getvalue("style", "")
  if refresh < 2:
    refresh = 2

  entry = wgo_contest.gallery_image(name)

  image_file = wgo_contest.gallery_file(entry["name"], ".png")

  next_name = name[0]
  for i in range(0, len(names)):
    if names[i] == name:
      next_name = names[(i + 1) % len(names)]
      break
    pass

  url = "gallery.cgi?display=slideshow&image=%s" % (next_name)
  if (fullscreen == "true"):
    fullscreen_attr = "&fullscreen=true"
    refresh_attr    = "&refresh=%d" % (refresh)
    if style != "":
      style_attr      = "&style=" + style
    else:
      style_attr    = ""
    
    wgo.http_preamble(["Content-Type: text/html", "Refresh: " + str(refresh) + ";url=" + url + refresh_attr + fullscreen_attr + style_attr])

    print xhtml.html.init()
    print xhtml.head()
    print xhtml.body.init({"style" : "background: black; color: white;"})
    if style == "":
      fill_window = xhtml.hyperlink({"style" : "color: gray;", "href" : url + refresh_attr + fullscreen_attr + "&style=width:100%;"}, "[fill window]")
    else:
      fill_window = xhtml.hyperlink({"style" : "color: gray;", "href" : url + refresh_attr + fullscreen_attr}, "[normal size]")
    
    print xhtml.span({"style" : "font-size: small; margin-top: 10ex; margin-bottom: 5ex;"},
                     xhtml.hyperlink({"style" : "color: gray;", "href" : url + fullscreen_attr + style_attr + "&refresh=%s" % (5)}, "5s") +  " " + 
                     xhtml.hyperlink({"style" : "color: gray;", "href" : url + fullscreen_attr + style_attr + "&refresh=%s" % (10)}, "10s") + " " +
                     xhtml.hyperlink({"style" : "color: gray;", "href" : url + fullscreen_attr + style_attr + "&refresh=%s" % (15)}, "15s") + " " +
                     xhtml.hyperlink({"style" : "color: gray;", "href" : url + fullscreen_attr + style_attr + "&refresh=%s" % (20)}, "20s") + " " +
                     fill_window
                     )

    print xhtml.table.init({"style" : "text-align: center; vertical-align: middle; width: 100%;"})
    print xhtml.table.row(
      xhtml.table.cell(xhtml.image({"style" : "%s" % (style), "src" : image_file})) +
      xhtml.table.cell({"style" : "font-size: xx-large; text-align: right; padding-right: 5%;" },
                       "<i>" + entry["title"] + "</i><br />&nbsp;" + entry["author"])
      )
    print xhtml.table.fini()

    print xhtml.body.fini()
    print xhtml.html.fini()
    pass
  else:
    url = "gallery.cgi?display=slideshow&image=%s&refresh=%d" % (next_name, refresh)
    wgo.http_preamble(["Content-Type: text/html", "Refresh: %s;url=%s" % (refresh, url)])
    wgo.header("page", "GIMP Splash Image Slideshow", [{"rel" : "stylesheet", "href" : wgo_contest.config.contest_dir + "wgo-contest.css", "type" : "text/css"}])

    print xhtml.span({"style" : "font-size: small; margin-bottom: 5ex;"},
                     xhtml.hyperlink({"href" : "gallery.cgi?display=slideshow&image=%s&refresh=%s" % (next_name, 5)}, "[5s]") +  " " + 
                     xhtml.hyperlink({"href" : "gallery.cgi?display=slideshow&image=%s&refresh=%s" % (next_name, 10)}, "[10s]") + " " +
                     xhtml.hyperlink({"href" : "gallery.cgi?display=slideshow&image=%s&refresh=%s" % (next_name, 15)}, "[15s]") + " " +
                     xhtml.hyperlink({"href" : "gallery.cgi?display=slideshow&image=%s&refresh=%s" % (next_name, 20)}, "[20s]") + " " +
                     xhtml.hyperlink({"href" : "gallery.cgi?display=slideshow&image=%s&refresh=%s&fullscreen=true" % (next_name, refresh)}, "[full window]")
                     )
    print xhtml.table.init({"class" : "splash-slideshow"})
    print xhtml.table.row(
      xhtml.table.cell(xhtml.image({"src" : image_file})) +
      xhtml.table.cell("<i>" + entry["title"] + "</i><br />&nbsp;" + entry["author"])
      )
    print xhtml.table.fini()

    wgo_contest.folio_fini()
    pass
  return

def main(argv):
  form = cgi.FieldStorage()

  display = form.getvalue("display", "gallery")
  
  if display in ["gallery", "GALLERY"]: display_gallery(form)
  elif display in ["image", "IMAGE"]: display_image(form)
  elif display in ["slideshow", "SLIDESHOW"]: display_slideshow(form)
  else:
    pass

  return (0)

sys.exit(main(sys.argv))
