#!/usr/bin/env ${PYTHON}
# -*- mode: python py-indent-offset: 2; -*-
# $Id$
#
# www.gimp.org website administration and tools
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
import fcntl
import getopt
import mimetypes
import os
import re
import rfc822
import sha
import stat
import string
import sys
import time
import types
import base64

import xhtml
import wgo
import contest_config as config

class gallery_image:
  
  def __init__(self, name):
    self.attrs = {"name" : name,
                  "author" : "",
                  "email" : "",
                  "title" : ""}

    if self.exists():
      self.restore()
    else:
      self.delete()
    
    return None

  def __getitem__(self, key):
    if key == "image": return (gallery_file(self["name"], ".png"))

    if key == "thumb":
      if os.path.isfile(gallery_path(self["name"], "-t.jpg")):
        return (gallery_file(self["name"], "-t.jpg"))
      if os.path.isfile(gallery_path(self["name"], "-t.png")):
        return (gallery_file(self["name"], "-t.png"))
      return ("")
      pass
    
    return (self.attrs[key])
  
  def __setitem__(self, key, value):
    old = self.attrs[key]
    self.attrs[key] = value;
    return (old)
  
  def __repr__(self):
    for key in self.attrs:
      typ = str(type(self.attrs[key]))
      typ = typ.replace("<type '", "").replace("'>", "")
      #print key + ": " + typ + ": " + str(self.attrs[key])
      pass

  def _ashtml(self, which="image"):
    return (xhtml.span(self["title"], {"class" : "title"})
            + (xhtml.image({"src" : self[which]}))
            + (xhtml.span(self["author"] + "&nbsp;", {"class": "author"})
	    #+ xhtml.span("&nbsp;")
            #   + xhtml.span("&nbsp;" + xhtml.character_reference(self["email"]), {"class" : "email"})
	    ))

  def ashtml(self, which="image"):
    return (xhtml.table(xhtml.table.row(xhtml.table.cell(xhtml.div(self["title"], {"class" : "title"}), {"colspan": 2}))
                        + xhtml.table.row(xhtml.table.cell(xhtml.image({"src" : self[which]}), {"colspan" : 2}))
                        + xhtml.table.row(xhtml.table.cell(xhtml.span(self["author"], {"class" : "author"}), {"class" : "author"}))
                        # + xhtml.table.row(xhtml.table.cell(xhtml.span(self["email"], {"class" : "email"}), {"class" : "email"}))
                        , {"class" : "splash-thumb"}))

  def delete(self):
    try:
      try: os.remove(gallery_path(self["name"], ".png"))
      except: pass

      try: os.remove(gallery_path(self["name"], "-t.png"))
      except: pass

      try: os.remove(gallery_path(self["name"], "-t.jpg"))
      except: pass

      try: os.remove(gallery_path(self["name"], ".meta"))
      except: pass
      return (True)
    except:
      pass
    return (False)

  def exists(self):
    if not os.path.isfile(gallery_path(self["name"], ".meta")): return (False)
    if not os.path.isfile(gallery_path(self["name"], ".png")): return (False)
    if not os.path.isfile(gallery_path(self["name"], "-t.png")) and not os.path.isfile(gallery_path(self["name"], "-t.jpg")): return (False)
    return (True)
    
  def save(self):
    fp = open(gallery_path(self["name"], ".meta"), "w")
    for key in self.attrs:
      typ = str(type(self.attrs[key]))
      typ = typ.replace("<type '", "").replace("'>", "")
      print >>fp, key + ": " + typ + ": " + str(self.attrs[key])
      #print key + ": " + typ + ": " + str(self.attrs[key])
      pass

    fp.close()
    #try: os.chown(gallery_path(self["name"], ".meta"), wgo.config.user_uid, wgo.config.user_gid)
    #except: pass
    
    return (True)

  def restore(self):
    fp = open(gallery_path(self["name"], ".meta"), "r")
    for l in fp.readlines():
      l = l.replace("\n", "")
      (attribute, typ, value) = string.split(l, ": ", 2)
      if self.attrs.has_key(attribute):
        if typ == "str": self[attribute] = value
        elif typ == "int": self[attribute] = int(value)
        else: self[attribute] = int(value)
        pass
      pass
    
    fp.close()
    return
    
  pass
  

def image_generate(title, image_file, author, email):
  img = (xhtml.div(title, {"class" : "title"})
         + xhtml.image({"src" : image_file})
         + xhtml.div(xhtml.span(author, {"class": "author"}) 
         # + xhtml.span(xhtml.mailto(email), {"class" : "email"})
         ))

  img = (xhtml.table(xhtml.table.row(xhtml.table.cell(xhtml.div(title, {"class" : "title"}), {"colspan": 2}))
                     + xhtml.table.row(xhtml.table.cell(xhtml.image({"src" : image_file}), {"colspan" : 2}))
                     + xhtml.table.row(xhtml.table.cell(xhtml.span(author, {"class" : "author"}), {"class" : "author"}))
                     # + xhtml.table.row(xhtml.table.cell(xhtml.span(email, {"class" : "email"}), {"class" : "email"}))
                     , {"class" : "splash-thumb"}))
  
  return (img)

#
# Return the relative pathname of the named file affixed with the supplied suffix.
#
def gallery_file(name, suffix=""):
  return (config.gallery_dir + name + suffix)

#
# Return the full pathname of the named file affixed with the supplied suffix.
#
def gallery_path(name, suffix=""):
  return (config.gallery_path + name + suffix)

def spool_file(name, suffix=""):
  return (config.spool_dir + name + suffix)

def spool_path(name, suffix=""):
  return (config.spool_path + name + suffix)


def folio_init(title=""):
  wgo.http_preamble(["Content-Type: text/html"])
  wgo.header("page", title, [{"rel" : "stylesheet", "href" : config.contest_dir + "wgo-contest.css", "type" : "text/css"}])
  return

def folio_fini():
  print wgo.page_fini()
  print wgo.xhtml_fini()
  return
