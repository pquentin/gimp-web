#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
#
# www.gimp.org website administration and tools
#
# Copyright (C) 2002, 2003 Helvetix Victorinox, a pseudonym,
# Mountain View, California
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
import errno
import os
import re
import stat
import sys
import types
import time
import string
import cgi
import cgitb; cgitb.enable()

sys.path = ['${LIBDIR}'] + sys.path

import xhtml
import wgo
import wgo_develop

scripts = [
  (wgo.config.admin_path + "/develop/gimp-unstable", "/develop/unstable.html", "/develop/unstable.txt"),
  (wgo.config.admin_path + "/develop/gegl-unstable", "/develop/gegl.html",     "/develop/gegl.txt"),
  (wgo.config.admin_path + "/develop/film-gimp",     "/develop/film.html",     "/develop/film.txt"),
  (wgo.config.admin_path + "/develop/gimp-help",     "/develop/help.html",     "/develop/help.txt"),
  ]

def header(title="", links=[]):
  print
  print wgo.xhtml_init()
  
  print xhtml.title(title)
  print wgo.look_feel()

  print xhtml.link({"rel" : "stylesheet", "href" : "/style/extended.css", "type" : "text/css", "media" : "screen"})
  print xhtml.link({"rel" : "stylesheet", "href" : "/style/wgo-admin.css", "type" : "text/css", "media" : "screen"})

  for link in links: print xhtml.link(link)

  print wgo.page_init('admin')

  return (True)


def footer(prefix=None):
  if prefix != None:
    print prefix
    pass
  
  print wgo.page_fini('admin')
  print wgo.xhtml_fini()
  
  return (True)

def rebuild(script):

  good = [ os.path.basename(p[0]) for p in scripts ]
  
  if script in good:
    fp = os.popen(wgo.config.admin_path + "/develop/" + script, "r")
    lines = fp.readlines()
    fp.close()
    print xhtml.para(string.join(lines, "<br />\n"))
  else:
    # log the potentially nefarious activity
    pass

  print xhtml.hyperlink("Continue", {"href" : "changelogs.cgi"})
  return

def html_index_page(script, html, text):

  html_mtime = "never"
  text_mtime = "never"
  html_path = wgo.config.DocumentRoot_path + "/" + html
  text_path = wgo.config.DocumentRoot_path + "/" + text

  if os.path.exists(html_path): html_mtime = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(os.path.getmtime(html_path)))
  if os.path.exists(text_path): text_mtime = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(os.path.getmtime(text_path)))
  
  update = xhtml.hyperlink("rebuild", {"class" : "faux-button", "href" : "changelogs.cgi?rebuild=" + os.path.basename(script)})
  
  print xhtml.table.row(xhtml.table.cell(xhtml.hyperlink(os.path.basename(script), {"href" : html}))
                        + xhtml.table.cell(html_mtime)
                        + xhtml.table.cell(update))
  return (1)

def main():
  print "Content-Type: text/html"
  header("", [])

  form = cgi.FieldStorage()

  if form.has_key("rebuild"):
    rebuild(form["rebuild"].value)
  else:
    print xhtml.para("Normally, the ChangeLog files are automatically updated from an automated cron(1) job.")
    print xhtml.para("You may force a particular ChangeLog file to be updated here.")
                    
    print xhtml.table.init({"class" : "wgo-admin", "style" : "width: 100%; border-width: 0 0 0 0;"})
    print xhtml.table.row(xhtml.table.header("ChangeLog", {"style" : "text-align: left;"})
                          + xhtml.table.header("Last Update", {"style" : "text-align: left;"})
                          + xhtml.table.header("", {"style" : "text-align: left;"}))

    map(lambda s: apply(html_index_page, s), scripts)
    print xhtml.table.fini()
    pass
  
  footer()
  
  return (0)


sys.exit(main())
